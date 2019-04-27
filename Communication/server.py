#server.py

import socket
import time
import datetime
import threading
import multiprocessing
import socketserver
import pymysql
import json

#Need to configure
ANY = '0.0.0.0'
SERVER_ADDR = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
SERVER_ACK_PORT = 10003
SERVER_REG_PORT = 10002
CLIENT_PORT = 10000
RECV_PORT = 10001
MULTICAST_ADDR = "224.0.1.0"
MULTICAST_PORT = 18888


global clients 
clients = {}

lock = threading.RLock()

def insertData2Sql(data) :
    # 将string转换为dic/list
    data = json.loads(data)
    data = json.loads(data)

    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "12345678", "swarmintelligence")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    sql = []
    # SQL 插入语句
    if (type(data) == dict) :
        sql.append("REPLACE INTO `location` SET `ID`=" + str(data['ID']) +",`X`=" + str(data['X']) +",`Y`="+ str(data['Y']) + ",`Z`="+ str(data['Z']) +",`speed`="+ str(data['speed']) + ",`pitch`="+ str(data['pitch']) + ",`roll`="+ str(data['roll']) + ",`azimuth`="+ str(data['azimuth']))
    else :
        sql.append("TRUNCATE TABLE history")
        for idata in data :
            sql.append("REPLACE INTO `location` SET `ID`=" + str(idata['ID']) +",`X`=" + str(idata['X']) +",`Y`="+ str(idata['Y']) + ",`Z`="+ str(idata['Z']) +",`speed`="+ str(idata['speed']) + ",`pitch`="+ str(idata['pitch']) + ",`roll`="+ str(idata['roll']) + ",`azimuth`="+ str(idata['azimuth']))

    try:
        # 执行sql语句
        for isql in sql :
            cursor.execute(isql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()


class TreeTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).decode() #接受数据  
        insertData2Sql(self.data)


class recvREGThread(threading.Thread) :
    def __init__(self, s, r):
        threading.Thread.__init__(self)
        self._running = True
        self.r = r
        self.s = s
    def run(self) :
        while self._running :
            try:
                data, addr = self.r.recvfrom(1024)
                lock.acquire()
                if data.decode() == 'REG' :
                    if addr[0] not in clients :
                        clients[addr[0]] = 0
                        self.s.sendto(bytes('REG', encoding = "utf8"), addr)
                        print(data.decode(), addr)
                    else :
                        self.s.sendto(bytes('REG', encoding = "utf8"), addr)    
                elif data.decode() == 'LOG' :
                    if addr[0] in clients :
                        del clients[addr[0]]
                        self.s.sendto(bytes('LOG', encoding = "utf8"), addr)
                        print(data.decode(), addr)
                lock.release()
            except BlockingIOError:
                pass
    def terminate(self) :
        self._running = False

class recvACKThread(threading.Thread) :
    def __init__(self, s):
        threading.Thread.__init__(self)
        self._running = True
        self.s = s
        self.count = len(clients)
    def run(self) :
        while self._running and (sum(clients[addr] for addr in clients) != len(clients)):
            try:
                data, addr = self.s.recvfrom(1024)
                lock.acquire()
                if data.decode() == 'ACK' :
                    clients[addr[0]] = 1
                    self.count -= 1
                lock.release()
                print(data.decode(), addr)
            except BlockingIOError:
                pass
    def terminate(self) :
        self._running = False

def __sendData(s, data, times) :
    s.sendto(data, (MULTICAST_ADDR, MULTICAST_PORT))
    recvACK = recvACKThread(s)
    recvACK.start()
    time.sleep(0.5)
    count = len(clients)
    for addr in clients :
        count -= clients[addr]
    recvACK.terminate()
    if count == 0 :
        for addr in clients:
            clients[addr] = 0
        return True
    elif times != 3 :
        times += 1
        return __sendData(s, data, times)
    else :
        for addr in clients:
            if clients[addr] == 0 :
                del clients[addr]
        for addr in clients:
            clients[addr] = 0
        return True

# 监听数据库变化并读取数据
def __fetchDataFromSql() :

    # SQL 查询语句
    sql = "SELECT * FROM command ORDER BY time DESC"
    t = time.time()
    flag = True
    while flag :
        try:
            # 执行SQL语句
            db = pymysql.connect("localhost","root","12345678","swarmintelligence" )
            cursor = db.cursor()
            cursor.execute(sql)
            # 获取所有记录列表
            result = cursor.fetchone()
            db.close()
            timestamp = result[7].timestamp()
            if timestamp > t :
                t = timestamp
                data = {
                'CommandID' : result[0],
                'start_x'   : result[1],
                'start_y'   : result[2],
                'start_z'   : result[3],
                'end_x'     : result[4],
                'end_y'     : result[5],
                'end_z'     : result[6],
                'time'      : timestamp,
                'IDs'       : result[8],
                }
                flag = False
            else :
                time.sleep(0.5)

        except:
           pass

    data = json.dumps(data)
    return data

def runSendService() :
    r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    r.bind((SERVER_ADDR, SERVER_REG_PORT))
    r.setblocking(False)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind((SERVER_ADDR, SERVER_ACK_PORT))
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 10)

    requestClient = recvREGThread(s, r)
    requestClient.start()
    #监听数据库变化并读取数据进行发送
    flag = True
    while flag :
        data = __fetchDataFromSql()
        __sendData(s, bytes(data, encoding = 'utf8'), 0)

    #通知终端退出
    __sendData(s, bytes("STD", encoding = 'utf8'), 0)
    time.sleep(5)

    requestClient.terminate()

def runReceiveService() :
    server = socketserver.ThreadingTCPServer((SERVER_ADDR,RECV_PORT),TreeTCPHandler)
    server.serve_forever()#打开服务器


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=runReceiveService,args=())
    p2 = multiprocessing.Process(target=runSendService,args=())
    p1.start()
    p2.start()
    p1.join()
    p2.join()
#server.py

import socket 
import time
import threading
import socketserver
import pymysql
import json

#Need to configure
ANY = '0.0.0.0'
SERVER_ADDR = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
SERVER_ACK_PORT = 1600
SERVER_REG_PORT = 1601
CLIENT_PORT = 3333
RECV_PORT = 3334
MULTICAST_ADDR = "224.0.1.0"
MULTICAST_PORT = 18888


global clients 
clients = {}

lock = threading.RLock()

class TreeTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).decode() #接受数据  
        __insertData2Sql(data)


class recvREGThread(threading.Thread) :
    def __init__(self, r):
        threading.Thread.__init__(self)
        self._running = True
        self.r = r
    def run(self) :
        while self._running :
            try:
                data, addr = r.recvfrom(1024)
                lock.acquire()
                if data.decode() == 'REG' :
                    if addr[0] not in clients :
                        clients[addr[0]] = 0
                        s.sendto(bytes('REG', encoding = "utf8"), addr)
                elif data.decode() == 'LOG' :
                    if addr[0] in clients :
                        del clients[addr[0]]
                        s.sendto(bytes('LOG', encoding = "utf8"), addr)
                lock.release()
                print(data.decode(), addr)
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
                data, addr = s.recvfrom(1024)
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

def ____sendData(s, data) :
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
    else :
        return __sendData(s, data)

def __insertData2Sql(data) :
    # 将string转换为dic
    data = json.load(data)

    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "swarmintelligence")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = """INSERT INTO `location` (`ID`, `X`, `Y`, `Z`, `speed`, `pitch`, `roll`, `azimuth`, `time`) VALUES ( """ + data['ID'] + "," + data['X'] + ","+ data['Y'] + "," + data['Z'] + ","+ data['speed'] + ","+ data['pitch'] + ","+ data['roll'] + ","+ data['azimuth'] + ", CURRENT_TIMESTAMP)"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()

def __acquireDataFromSql() :
    pass

def runSendService() :
    r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    r.bind((SERVER_ADDR, SERVER_REG_PORT))
    r.setblocking(False)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind((SERVER_ADDR, SERVER_ACK_PORT))
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 10)

    requestClient = recvREGThread(r)
    requestClient.start()
    
    #监听数据库变化并读取数据进行发送
    #flag 需要定义
    while flag :
        data = __listenDatabase()
        __sendData(s, data)

    #通知终端退出
    __sendData(s, bytes("STD", encoding = 'utf8'))
    time.sleep(5)

    requestClient.terminate()

def runReceiveService() :
    server = socketserver.ThreadingTCPServer((SERVER_ADDR,RECV_PORT),TreeTCPHandler)
    server.serve_forever()#打开服务器



# Need to finish

# 从数据库获取最新数据
def __acquireDataFromSql() :
    return data
# 监听数据库变化并读取数据进行发送
def __listenDatabase() :
    """
    监听数据库变化
    """
    return __acquireDataFromSql


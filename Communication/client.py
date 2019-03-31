#client.py

import socket
import threading
import time
import json

#Need to configure
ANY = '0.0.0.0'
SERVER_ADDR = "192.168.3.102"
SERVER_REG_PORT = 10002
SERVER_RECV_PORT = 10001
CLIENT_PORT = 10000
MULTICAST_ADDR = "224.0.1.0"
MULTICAST_PORT = 18888


class sendThread(threading.Thread) :
    def __init__(self, c, data):
        threading.Thread.__init__(self)
        self._running = True
        self.c = c
        self.data = data
    def run(self) :
        while self._running :
            self.c.sendto(self.data.encode(), (SERVER_ADDR, SERVER_REG_PORT))
            time.sleep(0.5)

    def terminate(self) :
        self._running = False


class recvACKThread(threading.Thread) :
    def __init__(self, c):
        threading.Thread.__init__(self)
        self._running = True
        self.c = c
    def run(self) :
        data, addr = self.c.recvfrom(1024)
        print(data.decode(), addr)

    def terminate(self) :
        self._running = False

def __register(c) :
    sendREG = sendThread(c, 'REG')
    sendREG.start()
    data, addr = c.recvfrom(1024)
    print(data.decode(), addr)
    print("register success.")
    sendREG.terminate()

def __logout(c) :
    sendLOG = sendThread(c, 'LOG')
    sendLOG.start()
    data, addr = c.recvfrom(1024)
    print(data.decode(), addr)
    print("Logout success.")
    sendLOG.terminate()

def __recvData(s) :
    data, addr = s.recvfrom(1024)
    print(data.decode(), addr) 
    s.sendto(bytes("ACK", encoding = "utf8"), addr)
    return data, addr

def __work(s) :
    i = 1
    while i:
        data, addr = __recvData(s)
        if data.decode() == 'STD' :
            i = 0
        __dataProcessing(data)
    return

def run() :
    ca = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ca.connect(('8.8.8.8', 80))
    Client_Addr = ca.getsockname()[0]

    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    c.bind((Client_Addr, CLIENT_PORT))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1) 

    s.bind((ANY,MULTICAST_PORT))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 10)
    s.setsockopt(socket.IPPROTO_IP,
                 socket.IP_ADD_MEMBERSHIP,
                 socket.inet_aton(MULTICAST_ADDR)+ socket.inet_aton(ANY) )

    __register(c)
    __work(s)
    __logout(c)

def send(data) :
    #将dic数据转换成string
    data = json.dumps(data)
    sk = socket.socket() 
    try:
        sk.connect((SERVER_ADDR, SERVER_RECV_PORT))
        sk.send(data.encode())
    except socket.error as err:
        print (err)
    finally:
        sk.close()

#Need  to finish
def __dataProcessing(data) :
    pass

# 测试
if __name__ =="__main__":
    run()
    data = {
    'ID' : 101,
    'X'  : 100.0,
    'Y'  : 200.0,
    'Z'  : 300.0,
    'speed' : 15.0,
    'pitch' : 16.0,
    'roll'  : 17.0,
    'azimuth' : 18.0
    }
    data = json.dumps(data)
    send(data)

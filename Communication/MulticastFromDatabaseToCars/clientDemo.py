#clientDemo.py
#2019-03-23
#PengChen

import socket
import threading
import time

#Need to configure
ANY = '0.0.0.0'
SERVER_ADDR = "192.168.3.102"
SERVER_REG_PORT = 1601
CLIENT_PORT = 3333
MULTICAST_ADDR = "224.0.1.0"
MULTICAST_PORT = 18888

def register(c) :
    sendREG = sendThread(c, 'REG')
    sendREG.start()
    data, addr = c.recvfrom(1024)
    print(data.decode(), addr)
    print("register success.")
    sendREG.terminate()

def logout(c) :
    sendLOG = sendThread(c, 'LOG')
    sendLOG.start()
    data, addr = c.recvfrom(1024)
    print(data.decode(), addr)
    print("Logout success.")
    sendLOG.terminate()

class sendThread(threading.Thread) :
    def __init__(self, c, data):
        threading.Thread.__init__(self)
        self._running = True
        self.c = c
        self.data = data
    def run(self) :
        while self._running :
            c.sendto(self.data.encode(), (SERVER_ADDR, SERVER_REG_PORT))
            time.sleep(0.5)

    def terminate(self) :
        self._running = False


class recvACKThread(threading.Thread) :
    def __init__(self, c):
        threading.Thread.__init__(self)
        self._running = True
        self.c = c
    def run(self) :
        data, addr = c.recvfrom(1024)
        print(data.decode(), addr)

    def terminate(self) :
        self._running = False

def recvData(s) :
    data, addr = s.recvfrom(1024)
    print(data.decode(), addr) 
    s.sendto(bytes("ACK", encoding = "utf8"), addr)
    return data, addr

def dataProcessing(data) :
    pass

def work(s) :
    i = 1
    while i:
        data, addr = recvData(s)
        if data.decode() == 'STD' :
            i = 0
        dataProcessing(data)
    return
if __name__=='__main__':
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

    register(c)
    work(s)
    logout(c)
    

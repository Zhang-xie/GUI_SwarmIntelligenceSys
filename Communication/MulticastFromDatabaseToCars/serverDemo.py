#serverDemo.py
#2019-03-23
#PengChen

import socket 
import time
import threading

#Need to configure
ANY = '0.0.0.0'
SERVER_ADDR = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
SERVER_ACK_PORT = 1600
SERVER_REG_PORT = 1601
CLIENT_PORT = 3333
MULTICAST_ADDR = "224.0.1.0"
MULTICAST_PORT = 18888


global clients 
clients = {}

lock = threading.RLock()

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

def sendData(s, data) :
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
        return sendData(s, data)

if __name__=='__main__':
    r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    r.bind((SERVER_ADDR, SERVER_REG_PORT))
    r.setblocking(False)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind((SERVER_ADDR, SERVER_ACK_PORT))
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 10)

    requestClient = recvREGThread(r)
    requestClient.start()
    
    #test codes
    time.sleep(3)
    sendData(s, bytes("Message 1", encoding = 'utf8'))
    time.sleep(1)
    sendData(s, bytes("Message 2", encoding = 'utf8'))
    time.sleep(1)
    sendData(s, bytes("Message 3", encoding = 'utf8'))
    time.sleep(1)
    sendData(s, bytes("STD", encoding = 'utf8'))
    time.sleep(5)

    requestClient.terminate()
    print("exit")

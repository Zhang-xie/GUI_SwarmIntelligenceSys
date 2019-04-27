#client.py

import socket
import threading
import time
import json
import random
from multiprocessing import Process, Queue

#Need to configure
ANY = '0.0.0.0'
SERVER_ADDR = "192.168.1.3"
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

class Car_socket_client():
    def __init__(self):
        self.q_recvdata=Queue()
        self.last_command=''
        self.recv_process=Process(target=self.recv_main)
        self.recv_process.start()
    def get(self):
        data=None
        while not self.q_recvdata.empty():
            data = self.q_recvdata.get()
        return data
    def send(self,data):
        data = json.dumps(data)
        sk = socket.socket() 
        try:
            sk.connect((SERVER_ADDR, SERVER_RECV_PORT))
            sk.send(data.encode())
        except socket.error as err:
            print(err)
        finally:
            sk.close()
    def recv_main(self):
        ca = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ca.connect(('8.8.8.8', 80))
        Client_Addr = ca.getsockname()[0]
    
        c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        
        c.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#fix error:Address already in use
        
        c.bind((Client_Addr, CLIENT_PORT))
    
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1) 
    
        s.bind((ANY,MULTICAST_PORT))
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 10)
        s.setsockopt(socket.IPPROTO_IP,
                     socket.IP_ADD_MEMBERSHIP,
                     socket.inet_aton(MULTICAST_ADDR)+ socket.inet_aton(ANY) )
    
        self.recv__register(c)
        self.recv__work(s)
        self.recv__logout(c)
    def recv__logout(self,c) :
        sendLOG = sendThread(c, 'LOG')
        sendLOG.start()
        data, addr = c.recvfrom(1024)
        print(data.decode(), addr)
        print("Logout success.")
        sendLOG.terminate()
    
    def __recvData(self,s) :
        data, addr = s.recvfrom(1024)
        s.sendto(bytes("ACK", encoding = "utf8"), addr)
        return data, addr
    def recv__dataProcessing(self,data):
        if data.decode() != self.last_command :
            self.last_command = data.decode()
            data=json.loads(self.last_command)
            self.q_recvdata.put(data)
    def recv__work(self,s) :
        i = 1
        while i:
            data, addr = self.__recvData(s)
            if data.decode() == 'STD' :
                i = 0
            self.recv__dataProcessing(data)
        return
    def recv__register(self,c):
        sendREG = sendThread(c, 'REG')
        sendREG.start()
        data, addr = c.recvfrom(1024)
        print(data.decode(), addr)
        print("register success.")
        sendREG.terminate()    

if __name__ =="__main__":
    car_client=Car_socket_client()
    #GET test
    '''
    t = 3
    while t :
        time.sleep(1)
        data = car_client.get()
        if data != None :
            print("Message:",data)
            t -= 1
    '''
    #SEND test
    ca = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ca.connect(('8.8.8.8', 80))
    Client_Addr = ca.getsockname()[0]
    id = Client_Addr[10:13]
    x = random.uniform(1, 10)
    y = random.uniform(1, 10)
    while 1:
        data = {
        'ID' : int(id),
        'X'  : x,
        'Y'  : y,
        'Z'  : float(id),
        'speed' : float(id),
        'pitch' : float(id),
        'roll'  : float(id),
        'azimuth' : float(id)
        }
        data = json.dumps(data)
        car_client.send(data)
        time.sleep(0.5)
        x += random.uniform(-1, 1)
        y += random.uniform(-1, 1)

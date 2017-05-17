#############################################################
#                                                           #
#   This program is relased in the GNU GPL v3.0 licence     #
#   you can modify/use this program as you wish. Please     #
#   link the original distribution of this software. If     #
#   you plan to redistribute your modified/copied copy      #
#   you need to relased the in GNU GPL v3.0 licence too     #
#   according to the overmentioned licence.                 #
#                                                           #
#   "PROUDLY" MADE BY chkrr00k (i'm not THAT proud tbh)     #
#                                                           #
#############################################################
#                                                           #
#   I have tried to use a good mvc modelling while let-     #
#   letting the maximum usability, modularity and mode-     #
#   lling                                                   #
#                                                           #
#############################################################

import threading
import socket
import sys
from functools import wraps
from time import sleep

def semaphore(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        self.semaphore.acquire()
        res = function(self, *args, **kwargs)
        self.semaphore.release()
        return res
    return wrapper

class Clients:
    def __init__(self):
        self.connections = dict()
        self.semaphore = threading.Semaphore()
    
    @semaphore
    def add(self, addr, conn):
        self.connections[addr] = conn

    @semaphore
    def pop(self, addr):
        if addr in self.connections:
            self.connections.pop(addr)

    def get(self, addr):
        return self.connections[addr]
    
    @semaphore
    def __iter__(self):
        for x in self.connections.keys():
            yield x
    
    def __len__(self):
        return len(self.connections)

class Msg:
    def __init__(self, sender, message, channel):
        self.sender = sender
        self.message = message
        self.channel = channel
    
    def getMsg(self):
        return self.message

    def getChan():
        return self.channel

    def getSender(self):
        return self.sender

class MessageContainer:
    def __init__(self):
        self.messages = list()
        self.semaphore = threading.Semaphore()
        self.clients = list()
    
    @semaphore
    def __iter__(self):
        for x in self.messages:
            yield x
        self.messages.clear()

    @semaphore
    def append(self, el):
        self.messages.append(el)

    @semaphore       
    def pop(self, el):
        if el in self.append:
            self.messages.remove(el)

    def __len__(self):
        return len(self.messages)

connections = Clients()
messages = MessageContainer()
newMessage = threading.Semaphore()
newMessage.acquire()

def check(conn, name):
    while 1:
        try:
            cur = conn.recv(20)
            messages.append(Msg(name, cur, "nescio"))
            newMessage.release()
        except:
            connections.pop(name)

def multiplexer():
    while 1:
        newMessage.acquire()
        if len(messages) > 0 and len(connections) > 1:
            for m in messages:
                for c in connections:
                    if c != m.getSender():
                        try:
                            connections.get(c).send(m.getMsg())
                        except:
                            connections.pop(name)

HOST = '0.0.0.0'
PORT = 8888
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print ("Error in socket")
        sys.exit()
    s.listen(10)
    print ("Listening for connections")
    
    listener = threading.Thread(target = multiplexer)
    listener.daemon = True
    listener.start()
    i = 0
    while 1:
        conn, addr = s.accept()
        connections.add(addr, conn)
        print("created new host at " + str(addr))
        t = threading.Thread(target = check, args = (conn, addr))
        t.daemon = True
        t.start()

    s.close()
    
if __name__ == "__main__":
    main()

'''
Created on Nov 1, 2013

@author: johannes
'''
import select
import random
import time
import SocketServer
import socket
import json
import threading
import sys, errno
from Network.Bonjour import Bonjour


class ZeroconfTcpServer():
    def __init__(self):
        self.host="0.0.0.0"
        self.name="robotMaze"
        self.regType='_maze._tcp'
        self.eventHandlers={}

    def initThreads(self):
        self.initTcp()    
        self.bonjour=Bonjour(self.name,self.regType,self.port)
        
    def start(self):
        self.tcpThread=threading.Thread(target=self.tcpServer.serve_forever)
        self.tcpThread.start()
        self.bonjour.runRegister()
        print("lol started everything")
        
        
    def stop(self):
        self.tcpServer.shutdown()
        self.bonjour.stopRegister()
    
    def addHandler(self,string,handler):
        self.eventHandlers[string]=handler
        
    def initTcp(self):
        class DebugTCPServer(SocketServer.TCPServer):
            def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, eventHandlers=None):
                #self.debug = debug
                self.eventHandlers=eventHandlers
                SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)
        
        class DebugMETCPHandler(SocketServer.BaseRequestHandler):
            def handle(self):
                # self.server is an instance of the DebugTCPServer
                try:
                    while True:
                        #data=self.request.recv(1024)      try:
                        data = json.loads(self.request.recv(1024).strip())
                        if data!=0:
                            func=self.server.eventHandlers.get(data.get("message"))
                            if func!=None:
                                response=func()
                                print("sending")
                                self.request.sendall(response)
                                print"delivered"
                except Exception:
                    pass

        while True:
            try:
                self.port=9000+random.randint(0,900)
                self.tcpServer = DebugTCPServer((self.host, self.port), DebugMETCPHandler, eventHandlers=self.eventHandlers)
                break
            finally:
                time.sleep(0.1)
        print ("got port "+str(self.port))

def printNumber():
    rint=random.randint(0,999)
    return json.dumps({'number':rint})


def printMaze():
    from collections import defaultdict
    d=defaultdict(dict)
    for i in range(10):
        for j in range(10):
            d[i][j]=(random.randint(1,7))
    print(str(d))
    print"finnished"
    return json.dumps(d)
    
def main():
    server=ZeroconfTcpServer()
    server.addHandler("number", printNumber)
    server.addHandler("maze", printMaze)
    
    server.initThreads()
    server.start()
    #server.addHandler("lol", printLol)
    try:
        print("running tcp and zeroconf")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
    
if __name__ == '__main__':
    main()
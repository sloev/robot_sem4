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
from Maze.Maze import Maze

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
                                response=func(data.get("params"))
                                print("sending")
                                self.request.sendall(response)
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

def receivePath(self,params=0):
    if self.Lock.is_set() or not params:
        returner= {'status':"error",'cause':"robot is busy"}
        return json.dumps(returner)
    else:
        print params
        returner= {'status':"success"}
        return json.dumps(returner)
        

def sendCurrentPosition(self,params=0):
    if self.Lock.is_set():
        returner ={'status':"error",'cause':"robot is busy"}
        return json.dumps(returner)
    else:
        currentPos=[0,0]
        returner= {'status':"success",'currentPosition':currentPos}
        return json.dumps(returner)
    
def printMaze(a=None):
    print "maze called"
    maze=Maze()
    maze.set(0,0,13)
    maze.set(1,0,11)
    maze.set(2,0,8)
    maze.set(3,0,12)
    maze.set(0,1,1)
    maze.set(1,1,10)
    maze.set(2,1,4)
    maze.set(3,1,5)
    maze.set(0,2,5)
    maze.set(1,2,11)
    maze.set(2,2,4)
    maze.set(3,2,5)
    maze.set(0,3,3)
    maze.set(1,3,10)
    maze.set(2,3,6)
    maze.set(3,3,7)




#     for y in range(10):
#         for x in range(5):
#             print("before random stuff")
#             north=random.randint(0,100)>90
#             east=random.randint(0,100)>90
#             south=random.randint(0,100)>90
#             west=random.randint(0,100)>90     
#             print("making value")
#             value=int((((north<<3) or (east <<2)) or (south <<1)) or west)
#             print str(value)    
#             maze.set(x, y, value)
    print(maze)
    currentPos=[0,0]
    print"finnished"
    mazeDict=maze.getDict()
    returner={'status':"success","currentpos":currentPos,"maze":mazeDict}
    return json.dumps(returner)
    
def main():
    server=ZeroconfTcpServer()
    server.addHandler("number", printNumber)
    server.addHandler("maze", printMaze)
    server.addHandler("path", printPath)
    server.addHandler("currentPosition", sendCurrentPosition)
    
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
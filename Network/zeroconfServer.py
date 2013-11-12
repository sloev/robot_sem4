'''
Created on Nov 1, 2013

@author: johannes
'''
import select
import random
import time
import SocketServer
import socket
import threading
from Network.Bonjour import Bonjour
from Network.EventHelpers import EventHookKeyValue


class zeroconfTcpServer():
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
        
#         class DebugMETCPHandler(SocketServer.BaseRequestHandler):
#             def handle(self):
#                 # self.server is an instance of the DebugTCPServer
#                 while True:
#                     #data=self.request.recv(1024)
#                     data = self.rfile.readline().strip()
#                     if data!=0:
#                         data = data.strip()
#                         string=self.server.eventHandlers.get(data)()
#                     #print ("{} wrote:".format(self.client_address[0])+" event="+str(self.server.eventHandlers.__class__.__name__))
#                         if string!=None:
#                             self.request.send(string)
#                         else:
#                             self.request.send("error: not in funcDict")
#                     else:
#                         break 
                    
        class DebugMETCPHandler(SocketServer.StreamRequestHandler):
            def handle(self):
                # self.server is an instance of the DebugTCPServer
                while True:
                    #data=self.request.recv(1024)
                    self.data = self.rfile.readline().strip()
                    if self.data!=0:
                        try:
                            string=self.server.eventHandlers.get(self.data)()
                            self.wfile.write(string)
                        except Exception:
                            self.wfile.write("error: not in funcDict")
                    else:
                        break 
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
    return "lol heres a number = "+str(rint)

def printMaze():
    string="here is a-maze-ing"
    return string
    
def main():
    server=zeroconfTcpServer()
    server.addHandler("lol", printNumber)
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
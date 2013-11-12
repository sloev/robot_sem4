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
        self.host="127.0.0.1"
        self.name="robotMaze"
        self.regType='_maze._tcp'
        self.eventHandler=EventHookKeyValue()


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
        self.eventHandler.add(string, handler)
        
    def initTcp(self):
        class DebugTCPServer(SocketServer.TCPServer):
            def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, eventHandler):#debug=True):
                #self.debug = debug
                self.eventHandler=eventHandler
                SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)
        
        class DebugMETCPHandler(SocketServer.BaseRequestHandler):
            def handle(self):
                # self.server is an instance of the DebugTCPServer
                self.data = self.request.recv(1024).strip()
                print("trying eventhandler")
                string=self.server.eventHandler.fire(self.data)
                print ("{} wrote:".format(self.client_address[0])+" event="+string)

                self.request.send("lol")
                    
        while True:
            try:
                self.port=9000+random.randint(0,900)
                self.tcpServer = DebugTCPServer((self.host, self.port), DebugMETCPHandler, debug=True)
                break
            finally:
                time.sleep(0.1)
        print ("got port "+str(self.port))
                
        

def printLol():
    rint=random.randint(0,999)
    print("received lol sending %d" % rint)
    return str(rint)
    
def main():
    server=zeroconfTcpServer()
    server.addHandler("lol", printLol)
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
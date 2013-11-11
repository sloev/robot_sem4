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
        while True:
            try:
                self.port=9000+random.randint(0,900)
                self.tcpServer = self.SimpleServer((self.host, self.port), self.SingleTCPHandler,self.eventHandler)
                break
            finally:
                time.sleep(0.1)
        print ("got port "+str(self.port))
    
    class SingleTCPHandler(SocketServer.StreamRequestHandler):

        def handle(self):
            # self.request is the client connection
            data = self.request.recv(1024)  # clip input at 1Kb
            string=self.server.eventHandler.get(str(data))
            #reply = pipe_command(my_unix_command, data)
            self.request.send("lol"+str(data))
            self.request.close()

    class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
        # Ctrl-C will cleanly kill all spawned threads
        daemon_threads = True
        # much faster rebinding
        allow_reuse_address = True
            
        def __init__(self, server_address, RequestHandlerClass,eventHandler):
            SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
    

def printLol():
    rint=random.randint(0,999)
    print("received lol sending %d" % rint)
    return str(rint)
    
def main():
    server=zeroconfTcpServer()
    server.addHandler("lol", printLol)
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
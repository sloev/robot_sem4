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
        self.name="robotMaze"
        self.regType='_maze._tcp'
        #self.address=address
        self.host= "127.0.0.1"
        self.initTcpServer()

        self.eventHandler=EventHookKeyValue()
      

    def startThreads(self):
        self.tcpServerThread = threading.Thread(target=self.tcpServer.serve_forever)
        self.tcpServerThread.start()

        self.registerThread=Bonjour(self.name,self.regType,self.port)
        self.registerThread.runBrowser()

    def close(self):
        self.tcpServer.shutdown()
        self.registerThread.stopRegister()
        print("closed tcpserver and zeroconf succesfully")
    
    def addHandler(self,string,handler):
        self.eventHandler.add(string, handler)
    
    class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
        daemon_threads = True
        allow_reuse_address = True

        def __init__(self, server_address, RequestHandlerClass):
            SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

    class MyTCPHandler(SocketServer.StreamRequestHandler):
        def handle(self):
            self.data = self.rfile.readline().strip()
            print "{} wrote:".format(self.client_address[0])
            print self.data
            string=self.eventHandler.fire(self.data)
            if(string!=None):
                self.wfile.write(self.data.upper())
    
    def initTcpServer(self):
        while True:
            try:
                self.port = 9000 + random.randint(0,999)
                self.tcpServer=self.SimpleServer((self.host, self.port), self.MyTCPHandler)
                print "%s: got port %s" % (self.name, self.port)
                break
            except IOError:
                print "%s: didn't get port %s" % (self.name, self.port)
        print "finnished init"
                

def printLol():
    rint=random.randint(0,999)
    print("received lol sending %d" % rint)
    return str(rint)
    
def main():
    server=zeroconfTcpServer()
    server.startThreads()
    #server.addHandler("lol", printLol)
    try:
        print("running tcp and zeroconf")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.close()
    
if __name__ == '__main__':
    main()
'''
Created on Nov 11, 2013

@author: johannes
'''

import random
import SocketServer
import socket
import threading

class TcpSocket():
    def __init__(self,host='127.0.0.1'):
        self.host=host
        self.initTcpServer()

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
        
    def startServer(self):
        self.tcpServerThread = threading.Thread(target=self.tcpServer.serve_forever)
        self.tcpServerThread.start()
        
    def startClient(self):
        self.clientSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.host,self.port))
        
    def closeClient(self):
        self.clientSocket.close()
        
    def closeServer(self):
        self.tcpServer.shutdown()
        print("closed tcpserver")
    
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

            self.wfile.write(self.data.upper())
            
    def send(self,string):
        self.clientSocket.send(string)    

def main():
    tcp=TcpSocket()
if __name__ == '__main__':
    pass
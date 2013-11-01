'''
Created on Nov 1, 2013

@author: johannes
'''
import pybonjour
import select
import random
import time
import SocketServer
import socket
import threading

class zeroconfTcpServer():
    def __init__(self):
        self.name="r-pi_robot_maze_socket"
        self.regType= '_maze._tcp'
        #self.address=address
        self.host='127.0.0.1'
        self.initTcpServer()
        self.tcpServerThread = threading.Thread(target=self.tcpServer.serve_forever).start()
        self.initBonjourServer()
            
    def close(self):
        self.tcpServer.shutdown()
        self.sdRef.close()
        print("closed tcpserver and zeroconf succesfully")
    
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
                
    def initBonjourServer(self):
        def register_callback(sdRef, flags, errorCode, name, regType, domain):
            if errorCode == pybonjour.kDNSServiceErr_NoError:
                print 'Registered service:'
                print '  name    =', name
                print '  regtype =', regType
                print '  domain  =', domain
        print"registering zeroconf"

        self.sdRef = pybonjour.DNSServiceRegister(name = self.name,
                                                  regtype = self.regType,
                                                  port = self.port,
                                                  callBack = register_callback)    
        ready = select.select([self.sdRef], [], [])
        if self.sdRef in ready[0]:
            print("first victim")
            pybonjour.DNSServiceProcessResult(self.sdRef)
            
    def makeClient(self):
        return self.tcpClient(self.host,self.port)
    
    class tcpClient():
        def __init__(self,host,port):
            self.host2=host
            self.port2=port
            self.socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.message = "lol"
    
        def __call__(self):
            self.socket2.connect((self.host2, self.port2))
            self.socket2.send(self.message)
            
def main():
    server=zeroconfTcpServer()
    try:
        client=server.makeClient()
        print("running tcp and zeroconf")
        while True:
            client()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    server.close()
    
if __name__ == '__main__':
    main()
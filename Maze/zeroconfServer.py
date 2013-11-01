'''
Created on Nov 1, 2013

@author: johannes
'''
import pybonjour
import select
import random
import time
import SocketServer

class zeroconfTcpServer():
    def __init__(self):
        self.name="r-pi_robot_maze_socket"
        self.regType= '_maze._tcp'
        #self.address=address
        self.host='127.0.0.1'
        
        self.initTcpServer()
        print "lol"
        #self.initBonjourServer()
            
    def close(self):
        self.tcpServer.shutdown()

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
                self.tcpServer = SocketServer.TCPServer((self.host, self.port), self.MyTCPHandler)
                print "%s: got port %s" % (self.name, self.port)
                break
            except IOError:
                print "%s: didn't get port %s" % (self.name, self.port)
        
        self.tcpServer.serve_forever()

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
    
def main():
    server=zeroconfTcpServer()
    index=0
    while index < 20:
        time.sleep(1)
        print "running for "+str(index)+" seconds"
        index=index+1
    server.close()
    
if __name__ == '__main__':
    main()
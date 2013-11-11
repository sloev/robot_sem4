'''
Created on Nov 6, 2013

@author: johannes
'''
import select
import sys
import pybonjour
import socket
import time
import threading
from EventHelpers import EventHook

class Client():
    def __init__(self):
        self.serviceName = None
        self.hostname = None
        self.ip = None
        self.port = None
        self.fullName=None
        self.regType=None
        self.resolved = False

    def __str__(self):
        string = "\nservice name: \t%s\n" % self.serviceName
        string += "host name:    \t%s\n" % self.hostname
        string += "full name:    \t%s\n" % self.fullname
        string += "ip:          \t%s\n" % self.ip
        string += "port:        \t%s\n" % self.port
        string += "regtype:        \t%s\n" % self.regType
        return string
    
class Bonjour():
    def __init__(self,name,regtype,port=None):
        self.name=name
        self.regtype=regtype
        self.port=port
        
        self.browserQueried  = []
        self.browserResolved = []
        
        self.browserLock=threading.Lock()
        self.timeout  = 5

        self.registerStopEvent = threading.Event()
        self.browserStopEvent = threading.Event()
        
        self.clients = dict()
        self.currentClient=Client()
        
        self.clientEventHandler=EventHook()
        
    def addClientEventHandler(self,fnc):
        self.clientEventHandler += fnc
    
    def removeClientEventHandler(self,fnc):
        self.clientEventHandler -= fnc
    
    def runRegister(self):
        self.registerStopEvent.clear()
        self.registerThread=threading.Thread(target=self.register)
        self.registerThread.start()
        
    def stopRegister(self):
        self.registerStopEvent.set()
        self.registerThread.join()

    def runBrowser(self):
        self.browserStopEvent.clear()
        self.browserThread=threading.Thread(target=self.browser)
        self.browserThread.start()
        
    def stopBrowser(self):
        self.browserStopEvent.set()
        self.browserThread.join()
    
    def register(self):
        def register_callback(sdRef, flags, errorCode, name, regtype, domain):
            if errorCode == pybonjour.kDNSServiceErr_NoError:
                print 'Registered service:'
                print '  name    =', name
                print '  regtype =', regtype
                print '  domain  =', domain
        
        
        sdRef = pybonjour.DNSServiceRegister(name = self.name,
                                             regtype = self.regtype,
                                             port = self.port,
                                             callBack = register_callback)
        
        try:
            while not self.registerStopEvent.is_set():
                ready = select.select([sdRef], [], [],self.timeout*2)
                if sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(sdRef)
#                self.regStopEvent.wait(0.01)
        finally:
            sdRef.close()
        print("exiting register thread")
        
    def browser(self):
        def query_record_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                                  rrtype, rrclass, rdata, ttl):
            if errorCode == pybonjour.kDNSServiceErr_NoError:
                with self.browserLock:
                    self.currentClient.ip=socket.inet_ntoa(rdata)
                    self.currentClient.resolved=True
                    self.currentClient.fullName=fullname
                self.browserQueried.append(True)
        
        
        def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                             hosttarget, port, txtRecord):
            if errorCode != pybonjour.kDNSServiceErr_NoError:
                return
            with self.browserLock:
                self.currentClient.fullname=fullname
                self.currentClient.port=port
                self.currentClient.hostname=hosttarget.decode('utf-8')

            query_sdRef = \
                pybonjour.DNSServiceQueryRecord(interfaceIndex = interfaceIndex,
                                                fullname = hosttarget,
                                                rrtype = pybonjour.kDNSServiceType_A,
                                                callBack = query_record_callback)

            try:
                while not self.browserQueried:
                    ready = select.select([query_sdRef], [], [], self.timeout)
                    if query_sdRef not in ready[0]:
                        print 'Query record timed out'
                        break
                    pybonjour.DNSServiceProcessResult(query_sdRef)
                else:
                    self.browserQueried.pop()
            finally:
                query_sdRef.close()
        
            self.browserResolved.append(True)
        
        
        def browse_callback(sdRef, flags, interfaceIndex, errorCode, serviceName,
                            regtype, replyDomain):
            if errorCode != pybonjour.kDNSServiceErr_NoError:
                return
        
            if not (flags & pybonjour.kDNSServiceFlagsAdd):
                with self.browserLock:
                    if self.clients.has_key(serviceName):
                        print("client exists to be removed= "+str(serviceName))
                        self.clients.pop(serviceName)
                        self.clientEventHandler.fire(self.clients)
                #print 'Service removed'
                return
            #print 'Service added; resolving'
            with self.browserLock:
                self.currentClient=Client()
                self.currentClient.serviceName=serviceName
            resolve_sdRef = pybonjour.DNSServiceResolve(0,
                                                        interfaceIndex,
                                                        serviceName,
                                                        regtype,
                                                        replyDomain,
                                                        resolve_callback)
       
            try:
                while not self.browserResolved:
                    ready = select.select([resolve_sdRef], [], [], self.timeout)
                    if resolve_sdRef not in ready[0]:
                        print 'Resolve timed out'
                        break
                    pybonjour.DNSServiceProcessResult(resolve_sdRef)
                else:
                    with self.browserLock:
                        
                        if not self.clients.has_key(serviceName) and self.currentClient.resolved:
                            print("ading client="+str(serviceName))
                            self.currentClient.regType=regtype
                            #print(self.currentClient)
                            self.clients[serviceName] = self.currentClient
                            self.clientEventHandler.fire(self.clients)
                    self.browserResolved.pop()
                    
            finally:
                resolve_sdRef.close()
        
        
        browse_sdRef = pybonjour.DNSServiceBrowse(regtype = self.regtype,
                                                  callBack = browse_callback)
        
        try:
            while not self.browserStopEvent.is_set():
                ready = select.select([browse_sdRef], [], [],self.timeout)
                if browse_sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(browse_sdRef)
        finally:
            browse_sdRef.close()
        print("exiting browser thread")
        
    def printClients(self):
        with self.browserLock:
            for client in self.clients.itervalues():
                print(client)
                
    def getFirstClient(self):
        if len(self.clients)>0:
            return self.clients.get(self.clients.keys()[0])
        return None

def printEvent(args,args2):
    print("args="+str(args)+"\n"+str(args2))
    
def main():
    name="oscTestServer"
    port=9027
    regtype='_osc._udp'
    
    a=Bonjour(name,regtype,port)
    b=Bonjour(name,regtype,port)
    b.addClientEventHandler(printEvent)
    
    b.runBrowser()
    time.sleep(3)
    print("starting bonjour register")
    a.runRegister()
    try :
        while 1 :
            time.sleep(2)
    except KeyboardInterrupt :
        a.stopRegister()
        print("exiting")
        b.stopBrowser()        

    
if __name__ == '__main__':
    main()




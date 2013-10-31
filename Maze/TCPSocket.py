'''
Created on 14/10/2013

@author: Daniel Machon
'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'This class is used to send the mapped maze using the TCP protocol,    '
'to a server, that will then handle the data and draw the maze.        '
'Before sending any data, a "serverDisover" will be made, to determine '
'if any servers are present on the local subnet                        '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


import socket

IP = "127.0.0.1"
PORT = 5001
BUFFER = 1024


class TCPSocket():
 
    '''
       Constructor
    '''
    def __init__(self, message):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message = message
        
    
    '''
        Makes the object callable
    '''
    def __call__(self):
        self.serverDiscover(5001)
        self.socket.connect((IP, PORT))
        self.socket.send(self.message)
        #self.response = self.socket.recv(BUFFER)

    
    '''
        Socket clean-up
    '''
    def __del__(self):
        self.socket.close()
        self.BCsocket.close()
        del self.socket, self.BCsocket
        
    
    '''
        Broadcast on the local subnet to detect if any server
        is present. The server will reply with it's IP address
    ''' 
    def __serverDiscover(self, port):
        self.BCsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.BCsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        self.BCsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.BCsocket.bind(('0.0.0.0', port))
        self.addr = '255.255.255.255', port
        assert self.BCsocket.sendto('Discover', self.addr) == len('Discover')
        
        while True:
            serverInfo = ""
            serverInfo = self.BCsocket.recvfrom(64)
            if(serverInfo!=None):
                break
            
        IP = serverInfo
            
    
    '''
        Set socket timeouts
    '''
    def __setSocketTimeout(self, timeout):
        self.socket.settimeout(timeout)
        self.BCsocket.settimeout(timeout)
        
        
    '''
        Get response from the server. Is used to check if the server
        has received and understood the data
    '''
    def checkResponse(self, response):
        if(self.response == "OK"):
            pass
        else:
            self()
        
        
def main():
    test = TCPSocket("LoL")
    test()
        

if __name__ == '__main__':
    main()
        
        
        
'''
Created on 14/10/2013

@author: danielmachon
'''

import socket

IP = "192.168.1.2"
PORT = 5000
BUFFER = 1024


class TCPSocket():
 

    def __init__(self, message):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(IP, PORT)
        self.message = message
        
    def __call__(self):
        self.socket.send(self.message)
        self.response = self.socket.recv(BUFFER)
        self.checkResponse(self.response)
        
    def __del__(self):
        self.socket.close()
        del self.socket
 
    def checkResponse(self, response):
        if(self.response == "OK"):
            continue
        else:
            self.__call__()
        
        
def main():
    pass

if __name__ == '__main__':
    main()
        
        
        
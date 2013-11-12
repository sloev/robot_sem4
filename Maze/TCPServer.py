'''
Created on 31/10/2013

@author: danielmachon
'''

import socket

IP = '127.0.0.1'
PORT = 5001
BUFFER = 64

class TCPServer():  


    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((IP, PORT))
        self.server.listen(1)
    
    def __call__(self):
        conn, addr = self.server.accept()
        while True:
            data = conn.recv(BUFFER)
            print data
        conn.close()
        
def main():
    test = TCPServer()
    test()
    
if __name__ == '__main__':
    main()
        
        
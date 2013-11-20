'''
Created on Nov 11, 2013

@author: johannesbent
'''
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import QObject, pyqtSignal
import time
from Network.Bonjour import Bonjour
import socket
import json
from Maze.Maze import Maze
from MazeView import MazeView

class MainGui(QtGui.QMainWindow):
    mitSignal = pyqtSignal(str, int, name='mitSignal')

    def __init__(self):
        
        super(MainGui, self).__init__()
        self.initUI()

    def initUI(self):
        self.mazeView=MazeView()
        name="robotMaze"
        regtype='_maze._tcp'
        
        self.address=None
        self.browser=Bonjour(name,regtype)
        self.browser.runBrowser()
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
        self.mitSignal.connect(self.updateIp)

        closeAction = QtGui.QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Notepad')
        closeAction.triggered.connect(self.close)
    
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(closeAction)
    
        self.setGeometry(300,300,300,50) 
        self.setWindowTitle('LUL') 
        self.browser.addClientEventHandler(self.mitSignal.emit)  
        
        self.rpiLabel = QtGui.QLabel("Not connected to r-pi",self)
        self.rpiLabel.move(5,5)
        self.rpiLabel.resize(self.rpiLabel.sizeHint())
        self.rpiLabel.show()
        
        self.getMaze = QtGui.QPushButton('getMaze', self)
        self.getMaze.clicked.connect(self.clientSendMaze)
        self.getMaze.resize(self.getMaze.sizeHint())
        self.getMaze.move(0, 20)
        self.getMaze.setEnabled(False)    
        self.show()

    def closeEvent(self,event):
        self.browser.stopBrowser()
        self.mazeView.close()
        event.accept() 
    
    def updateIp(self,ip,port):
        if self.address==(ip,port):
            self.closeTcpClient()
            self.address=None
            self.getMaze.setEnabled(False)    
            self.rpiLabel.setText("Not connected to r-pi")
            self.rpiLabel.resize(self.rpiLabel.sizeHint())
            print("r-pi removed and clientSocket closed with ip="+str(ip)+" port="+str(port))
        else:
            print("r-pi catched with address"+str((ip,port)))
            
            reply = QtGui.QMessageBox.question(self, 'question',"rpi detected\nwanna update ip/port?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                print("old ip and port="+str(self.address))
                self.address=(str(ip),port)
                print("new ip and port="+str(self.address)+"\n")
                self.getMaze.setEnabled(True)    
                self.rpiLabel.setText("Connected to "+str(self.address))
                self.rpiLabel.resize(self.rpiLabel.sizeHint())
            else:
                pass
        
    def clientSendNumber(self):
        self.clientSend("number")
    
    def clientSendMaze(self):
        data = {'message':"maze"}
        print"maze called"
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect(self.address)
        self.clientSocket.send(json.dumps(data))
        data = self.clientSocket.recv(16384)  # limit reply to 16K
        self.clientSocket.close()
        print("closed socket")
        
        received = json.loads(data)
        currentPos=received["currentpos"]
        maze=Maze(received["maze"])
        self.mazeView=MazeView(maze,currentPos)
        self.mazeView.repaint()
        self.mazeView.show()
        
        print maze
        
    def clientSend(self,string):
        received="nothing received"
        data = {'message':string, 'test':123.4}
        try:
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientSocket.connect(self.address)
            self.clientSocket.send(json.dumps(data))
            received = json.loads(self.clientSocket.recv(1024))
        finally:
            tmp=received.get(string)
            if tmp!=None:
                print tmp
            else:
                print received
    
    def closeTcpClient(self):
        try:
            self.clientSocket.close()
            print("closed client")
        finally:
            pass   
        
def main():
    app = QtGui.QApplication(sys.argv)
    gui = MainGui()
    sys.exit(app.exec_())
        

if __name__ == '__main__':
    main()


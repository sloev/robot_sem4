'''
Created on Nov 11, 2013

@author: johannes
'''
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4 import QtCore
import time
from Network import Bonjour
import socket


class MainGui(QtGui.QMainWindow):
    mitSignal = pyqtSignal(str, int, name='mitSignal')

    def __init__(self):
        
        super(MainGui, self).__init__()
        self.initUI()

    def initUI(self):
        name="robotMaze"
        regtype='_maze._tcp'
                
        self.browser=Bonjour(name,regtype)
        self.browser.runBrowser()
        
        self.mitSignal.connect(self.updateIp)

        closeAction = QtGui.QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Notepad')
        closeAction.triggered.connect(self.closeEvent)
    
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(closeAction)
    
        self.setGeometry(300,300,300,300) 
        self.setWindowTitle('LUL') 
        self.show()
        self.browser.addClientEventHandler(self.mitSignal.emit)

    def closeEvent(self,event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.browser.stopBrowser()
            event.accept()
        else:
            event.ignore()    
    
    def updateIp(self,ip,port):
        (oldIp,oldPort)=self.clientSocket.getsockname()
        if oldIp==ip and oldPort==port:
            self.closeTcpClient()
            print("r-pi removed and clientSocket closed with ip="+str(ip)+" port="+str(port))
        else:
            print("r-pi catched with ip="+str(ip)+" port="+str(port))
            
        reply = QtGui.QMessageBox.question(self, 'question',"rpi detected\nwanna update ip/port?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            print("old ip and port="+str(self.ip)+" "+str(self.port))
            self.initTcpClient(ip,port)
            print("new ip and port="+str(self.ip)+" "+str(self.port))
        else:
            pass
        
    def initClient(self, address):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect(address)
    
    def closeTcpClient(self):
        self.clientSocket.close()
    
    def clientSend(self,string):
        self.clientSocket.send(string)

def main():
    app = QtGui.QApplication(sys.argv)
    gui = MainGui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


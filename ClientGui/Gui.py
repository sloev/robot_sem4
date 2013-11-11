'''
Created on Nov 11, 2013

@author: johannes
'''
import sys
from PyQt4 import *

import time
from Network.Bonjour import Bonjour

class MainGui(QMainWindow):
    def __init__(self):
        super(MainGui, self).__init__()
        self.initUI()

    def initUI(self):
        name="robotMaze"
        regtype='_maze._tcp'
        
        self.ip=None
        self.port=None
        self.newIpPort=[None,None]
        
        self.browser=Bonjour(name,regtype)
        self.browser.runBrowser()
        self.browser.addClientEventHandler(self.lol)
        
        self.mitSignal = pyqtSignal(str, int, name='mitSignal')
        self.mitSignal.connect(self.updateServerList(str,int))
        ###
        ###
        
        closeAction = QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Notepad')
        closeAction.triggered.connect(self.closeEvent)
    
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(closeAction)
    
        self.setGeometry(300,300,300,300) 
        self.setWindowTitle('LUL') 
        self.show()
        
    def lol(self,args=None,args2=None):
        if len(args)>0:
            args=args.get(args.keys()[0])
            print("ip="+str(args.ip)+" port="+str(args.port))
            if args.ip!=self.ip or args.port!=self.port:
                self.mitSignal.emit(args.ip, args.port)

    def closeEvent(self,event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.browser.stopBrowser()
            event.accept()
        else:
            event.ignore()    
    
    def updateServerList(self,ip,port):
        try:
            print(str(ip)+" lol "+str(port))
        finally:
            pass
        reply = QMessageBox.question(self, 'Message',"Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            pass         
        else:
            pass
def main():
    
    app = QApplication(sys.argv)
    gui = MainGui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


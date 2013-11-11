'''
Created on Nov 11, 2013

@author: johannes
'''
import sys
from PyQt4 import QtGui
import time
from Network.Bonjour import Bonjour

class MainGui(QtGui.QMainWindow):
    def __init__(self):
        super(MainGui, self).__init__()
        self.initUI()

    def initUI(self):
        name="robotMaze"
        regtype='_maze._tcp'
        
        self.ip=None
        self.port=None
        
        self.browser=Bonjour(name,regtype)
        self.browser.runBrowser()
        self.browser.addClientEventHandler(self.updateServerList)
        ###
        ###
        
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
        
    def closeEvent(self,event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.browser.stopBrowser()
            event.accept()
        else:
            event.ignore()    
    
    def updateServerList(self,args=None,args2=None):
        print("event fired from bonjour browser")
        if len(args)>0:
            args=args.get(args.keys()[0])
            print("ip="+str(args.ip)+" port="+str(args.port))
            if args.ip!=self.ip or args.port!=self.port:
                self.ip=args.ip
                self.port=args.port

                self.QMessageBox.about(self, "")
                
def main():
    
    app = QtGui.QApplication(sys.argv)
    gui = MainGui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


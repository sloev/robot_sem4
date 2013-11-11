'''
Created on Nov 11, 2013

@author: johannes
'''
import sys
from PyQt4 import QtGui
import time
from Network.Bonjour import Bonjour
    
class Gui(QtGui.QWidget):
    
    def __init__(self):
        super(Gui, self).__init__()
        self.initUI()
        
    def initUI(self):
        name="robotMaze"
        regtype='_maze._tcp'
        


        self.ip=None
        self.port=None
        
        self.b=Bonjour(name,regtype)
        self.b.runBrowser()
        self.b.addClientEventHandler(self.updateServerList)
        
        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('Simple')
        self.show()
        

        
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.b.stopBrowser()
            event.accept()
        else:
            event.ignore()        
            
    def dialog(self):
        reply = QtGui.QMessageBox.question(self, 'question',
                    "update ip/port?", QtGui.QMessageBox.Yes | 
                    QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:
            return True
        else:
            return False
    

    def updateServerList(self,args=None,args2=None):
        print("event fired from bonjour browser")
        if len(args)>0:
            args=args.get(args.keys()[0])
            print("ip="+str(args.ip)+" port="+str(args.port))
            if args.ip!=self.ip or args.port!=self.port:
                self.ip=args.ip
                self.port=args.port

            
def main():
    app = QtGui.QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_()) 

     
if __name__ == '__main__':
    main()
        
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
        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('Simple')
        self.show()
        
        name="robotMaze"
        regtype='_maze._tcp'
        
        self.b=Bonjour(name,regtype)
        self.b.runBrowser()
        
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.b.stopBrowser()
            event.accept()
        else:
            event.ignore()        
            
    def waitForService(self): 
        c=None
        while(c==None):
            c=self.b.getFirstClient()            
            time.sleep(1)    
        print("got first service")
        while 1:
            time.sleep(4)
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    ex.waitForService()

    sys.exit(app.exec_())

     
if __name__ == '__main__':
    main()
        
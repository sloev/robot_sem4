'''
Created on Nov 13, 2013

@author: johannes
'''
from PyQt4 import QtGui,QtCore

from Maze.Maze import Maze
from Maze.Astar import Astar

class MazeView(QtGui.QWidget):
    def __init__(self,maze=None):
        self.target=[0,0]
        self.source=self.target
        self.path=None
        
        self.mode=-1
        if(maze!=None):
            self.mazeModel=maze
            QtGui.QWidget.__init__(self)
            self.modelWidth = self.mazeModel.getWidth()
            self.modelHeight = self.mazeModel.getHeight()
            self.boxsize = 50
            self.width=self.modelWidth * self.boxsize + 10
            self.height=self.modelHeight * self.boxsize + 40
            self.setFixedSize(self.width, self.height)
            
            self.modeButton = QtGui.QPushButton('select and make path', self)
            self.modeButton.clicked.connect(self.modeChange)
            self.modeButton.resize(self.modeButton.sizeHint())
            self.modeButton.move(0, 0)    
        
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        b=self.boxsize
        qp.fillRect(0, 30, self.modelWidth * b + 10, self.modelHeight * b + 30, QtGui.QColor(0, 0, 0))
        qp.translate(QtCore.QPointF(5.5, 35.5))
        qp.setPen(QtGui.QColor(255, 255, 255))
        qp.drawRect(0,0,self.modelWidth * b,self.modelHeight * b)

        for y in range(self.modelHeight):
            for x in range(self.modelWidth):
                cell=self.mazeModel.get(x,y)
                if(cell & 0b1000) >>3:
                    qp.drawLine(x*b, y*b, (x+1)*b, y*b)
                if cell & 0b0001:
                    qp.drawLine(x*b, y*b, x*b, (y+1)*b)
        qp.setPen(QtGui.QColor(255, 255, 0))
        if self.path!=None:
            lastN=None
            for n in self.path.getPath():
                if lastN!=None:
                    x=n.x
                    y=n.y
                    qp.drawLine(lastN.x*b+(b/2), lastN.y*b+(b/2), n.x*b+(b/2), n.y*b+(b/2))
                lastN=n
        if self.mode!=-1:
            qp.setBrush(QtGui.QColor(255, 0, 0))
            p1=QtCore.QPointF(int(self.source[0]*self.boxsize+self.boxsize/2),int(self.source[1]*self.boxsize+30-self.boxsize/8))
            qp.drawEllipse(p1,self.boxsize/4,self.boxsize/4)
            qp.setBrush(QtGui.QColor(0, 255, 0))
            p2=QtCore.QPointF(int(self.target[0]*self.boxsize+self.boxsize/2),int(self.target[1]*self.boxsize+30-self.boxsize/8))
            qp.drawEllipse(p2,self.boxsize/4,self.boxsize/4)
        qp.end()
        
    def mouseReleaseEvent(self, event):
        if self.mode==1:
            self.path=None
            self.source=self.cordToCord([event.x(),event.y()])
            self.mode=2
        elif self.mode==2:
            self.target=self.cordToCord([event.x(),event.y()])
            self.modeButton.setEnabled(True)
            self.mode=0
            self.findPath()
        print("source="+str(self.source)+"target="+str(self.target))   
        self.repaint()
          
    def cordToCord(self,cord):
        value=[0,0]
        if cord[0]>5.5 and cord[0]<self.width-5.5 and cord[1]>35.5 and cord[1]<self.height-5.5: 
            for x in range(self.modelWidth):
                tmpx=x*self.boxsize+5.5
                if cord[0]>=tmpx:
                    value[0]=x
                else:
                    break
            for y in range(self.height):
                tmpy=y*self.boxsize+35.5
                if cord[1]>=tmpy:
                    value[1]=y
                else:
                    break        
        return value
    
    def modeChange(self):
        self.modeButton.setEnabled(False)
        self.mode=1
        
    def findPath(self):
        astar=Astar(self.mazeModel)
        path=astar.search(self.source,self.target)
        print"made astar"
        if path ==None:
            print "no path"
        else:
            print path
            self.path=path
        self.repaint()
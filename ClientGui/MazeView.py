'''
Created on Nov 13, 2013

@author: johannes
'''
from PyQt4 import QtGui,QtCore

from Maze.Maze import Maze
from Maze.Dijkstra import Dijkstra
import socket
import json

class MazeView(QtGui.QWidget):
    def __init__(self,maze=None,currentPos=None,address=None):
        self.address=address
        self.target=[0,0]
        self.source=currentPos
        self.path=None
        self.visited=None
        self.mode=-1
        if(maze!=None):
            self.mazeModel=maze
            QtGui.QWidget.__init__(self)
            self.modelWidth = self.mazeModel.getWidth()
            self.modelHeight = self.mazeModel.getHeight()
            self.boxsize = 50
            self.width=self.modelWidth * self.boxsize + 10
            if self.width<400:
                self.boxsize=(400-10)/self.modelWidth
                self.width=self.modelWidth * self.boxsize + 10
                self.height=self.modelHeight * self.boxsize + 40               
                
            self.setFixedSize(self.width, self.height)
            
            self.modeButton = QtGui.QPushButton('select and make path', self)
            self.modeButton.clicked.connect(self.modeChange)
            self.modeButton.resize(self.modeButton.sizeHint())
            self.modeButton.move(0, 0)    
            

            self.sendPath = QtGui.QPushButton('sendPath', self)
            self.sendPath.clicked.connect(self.clientSendPath)
            self.sendPath.resize(self.sendPath.sizeHint())
            self.sendPath.move(self.width-self.sendPath.sizeHint().width(), 0)
            self.sendPath.setEnabled(False)    

            self.receiveCurrentPos = QtGui.QPushButton('getCurrentPosition', self)
            self.receiveCurrentPos.clicked.connect(self.getCurrentPosition)
            self.receiveCurrentPos.resize(self.receiveCurrentPos.sizeHint())
            self.receiveCurrentPos.move(self.width-self.receiveCurrentPos.sizeHint().width()-self.sendPath.sizeHint().width()-5, 0)
            self.receiveCurrentPos.setEnabled(False)    
            
            self.dijkstra=Dijkstra(self.mazeModel)

                    
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing) 

        b=self.boxsize
        qp.fillRect(0, 30, self.modelWidth * b + 10, self.modelHeight * b + 30, QtGui.QColor(0, 0, 0))
        qp.translate(QtCore.QPointF(5.5, 35.5))
        pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        pen.setCapStyle(QtCore.Qt.RoundCap);
        pen.setJoinStyle(QtCore.Qt.RoundJoin);

        qp.setPen(pen)
        qp.drawRect(0,0,self.modelWidth * b,self.modelHeight * b)

        for y in range(self.modelHeight):
            for x in range(self.modelWidth):
                cell=self.mazeModel.get(x,y)
                if(cell & 0b1000) >>3:
                    qp.drawLine(x*b, y*b, (x+1)*b, y*b)
                if cell & 0b0001:
                    qp.drawLine(x*b, y*b, x*b, (y+1)*b)
                if(cell & 0b0010) >>1:
                    qp.drawLine(x*b, (y+1)*b, (x+1)*b, (y+1)*b)
                if (cell & 0b0100) >>2:
                    qp.drawLine((x+1)*b, y*b, (x+1)*b, (y+1)*b)
        #qp.setPen(QtGui.QColor(0, 255, 255))
        qp.setPen(QtCore.Qt.NoPen)

        if self.visited!=None:
            inc=255/len(self.visited)
            i=0
            for n in self.visited:
                qp.setBrush(QtGui.QColor(255-inc*i,inc*i ,0))
                p1=QtCore.QPointF(n.x*b+(b/2), n.y*b+(b/2))
                qp.drawEllipse(p1,self.boxsize/10,self.boxsize/10)
                i+=1
        lastN=None
        if self.path!=None:
            pen.setStyle(QtCore.Qt.DotLine)
            pen.setColor(QtGui.QColor(255,255,0))
            pen.setWidth(3)
            #pen.setWidth(3);
            qp.setPen(pen)
            
            for n in self.path.getPath():
                if lastN!=None:
                    x=n.x
                    y=n.y
                    qp.drawLine(lastN.x*b+(b/2), lastN.y*b+(b/2), n.x*b+(b/2), n.y*b+(b/2))
                lastN=n
        if self.mode!=-1:
            qp.setPen(QtCore.Qt.NoPen)
     

            qp.setBrush(QtGui.QColor(255, 0, 0))
            qp.setFont(QtGui.QFont('Arialblack', 20))

            p1=QtCore.QPointF(self.source[0]*b+(b/2), self.source[1]*b+(b/2))
            p2=QtCore.QPointF(self.target[0]*b+(b/2), self.target[1]*b+(b/2))
            qp.drawEllipse(p1,self.boxsize/4,self.boxsize/4)
            
            qp.setBrush(QtGui.QColor(0, 255, 0))
            qp.drawEllipse(p2,self.boxsize/4,self.boxsize/4)
            qp.setPen(QtCore.Qt.black)
            qp.drawText(p1.x()-10,p1.y()-5,20,20,QtCore.Qt.AlignCenter,"S")
            qp.drawText(p2.x()-10,p2.y()-5,20,20,QtCore.Qt.AlignCenter,"T")
        qp.end()
        
    def mouseReleaseEvent(self, event):
        if self.mode==9:
            self.path=None
            self.source=self.cordToCord([event.x(),event.y()])
            self.mode=2
        elif self.mode==1:
            self.target=self.cordToCord([event.x(),event.y()])
            self.modeButton.setEnabled(True)
            self.mode=0
            print("source="+str(self.source)+"target="+str(self.target))   
            self.findPath()
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
        
    def clientSendPath(self):
        stack= self.path.pathToStack()

        data = {'message':"path","params":stack}
        print"sending path:\n"+str(stack)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect(self.address)
        self.clientSocket.send(json.dumps(data))
        data = self.clientSocket.recv(16384)  # limit reply to 16K
        
        received = json.loads(data)
        status=received.get("status")
        if status=="error":
            print "error: "+received.get("cause")
        else:
            print status        
        self.clientSocket.close()
        self.receiveCurrentPos.setEnabled(True)
        self.sendPath.setEnabled(False)        
        self.modeButton.setEnabled(False)
        print "closed socket"
        
    def getCurrentPosition(self):
        data = {'message':"currentPosition"}
        print"getting currentposition"
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect(self.address)
        self.clientSocket.send(json.dumps(data))
        data = self.clientSocket.recv(16384)  # limit reply to 16K
        
        received = json.loads(data)
        status=received.get("status")
        if status=="error":
            print "error: "+received.get("cause")
        else:
            print status   
            tmp=received.get("currentPosition")
            self.source =[ tmp[str(0)],tmp[str(1)] ]
            print "source="+str(self.source)
            self.receiveCurrentPos.setEnabled(False)
            self.modeButton.setEnabled(True)     
        self.clientSocket.close()
        print "closed socket"
        
    def findPath(self):
        pathTuple=self.dijkstra.search(self.source,self.target)
        path=pathTuple[0]

        print"made astar"
        if path ==None:
            print "no path"
        else:
            print"all paths the same="
            print path
            self.path=path
        self.visited=pathTuple[1]
        self.sendPath.setEnabled(True)    
        self.repaint()
        
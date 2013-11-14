'''
Created on Nov 13, 2013

@author: johannes
'''
from PyQt4 import QtGui,QtCore

from Maze.Maze import Maze

class MazeView(QtGui.QWidget):
    def __init__(self,maze=None):
        if(maze!=None):
            self.mazeModel=maze
            QtGui.QWidget.__init__(self)
            self.modelWidth = self.mazeModel.getWidth()
            self.modelHeight = self.mazeModel.getHeight()
            self.boxsize = 30
            self.setFixedSize(self.modelWidth * self.boxsize + 10, self.modelHeight * self.boxsize + 10)
        
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        b=self.boxsize
        qp.fillRect(0, 0, self.modelWidth * b + 10, self.modelHeight * b + 10, QtGui.QColor(0, 0, 0))
        qp.translate(QtCore.QPointF(5.5, 5.5))
        qp.setPen(QtGui.QColor(255, 0, 0))
        qp.drawRect(0,0,self.modelWidth * b,self.modelHeight * b)

        for y in range(self.modelHeight):
            for x in range(self.modelWidth):
                cell=self.mazeModel.get(x,y)
                if(cell & 0b1000) >>3:
                    qp.drawLine(x*b, y*b, (x+1)*b, y*b)
                if cell & 0b0001:
                    qp.drawLine(x*b, y*b, x*b, (y+1)*b)
        qp.end()

        
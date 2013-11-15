'''
Created on Nov 15, 2013

@author: johannes
'''
from Maze import Maze

class Mapping():
    '''
    classdocs
    '''
    stepsPrCell=6018

    def __init__(self):
        '''
        Constructor
        '''
        self.maze=Maze()
        self.globalCompass=[0,1,2,3]#north/east/south/west
        self.direction=self.globalCompass[2]#south
        
        self.startPosition=[0,0]
        self.startDirection=[0,0]
        
        self.currentPosition=[0,0]#x,y
        self.lastPosition=[0,0]
        self.funcDict={0:self.subY, 1:self.addX, 2:self.addY, 3:self.subX}
        self.stack=[]
        '''
        table:
        0,0 -------------- x,0
        |
        |
        |
        |
        |
        |
        0,y
        '''
        
    def stepsToCells(self,steps):
        return int(steps/self.stepsPrCell)
    
    def wallsToInt(self,walls):
        north=0
        east=0
        south=0
        west=0
        if(self.startDirection==self.direction and self.startPosition == self.currentPosition):
            north=1
            east=walls[0]
            south=walls[2]
            west=walls[1]
        else:
            if(self.direction==0):#north
                west=walls[0]
                east=walls[1]
                south=0
                north=walls[2]
            elif(self.direction==1):#east
                west=0
                east=walls[2]
                south=walls[1]
                north=walls[0]
            elif(self.direction==2):#south
                west=walls[1]
                east=walls[0]
                south=walls[2]
                north=0
            else:#west
                west=walls[2]
                east=0
                south=walls[0]
                north=walls[1]
        return [north,east,south,west]
                
    def getChoice(self,steps,walls):
        cells=self.stepsPrCell(steps)
        func=self.funcDict[self.direction]
        dX=abs(self.currentPosition[0]-self.lastPosition[0])
        dY=abs(self.currentPosition[1]-self.lastPosition[1])
        dI=dY if dY!=0 else dX
        
        x=self.lastPosition[0]
        y=self.lastPosition[1]
        
        walls=self.wallsToInt(walls)
        for i in range(dI):
            self.maze.set(x, y, walls)
            tmp=func(x,y)
            x=tmp[0]
            y=tmp[1]
        self.currentPosition=[x,y]
        posibilities=self.findPossibilities(self.currentPosition)
        if not posibilities:
            choice=self.stack.pop()
        else:
            choice=self.makeChoice(posibilities)
        self.lastPosition=self.currentPosition      
        self.direction=choice[0]
        self.stack.append(choice[1])
        return choice[2]
        
    def findPossibilities(self,pos):
        posibilities=[0,1,2,3]
        for i in range(4):
            xy=self.funcDict(i)(pos[0],pos[1])
            tmp=self.maze.get(xy[0], xy[1])
            if(tmp!=None):
                posibilities.pop(i)
        return posibilities
        
    def makeChoice(self,posibilities):
        left=self.direction-1
        if left<0:
            left=3
        right=self.direction+1
        if right>3:
            right=0
        back=left-1
        if back < 0:
            back=3
        
        for i in range(posibilities):
            if i==self.direction:#ligeud
                return [self.direction,3,0] # som i [til brug, til stack, til turnthread]
            elif i==right:
                return [right,4,2]
            elif i==left:
                return [left,3,4]
        return [back,0,3]

    def addX(self,x,y):
        return [x+1,y]
    
    def subX(self,x,y):
        return [x-1,y]
    
    def addY(self,x,y):
        return [x,y+1]
    
    def subY(self,x,y):
        return [x,y-1]
        
        
        
        
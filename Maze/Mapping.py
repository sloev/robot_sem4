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

    def __init__(self,path=None):
        '''
        Constructor
        mode=0 er mapping
        mode=1 er goToPath
        '''
        
        self.mode=0#mapping
        self.maze=Maze()
        self.globalCompass=[0,1,2,3]#north/east/south/west
        self.startDirection=self.globalCompass[2]
        self.direction=self.startDirection#south
                
        self.startPosition =[0,0]
        self.currentPosition=self.startPosition#x,y
        self.lastWas180=False
        self.lastPosition=[0,0]
        self.funcDict={
                       0:self.subY,
                       1:self.addX, 
                       2:self.addY, 
                       3:self.subX}
        if path!=None:
            self.stack=self.pathToStack()
        else:
            self.stack=[]
        '''
                        1 : self.goStraight,
                       2 : self.turnRight,
                       3 : self.turn180,
                       4 : self.turnLeft
                       }
                       
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
    def receiveStack(self,stack):
        #important see path.pathToStack()
        pass
    
    def stepsToCells(self,steps):
        cells=int(steps/self.stepsPrCell)
        #print"cells=%d"% cells
        return cells
    
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
        cells=self.stepsToCells(steps)
        func=self.funcDict[self.direction]
        
        tmpWalls=self.wallsToInt([1,1,0])  
                  
        for i in range(cells):
            tmp=self.maze.get(self.currentPosition[0], self.currentPosition[1])
            if not tmp:
                self.maze.set(self.currentPosition[0], self.currentPosition[1], tmpWalls)
            self.currentPosition=func(self.currentPosition)
        
        #self.currentPosition=func(self.currentPosition)
        globalWalls=self.wallsToInt(walls)            
        tmp=self.maze.get(self.currentPosition[0], self.currentPosition[1])
        if not tmp:
            self.maze.set(self.currentPosition[0], self.currentPosition[1], globalWalls)
            
        missingWalls=self.findMissingWalls(self.currentPosition,globalWalls)
        unexploredCells=self.findUnexploredCells(self.currentPosition,missingWalls)
        returnChoice=0

        if len(missingWalls)==1:#180
            if self.stack:#still unexplored nodes
                self.stack.pop()
                choice=self.makeChoice(missingWalls)
                returnChoice=3      
                self.direction=choice[1]
            else:
                pass
        else:
            if unexploredCells:
                choice=self.makeChoice(unexploredCells)
                self.stack.append(choice)
                returnChoice=choice[3]
                self.direction=choice[1]
            elif self.stack:
                choice=self.stack.pop()
                returnChoice=choice[2]
                self.direction=choice[0]
            else:
                pass
        print(
              str(self.currentPosition)
              +"\tdirection="+str(self.direction)
              +"\tm-walls="+str(missingWalls)+"\tunex="+str(unexploredCells)+"\t"
              +str(self.stack)
              )
#         print (
#                "cells="+str(cells)
#                +" "+str(self.currentPosition)
#                +"\tdirection="+str(self.direction)
#                +"\twalls="+str(walls)+
#                "  \tglobalWalls="
#                +str(globalWalls)
#                +"\tm-walls="+str(missingWalls)+"    "
#                +"\tchoice="+str(choice)
#                +"  \tR-Choice="+str(returnChoice)
#                )
        if returnChoice!=0:
            self.currentPosition=self.funcDict[self.direction](self.currentPosition)

        self.lastPosition=self.currentPosition

        return returnChoice
        
    def findMissingWalls(self,pos,globalWalls):
        posibilities=[]
        for d in range(4):
            if not globalWalls[d]:
                posibilities.append(d)
        return posibilities
    
    def findUnexploredCells(self,pos,missingWalls):
        posibilities=[]
        for d in missingWalls:
            xy=self.funcDict[d](pos)
            if xy[0]>=0 and xy[1]>=0:
                tmp=self.maze.get(xy[0], xy[1])
                if not tmp:
                    posibilities.append(d)
        return posibilities
        
    def makeChoice(self,posibilities):
        left=self.direction-1
        if left<0:
            left=3
        right=self.direction+1
        if right>3:
            right=0
        
        back=self.direction-2
        if back < 0:
            back+=4
            #print "direction="+str(self.direction)+"back before="+str(back)+" back after"+str(back2)
        if self.direction in posibilities:
            return [back,self.direction,1,1] # som i [til brug, til stack, til turnthread]
        elif right in posibilities:
            return [left,right,4,2]
        elif left in posibilities:
            return [right,left,2,4]
        lol=[self.direction,back,1,3]
        #self.stack.append(lol)
        #self.stack.append(lol)
        return lol

    def addX(self,xy):
        return [xy[0]+1,xy[1]]
    
    def subX(self,xy):
        return [xy[0]-1,xy[1]]
    
    def addY(self,xy):
        return [xy[0],xy[1]+1]
    
    def subY(self,xy):
        return [xy[0],xy[1]-1]
        
    def getMaze(self):
        return self.maze
        
        
        

  
def main():
    mapping=Mapping()
    cell=6018
    
    steps=cell
    walls=[0,1,0]
    mapping.getChoice(steps, walls)#[0,1]
    steps=0
    
    steps=cell
    walls=[0,1,1]
    mapping.getChoice(steps, walls)#[0,3]
    
    steps=cell
    walls=[0,1,1]
    mapping.getChoice(steps, walls)#[2,3]
    
    steps=0
    walls=[0,1,0]
    mapping.getChoice(steps, walls)#[2,2]
    
    steps=0
    walls=[0,1,0]
    mapping.getChoice(steps, walls)#[2,1]
    
    steps=0
    walls=[0,0,1]
    mapping.getChoice(steps, walls)#[2,0]
    
    steps=0
    walls=[1,0,1]
    mapping.getChoice(steps, walls)#[3,0]
    
    steps=cell*2    
    walls=[1,1,1]
    mapping.getChoice(steps, walls)#[3,3]
    
    steps=cell*2
    walls=[0,1,1]
    mapping.getChoice(steps, walls)#[3,0]
    
    steps=0
    walls=[0,1,0]
    mapping.getChoice(steps, walls)#[2,0]
    
    steps=0
    walls=[1,1,1]
    mapping.getChoice(steps, walls)#[1,0]
    
    steps=0
    walls=[1,0,0]
    mapping.getChoice(steps, walls)#[2,0]
    
    steps=0
    walls=[1,0,0]
    mapping.getChoice(steps, walls)#[2,1]

    steps=cell
    walls=[0,0,1]
    mapping.getChoice(steps, walls)#[0,1]
    
    steps=cell
    walls=[0,0,1]
    mapping.getChoice(steps, walls)#[2,1]
    
    steps=0
    walls=[1,0,0]
    mapping.getChoice(steps, walls)#[2,2]
    
    steps=0
    walls=[1,1,1]
    mapping.getChoice(steps, walls)#[1,2]
    
    steps=0
    walls=[1,1,1]
    mapping.getChoice(steps, walls)#[1,2]

    steps=0
    walls=[0,0,1]
    print mapping.getChoice(steps, walls)#[2,2]
    
    steps=0
    walls=[1,0,1]
    print mapping.getChoice(steps, walls)#[2,3]

    steps=cell
    walls=[1,0,1]
    print mapping.getChoice(steps, walls)#[0,3]
    
    maze=mapping.getMaze()
    print maze
#     maze.set(0,0,13)
#     maze.set(1,0,11)
#     maze.set(2,0,8)
#     maze.set(3,0,12)
#     maze.set(0,1,1)
#     maze.set(1,1,10)
#     maze.set(2,1,4)
#     maze.set(3,1,5)
#     maze.set(0,2,5)
#     maze.set(1,2,11)
#     maze.set(2,2,4)
#     maze.set(3,2,5)
#     maze.set(0,3,3)
#     maze.set(1,3,10)
#     maze.set(2,3,6)
#     maze.set(3,3,7)
    
if __name__ == '__main__':
    main()
        
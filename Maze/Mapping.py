'''
Created on Nov 15, 2013

@author: johannes
'''
from Maze import Maze
import logging

class Mapping():
    '''
    classdocs
    '''
    stepsPrCell=6500

    def __init__(self):
        self.mode=0#mapping mode
        '''
        Constructor
        mode=0 er mapping
        mode=1 er goToPath
        '''
        self.logger=logging.getLogger("robot.Mapping")
        self.logger.info("Mapping initialised")
        self.mode=0#mapping
        self.maze=Maze()
        self.globalCompass=[0,1,2,3]#north/east/south/west
        self.startDirection=self.globalCompass[2]
        self.direction=self.startDirection#south
                
        self.startPosition =[0,0]
        self.currentPosition=self.startPosition#x,y
        
        self.lastWas180=False
        self.lastPosition=self.currentPosition
        self.funcDict={
                       0:self.subY,
                       1:self.addX, 
                       2:self.addY, 
                       3:self.subX}

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
    def receiveStack(self,path):        
        self.mode=1#path finding go to mode
        self.stack=path#self.pathToStack()
        lastS=self.direction
            
        for i in range(len(self.stack)):
            j=len(self.stack)-i-1
            direction=self.stack[j][0]
            steps=self.stack[j][1]
            self.stack[j]=[direction,steps]#self.getLocalDirection(lastS,direction),steps]
            lastS=direction
        print self.stack
        

    def getLocalDirection(self,lastS,s):
        #print lastS
        left=lastS-1
        if left<0:
            left=3
        right=lastS+1
        if right>3:
            right=0
        
        direction180=lastS-2
        if direction180 < 0:
            direction180+=4        
        
        if left==s:
            return 2
        elif right==s:
            return 4
        elif direction180==s:
            return 3
        return 1
    
    def getCurrentPosition(self):
        print "mapping getCurrentPosition"
        print"currentPos="+str(self.currentPosition)
        return self.currentPosition
    
    def stepsToCells(self,steps):
        #print steps
        cells=(steps*1.0)/(self.stepsPrCell*1.0)
        decimals=cells % 1
        cells=int(cells)
        if decimals > 0.75 and cells<1:
            cells+=1
        elif decimals > 0.75:
            cells+=1
        self.logger.info("cells/"+str(cells))
        return cells
    
    def wallsToGlobalWalls(self,walls):
        north=0
        east=0
        south=0
        west=0
        if(self.startPosition == self.currentPosition):#south
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
                north=0
                east=walls[0]
                south=walls[2]
                west=walls[1]
            else:#west
                west=walls[2]
                east=0
                south=walls[0]
                north=walls[1]
        return [north,east,south,west]
    
    def wallsToInt(self,walls):
        value=(((walls[0]<<3) | (walls[1]<<2)) | (walls[2]<<1)) | (walls[3])        
        return value
                
    def getChoice(self,steps=None,walls=None):
        if not self.mode:
            return self.mappingChoice(steps, walls)
        else:
            return self.gotoChoice()
        
    def gotoChoice(self):
        returnChoice=[0,0]#steps,local direction
        cells=0
        if self.stack:
            choice=self.stack.pop()
            cells=choice[1]
            returnChoice[0]=cells*self.stepsPrCell
            choice=self.makeChoice([choice[0]])
            returnChoice=choice[3]
            self.direction=choice[1]
            #returnChoice[1]=choice[1]
            #self.direction=choice[0]
            #cells

                
            #self.currentPosition=func(self.currentPosition)
        print(
              "dir="+str(self.direction)
              +"\tpos"+str(self.currentPosition)
              +"\tchoice"+str(returnChoice)
              )
        if returnChoice!=[0,0]:
            for i in range(cells):
                self.currentPosition=self.funcDict[self.direction](self.currentPosition)
        return returnChoice

    def mappingChoice(self,steps,walls):
        self.logger.info("directionIn/"+str(self.direction))

        func=self.funcDict[self.direction]
        
        tmpWalls=self.wallsToGlobalWalls([1,1,0]) 
        cells=self.stepsToCells(steps)+1

        for i in range(cells):
            tmpWalls=self.wallsToInt(self.wallsToGlobalWalls([1,1,0]))
            tmp=self.maze.get(self.currentPosition[0], self.currentPosition[1])
            if not tmp:
                self.maze.set(self.currentPosition[0], self.currentPosition[1], tmpWalls)
            self.currentPosition=func(self.currentPosition)
         
        tmp=self.maze.get(self.currentPosition[0], self.currentPosition[1])
        globalWalls=self.wallsToGlobalWalls(walls)            

        if not tmp:
            self.maze.set(self.currentPosition[0], self.currentPosition[1], self.wallsToInt(globalWalls))
        #self.currentPosition=self.funcDict[self.direction](self.currentPosition)
        print "after incrementation current pos="+str(self.currentPosition)+" dir="+str(self.direction)

        missingWalls=self.findMissingWalls(self.currentPosition,globalWalls)
        unexploredCells=self.findUnexploredCells(self.currentPosition,missingWalls)
        
        returnChoice=0

        if len(missingWalls)==1:#180
            if self.stack:#still unexplored nodes
                self.logger.info("180")
                self.stack.pop()
                self.logger.info("stack/"+str(self.stack))
                choice=self.makeChoice(missingWalls)
                returnChoice=3      
                self.direction=choice[1]
            else:
                pass
        else:
            if unexploredCells:
                self.logger.info("exploring")
                choice=self.makeChoice(unexploredCells)
                self.stack.append(choice)
                self.logger.info("stack/"+str(self.stack))
                returnChoice=choice[3]
                self.direction=choice[1]
            elif self.stack:
                self.logger.info("backtracking")
                choice=self.stack.pop()
                choice=self.makeChoice([choice[0]])

                self.logger.info("stack/"+str(self.stack))
                returnChoice=choice[3]
                self.direction=choice[1]
            else:
                print "finnished mapping"
                #func=self.funcDict[self.direction]
                #self.currentPosition=func(self.currentPosition)
                return 0
        print(
              "dir="+str(self.direction)
              +"\tpos"+str(self.currentPosition)
              +"\tchoice"+str(returnChoice)
              )
        self.logger.info("returnChoice/"+str(returnChoice))
        self.logger.info("currentpos/"+str(self.currentPosition))
        self.logger.info("directionOut/"+str(self.direction))

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
            return [left,right,2,4]
        elif left in posibilities:
            return [right,left,4,2]
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
    steps=[]
    walls=[]
    steps.append(0)
    walls.append([0,1,0])
    
    steps.append(cell)
    walls.append([0,1,1])
    
    steps.append(cell)
    walls.append([0,1,1])
    
    steps.append(0)
    walls.append([0,1,0])
    
    steps.append(0)
    walls.append([0,1,0])
    
    steps.append(0)
    walls.append([0,0,1])
    
    steps.append(2000)
    walls.append([1,0,1])
    
    steps.append(cell*2)
    walls.append([1,1,1])
    
    steps.append(cell*2)
    walls.append([0,1,1])
    
    steps.append(2000)
    walls.append([0,1,0])
    
    steps.append(2000)
    walls.append([1,1,1])
    
    steps.append(2000)
    walls.append([1,0,0])
    
    steps.append(0)
    walls.append([1,0,0])

    steps.append(cell)
    walls.append([0,0,1])
    
    steps.append(cell)
    walls.append([0,0,1])
    
    steps.append(0)
    walls.append([1,0,0])
    
    steps.append(0)
    walls.append([1,1,1])

    steps.append(0)
    walls.append([0,0,1])
    
    steps.append(0)
    walls.append([1,0,1])

    steps.append(cell)
    walls.append([1,0,1])
    
    steps.append(cell)
    walls.append([1,0,0])
    
    steps.append(cell)
    walls.append([1,0,0])
    
    for i in range(len(walls)-1):
        w=walls[i]
        s=steps[i]
        choice=mapping.getChoice(s, w)#[0,3]
        print choice
        if not choice:
            print "exited at index %d" %i
            break

    maze=mapping.getMaze()

    print maze

    path=[2, 2, 2, 1, 0, 1, 1, 2]
    value=10
    mapping.receiveStack(path)
    while(value!=[0,0]):
        value=mapping.getChoice(0,[1,1,1])
        
    path=[2, 2, 3, 0, 0, 0]
    value=10
    mapping.receiveStack(path)
    while(value!=[0,0]):
        value=mapping.getChoice(0,[1,1,1])
        #print value
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
        
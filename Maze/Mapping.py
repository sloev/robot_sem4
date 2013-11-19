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
        self.direction=self.globalCompass[2]#south
        
        self.startPosition=[0,0]
        self.startDirection=[0,0]
        
        self.currentPosition=[0,0]#x,y
        self.lastPosition=[0,0]
        self.funcDict={0:self.subY, 1:self.addX, 2:self.addY, 3:self.subX}
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
        globalWalls=self.wallsToInt(walls)
        for i in range(cells):
            tmp=self.maze.get(self.currentPosition[0], self.currentPosition[1])
            if not tmp:
                self.maze.set(self.currentPosition[0], self.currentPosition[1], globalWalls)
            self.currentPosition=func(self.currentPosition)
        posibilities=self.findPossibilities(self.currentPosition,globalWalls)

        if not posibilities:
            if self.stack:
                choice=self.stack.pop()
            else:
                return 0#stop robot
        else:
            choice=self.makeChoice(posibilities)
            
        self.direction=choice[0]
        self.stack.append(choice)   
        choice=choice[2]             

        print (
               str(self.currentPosition)
               +"\tdirection="+str(self.direction)
               +"\twalls="+str(walls)+
               "  \tglobalWalls="
               +str(globalWalls)
               +"\tposibilities="+str(posibilities)
               +"   \tchoice="+str(choice)
               )
        self.lastPosition=self.currentPosition
        return choice

        
#         x=self.lastPosition[0]
#         y=self.lastPosition[1]
#         
#         func=self.funcDict[self.direction]
#         dx=x
#         dy=y
#         for i in range(cells):
#             tmp=func(dx,dy)
#             dx=tmp[0]
#             dy=tmp[1]
#         self.currentPosition=[dx,dy]
# 
#         
#         dX=abs(self.currentPosition[0]-self.lastPosition[0])
#         dY=abs(self.currentPosition[1]-self.lastPosition[1])
#         dI=dY if dY!=0 else dX
#         
# 
#         walls=self.wallsToInt(walls)
#         for i in range(dI):
#             self.maze.set(x, y, walls)
#             tmp=func(x,y)
#             x=tmp[0]
#             y=tmp[1]
#         posibilities=self.findPossibilities(self.currentPosition)
#         if not posibilities:
#             choice=self.stack.pop()
#             if not choice:
#                 choice=0#stop robot
#         else:
#             choice=self.makeChoice(posibilities)
#         self.lastPosition=self.currentPosition      
#         self.direction=choice[0]
#         self.stack.append(choice[1])
#         return choice[2]
        
    def findPossibilities(self,pos,globalWalls):
        posibilities=[]
        for d in range(4):
            if not globalWalls[d]:
                xy=self.funcDict[d](pos)
                if xy[0]>=0 and xy[1]>=0:
                    tmp=self.maze.get(xy[0], xy[1])
                    if not tmp:
                        posibilities.append(d)
        return posibilities
        
    def makeChoice(self,posibilities):
        left=self.direction-1
        if left<0:
            left+=3
        right=self.direction+1
        if right>3:
            right+=3
        
        back=self.direction-2
        if back < 0:
            back2=3+back
            print "direction="+str(self.direction)+"back before="+str(back)+" back after"+str(back2)
            back=back2
        if self.direction in posibilities:
            return [self.direction,1,1] # som i [til brug, til stack, til turnthread]
        elif right in posibilities:
            return [right,4,2]
        elif left in posibilities:
            return [left,2,4]
        return [back,1,3]

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
    walls=[1,0,1]
    mapping.getChoice(steps, walls)#[1,2]
        
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
        
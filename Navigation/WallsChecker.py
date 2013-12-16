'''
Created on Oct 30, 2013

@author: johannes
'''
import logging
class WallsChecker():
    def __init__(self,left,right,front,cmMin,cmMax,setPoint):
        self.logger=logging.getLogger("robot.wallsChecker")
        self.min=cmMin
        self.max=cmMax
        self.setpoint=setPoint
        self.left=left
        self.right=right
        self.front=front
        self.walls=[1,1,1]
        self.lastWalls=self.walls
        self.lastLastWalls=self.lastWalls
        
    def checkWalls(self,sample):
        self.lastLastWalls=self.lastWalls
        self.lastWalls=self.walls
        
        self.walls=[1,1,1]
        if(sample[self.left]>self.max):
            self.walls[self.left]=0
        if(sample[self.right]>self.max):
            self.walls[self.right]=0
        if(sample[self.front]>(self.setpoint*1.5)):
            self.walls[self.front]=0
        self.logger.info("checkWalls/"+str(self.walls))
        return self.walls
    
    def compare(self):
        foo=(self.walls==self.lastWalls) and (self.walls==self.lastLastWalls)
        self.logger.info("compareSidesAndFront/"+str(foo))
        return foo
      
    def compareSides(self):
        foo=self.walls[self.left]==self.lastWalls[self.left] and self.walls[self.right]==self.lastWalls[self.right] 
        self.logger.info("compareSides/"+str(foo))
        return foo
    
    def compareFront(self):
        foo= self.walls[self.front]==self.lastWalls[self.front]
        self.logger.info("compareFront/"+str(foo))
        return foo

if __name__ == '__main__':
    pass

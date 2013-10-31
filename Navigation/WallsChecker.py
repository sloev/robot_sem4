'''
Created on Oct 30, 2013

@author: johannes
'''
import logging
class WallsChecker():
    def __init__(self,minMax,left,right,front):
        self.logger=logging.getLogger("robot.wallsChecker")
        self.min=minMax[0]
        self.max=minMax[1]
        self.left=left
        self.right=right
        self.front=front
        self.walls=[1,1,0]
        
    def checkWalls(self,sample):
        self.lastWalls=self.walls
        
        self.walls=[1,1,0]
        if(sample[self.left]>self.cmMax):
            self.walls[self.left]=0
        if(sample[self.right]>self.cmMax):
            self.walls[self.right]=0
        if(sample[self.front]<self.setPoint):
            self.walls[self.front]=1
        self.logger.info("checkWalls/"+str(self.walls))
        return self.walls
    
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

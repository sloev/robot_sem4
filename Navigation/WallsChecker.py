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
        
    def checkWalls(self,sample):
        self.lastWalls=self.walls
        
        walls=[1,1,0]
        if(self.sample[self.left]>self.cmMax):
            walls[self.left]=0
        if(self.sample[self.right]>self.cmMax):
            walls[self.right]=0
        if(self.sample[self.front]<self.setPoint):
            walls[self.front]=1
        self.logger.info("checkWalls/"+str(walls))
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

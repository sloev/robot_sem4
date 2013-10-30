'''
Created on Oct 30, 2013

@author: johannes
'''
class WallsChecker():
    def __init__(self,minMax,left,right,front):
        self.min=minMax[0]
        self.max=minMax[1]
        self.left=left
        self.right=right
        self.front=front
        
    def checkWalls(self,sample):
        self.lastWalls=self.walls
        return self.walls
    
    def compareSides(self):
        return self.walls[self.left]==self.lastWalls[self.left] and self.walls[self.right]==self.lastWalls[self.right] 
    
    def compareFront(self):
        return self.walls[self.front]==self.lastWalls[self.front]
     
if __name__ == '__main__':
    pass


    def sampleDistances(self):
        self.sample=self.ir_sensors.multiChannelReadCm(sensorChannels,5)
        self.logger.info("sample:"+str(self.sample))
        #print("sample="+str(self.sample))
        
        



    def detectMissingWalls(self):
        self.sampleDistances()
        walls=[1,1,0]
        if(self.sample[self.left]>self.cmMax):
            walls[self.left]=0
        if(self.sample[self.right]>self.cmMax):
            walls[self.right]=0
        if(self.sample[self.front]<self.setPoint):
            walls[self.front]=1
        self.logger.info("walls/"+str(walls))
        return walls  
      
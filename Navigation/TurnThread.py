'''
Created on Oct 30, 2013

@author: johannes
'''
import logging
import time

Vin1                                =   0x08
Vin2                                =   0x09
Vin3                                =   0x0A

sensorChannels=[Vin1,Vin2,Vin3]

class TurnThread():
    def __init__(self,irSensors,wallchecker,dual_motors,left,right):
        self.dual_motors=dual_motors
        self.irsensors=irSensors
        self.wallchecker=wallchecker
        self.left=left
        self.right=right
        self.funcDict={
                       1 : self.goStraight,
                       2 : self.turnRight,
                       3 : self.turn180,
                       4 : self.turnLeft
                       }
        self.logger=logging.getLogger("robot.TurnThread")
        self.logger.info("TurnThread initialised")
        pass
    
    def checkForTurn(self,choice):
        try:
            self.funcDict[choice]()
        except KeyError:
            pass
            
    def turnLeft(self):
        self.logger.info("left")
        self.oldTurn(0)
        pass
    
    def turnRight(self):
        self.logger.info("right")
        self.oldTurn(1)
        pass
    
    def turn180(self):
        print("turning180")
        self.logger.info("180")
        self.dual_motors.softStop()
        time.sleep(0.3)
        self.dual_motors.turn180(2)
        time.sleep(1.6)
    
        self.dual_motors.setMotorParams(self.left, self.right, 2, 2)
        time.sleep(0.5)
        pass
    
    def goStraight(self):
        self.logger.info("straight")
        pass
    
    def oldTurn(self,direction):
        #print("turning wheel="+str(direction))
        sample=self.irsensors.multiChannelReadCm(sensorChannels,5)
        walls=self.wallchecker.checkWalls(sample)  
        debounce=self.wallchecker.compare()
        
        time.sleep(0.3)
        self.dual_motors.softStop()
        time.sleep(0.3)
        self.dual_motors.turn90(direction, 2)
        time.sleep(0.8)
        
        sample=self.irsensors.multiChannelReadCm(sensorChannels,5)
        walls=self.wallchecker.checkWalls(sample)  
        debounce=self.wallchecker.compare()
        
        self.dual_motors.setMotorParams(self.left, self.right, 2, 2)
        self.dual_motors.setPosition(32767, 32767)
        
        while(not debounce):
            time.sleep(0.3)
            sample=self.irsensors.multiChannelReadCm(sensorChannels,5)
            walls=self.wallchecker.checkWalls(sample)  
            debounce=self.wallchecker.compare()
        time.sleep(0.2)
def main():
    pass

if __name__== '__main__':
    main()

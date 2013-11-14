'''
Created on Oct 30, 2013

@author: johannes
'''
import logging
import time
import Calibrate

Vin1                                =   0x08
Vin2                                =   0x09
Vin3                                =   0x0A

sensorChannels=[Vin1,Vin2,Vin3]

class TurnThread():
    def __init__(self,irSensors,wallchecker,dual_motors,left,right):
        self.dual_motors=dual_motors
        self.irsensors=irSensors
        self.wallchecker=wallchecker
        #self.calibrater = Calibrate()
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
        value=0
        try:
            if(choice>1):
                value=1
            self.funcDict[choice]()
        except KeyError:
            pass
        return value

            
    def turnLeft(self):
        self.logger.info("left")
        self.dual_motors.setMotorParams(self.left, self.right, 1, 1)
        self.turn90(0)
    
    def turnRight(self):
        self.logger.info("right")
        self.dual_motors.setMotorParams(self.left, self.right, 1, 1)
        self.turn90(1)
    
    def turn180(self):
        print("turning180")
        self.dual_motors.setMotorParams(self.left, self.right, 1, 1)

        self.logger.info("180")
        self.dual_motors.softStop()
        time.sleep(0.3)
        self.dual_motors.turn180(2)
        time.sleep(1.6)
    
        time.sleep(0.5)
        pass
    
    def goStraight(self):
        self.logger.info("straight")
        self.dual_motors.setMotorParams(self.left, self.right, 1, 1)

        print("straight")
        
    def turn90(self,direction):
        self.dual_motors.softStop()
        while(self.dual_motors.isBusy()):
            self.logger.info("turning")
            time.sleep(0.1)
   
        print("Driving out to turn")
        self.initialize90Turn()

        print "Turning 90 NOW"
        self.dual_motors.turn90(direction,2)
        while(self.dual_motors.isBusy()):
            self.logger.info("turning")
            time.sleep(0.1)
        
        print "Driving out of turn"   
        self.dual_motors.setMotorParams(self.left, self.right, 1, 1)
        self.dual_motors.setPosition(3650, 3650)
        
        while(self.dual_motors.isBusy()):
            self.logger.info("turning")
            time.sleep(0.1)
            
    def initialize90Turn(self):
        self.dual_motors.setMotorParams(self.right, self.left, 1, 1)
        self.dual_motors.setPosition(32768, 32768)
        while(self.irsensors.multiChannelReadCm([0x0A], 0x20) > 9):
            time.sleep(0.1)
        
        
       
        
def main():
    pass

if __name__== '__main__':
    main()

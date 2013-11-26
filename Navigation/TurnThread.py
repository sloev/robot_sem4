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
    stepsPrCell=6018

    def __init__(self,irSensors,wallchecker,dual_motors,left,right):
        self.dual_motors=dual_motors
        self.irsensors=irSensors
        self.wallchecker=wallchecker
        self.left=left
        self.right=right
        self.funcDict={
                       -1:self.goInto,
                       1 : self.goStraight,
                       2 : self.turnRight,
                       3 : self.turn180,
                       4 : self.turnLeft
                       }
        self.logger=logging.getLogger("robot.TurnThread")
        self.logger.info("TurnThread initialised")
        pass
    
    def checkForTurn(self,choice):
        if choice in self.funcDict:
            self.funcDict[choice]()
            return 1
        return 0
            
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
        self.dual_motors.setAccelerations(self.left, self.right, 1)

        self.logger.info("180")
        self.dual_motors.softStop()
        self.dual_motors.turn180(2) 
        while(self.dual_motors.isBusy()):
            time.sleep(0.1)
    
    def goStraight(self):
        self.logger.info("straight")
        self.dual_motors.setMotorParams(self.left, self.right, 1,1)
        self.dual_motors.setAccelerations(self.left, self.right, 1)
        self.dual_motors.setPosition((self.stepsPrCell/3)*2,(self.stepsPrCell/3)*2)
        while(self.dual_motors.isBusy()):
            self.logger.info("straight")
            time.sleep(0.1)
        print("straight")
        
    def goInto(self):
        self.logger.info("gointo")
        self.dual_motors.setMotorParams(self.left, self.right, 1,1)
        self.dual_motors.setAccelerations(self.left, self.right, 1)
        self.dual_motors.setPosition(500+self.stepsPrCell/2,500+self.stepsPrCell/2)
        while(self.dual_motors.isBusy()):
            self.logger.info("gointo")
            time.sleep(0.1)
        print("gointo")        
        
    def turn90(self,direction):
        self.dual_motors.setAccelerations(self.left, self.right, 1)

        #self.dual_motors.softStop()
        while(self.dual_motors.isBusy()):
            self.logger.info("turning")
            time.sleep(0.1)
   
        print("Driving out to turn")
        self.dual_motors.setMotorParams(self.left, self.right, 1, 1)
#         self.dual_motors.setPosition(3600, 3580)
#         
#         while(self.dual_motors.isBusy()):
#             self.logger.info("turning")
#             time.sleep(0.1)

        print "Turning 90 NOW"
        self.dual_motors.turn90(direction,2)
        while(self.dual_motors.isBusy()):
            self.logger.info("turning")
            time.sleep(0.1)
        
        print "Driving out of turn"   
        self.dual_motors.setMotorParams(self.left, self.right, 1, 1)
        #self.dual_motors.setAccelerations(self.left, self.right, 1)
        self.dual_motors.setPosition(3650, 3630)
        
        while(self.dual_motors.isBusy()):
            self.logger.info("turning")
            time.sleep(0.1)
       
        
def main():
    pass

if __name__== '__main__':
    main()

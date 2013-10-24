'''
Created on Oct 2, 2013

@author: johannes, benjamin
'''
'class variables:'


from Decorators.TMC222Status import TMC222Status
from Motor_I2C import Motor_I2C
import time as time
import logging
import sys
class DualMotorController:
    '''
        for controlling two stepper motors through i2c
    '''
    
    def __init__(self, add1, add2):
        self.turn90Steps=1500
        self.turn180Steps=6316
        
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing DualMotorController")
        self.motorLeft = Motor_I2C(add1)
        self.motorRight = Motor_I2C(add2)
        self.positionLeft=200
        self.positionRight=200
        self.logger.debug("Initializing DualMotorController DONE")

    
    def setOtpParam(self):
        self.logger.debug("setOtpParam")

        self.motorLeft.setOTPParam()
        self.motorRight.setOTPParam()
    
        
    def runInit(self):
        self.logger.debug("runInit")

        self.motorLeft.runInit()
        self.motorRight.runInit()
    
    def setMotorParams(self,leftDir,rightDir,leftMaxVel,rightMaxVel):
        self.logger.debug("setMotorParams")

        self.motorLeft.setMotorParam(leftDir, leftMaxVel)
        self.motorRight.setMotorParam(rightDir, rightMaxVel)
    
    def getFullStatus1(self):
        self.logger.debug("getFullStatus1")

        return [self.motorLeft.getFullStatus1(),self.motorRight.getFullStatus1()]
    
    def getFullStatus2(self):
        self.logger.debug("getFullStatus2")

        return [self.motorLeft.getFullStatus2(),self.motorRight.getFullStatus2()]
    
    def turn90(self,direction,maxVel):
        self.logger.debug('turn 90:'+str(direction))

        self.motorLeft.setMotorParam(direction, maxVel)
        self.motorRight.setMotorParam(direction, maxVel)
        
        self.setPosition(self.turn90Steps, self.turn90Steps)
        
    def turn180(self,maxVel):
        self.logger.debug("turn180")

        self.motorLeft.setMotorParam(1, maxVel)
        self.motorRight.setMotorParam(1, maxVel)
        
        self.setPosition(self.turn180Steps, self.turn180Steps)
        
    def setPosition(self,incLeftPos,incRightPos):
        self.logger.debug("setPosition"+str(incLeftPos)+","+str(incRightPos))

        self.positionLeft+=incLeftPos
        self.positionRight+=incRightPos
        
        self.motorLeft.setPosition(self.positionLeft)
        self.motorRight.setPosition(self.positionRight)
        
    def getOfflinePosition(self):
        return [self.positionLeft,self.positionRight]
    
    def isBusy(self,fullStatus2Matrix):
        leftstatus=fullStatus2Matrix[0][:]
        rightstatus=fullStatus2Matrix[1][:]
        leftstatus=(leftstatus[1] == leftstatus[3]) & (leftstatus[2] == leftstatus[4])
        rightstatus=(rightstatus[1] == rightstatus[3]) & (rightstatus[2] == rightstatus[4])
        value=(leftstatus & rightstatus)==1
       
        self.logger.debug("isBusy="+str(value))
        return value
        
    def hardStop(self):
        self.logger.debug("hardStop")

        self.motorLeft.hardStop()
        self.motorRight.hardStop()
        
    def softStop(self):
        self.logger.debug("softStop")

        self.motorLeft.softStop()
        self.motorRight.softStop()
        
def main():

    motors=DualMotorController(0x60,0x61)
    if(len(sys.argv)>0):
        motors.turn90Steps=int(sys.argv[1])
        print str(motors.turn90Steps)
    motors.setOtpParam()
    #print(str(motors.getFullStatus1()[0][:])+"\n"+str(motors.getFullStatus1()[1][:]))
    tmp=motors.getFullStatus2()
    #print("busy="+motors.isBusy(tmp))
    motors.setMotorParams(1, 0, 5, 5)
    motors.runInit()
    time.sleep(5)
    #print(str(motors.getFullStatus1()[0][:])+"\n"+str(motors.getFullStatus1()[1][:]))
    print("turning left")
    motors.turn90(1, 5)
    
    time.sleep(4)
   # print(str(motors.getFullStatus1()[0][:])+"\n"+str(motors.getFullStatus1()[1][:]))

   # motors.turn90(0, 5)
    #time.sleep(6)
    #print(str(motors.getFullStatus1()[0][:])+"\n"+str(motors.getFullStatus1()[1][:]))
    #motors.setPosition(2000, 2000)

if __name__ == '__main__':
    main()
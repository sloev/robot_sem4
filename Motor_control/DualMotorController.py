'''
Created on Oct 2, 2013

@author: johannes, benjamin
'''
'class variables:'
turn90Steps=3158
turn180Steps=6316

from Decorators.TMC222Status import TMC222Status
from Motor_I2C import Motor_I2C
import time as time

class DualMotorController:
    def __init__(self, add1, add2):
        self.motorLeft = Motor_I2C(add1)
        self.motorRight = Motor_I2C(add2)
        self.positionLeft=200
        self.positionRight=200
    
    def setOtpParam(self):
        self.motorLeft.setOTPParam()
        self.motorRight.setOTPParam()
        
    def runInit(self):
        self.motorLeft.runInit()
        self.motorRight.runInit()
    
    def setMotorParams(self,leftDir,rightDir,leftMaxVel,rightMaxVel):
        self.motorLeft.setMotorParam(leftDir, leftMaxVel)
        self.motorRight.setMotorParam(rightDir, rightMaxVel)
    
    def getFullStatus1(self):
        return [self.motorLeft.getFullStatus1(),self.motorRight.getFullStatus1()]

    
    def test(self):
        self.motorLeft.printFullStatus1()

    
    def getFullStatus2(self):
        return [self.motorLeft.getFullStatus2(),self.motorRight.getFullStatus2()]
    
    def turn90(self,direction,maxVel):
        self.motorLeft.setMotorParam(direction, maxVel)
        self.motorRight.setMotorParam(not direction, maxVel)
        
        self.setPosition(turn90Steps, turn90Steps)
        
    def turn180(self,maxVel):
        self.motorLeft.setMotorParam(1, maxVel)
        self.motorRight.setMotorParam(0, maxVel)
        
        self.setPosition(turn180Steps, turn180Steps)
        
    def setPosition(self,incLeftPos,incRightPos):
        self.positionLeft+=incLeftPos
        self.positionRight+=incRightPos
        
        self.motorLeft.setPosition(self.positionLeft)
        self.motorRight.setPosition(self.positionRight)
        
    def getOfflinePosition(self):
        return [self.positionLeft,self.positionRight]
    
    def isBusy(self,fullStatus2Matrix):
        return 1
#         leftstatus=fullStatus2Matrix[0][:]
#         rightstatus=fullStatus2Matrix[1][:]
#         leftstatus=(leftstatus[1]<<8 | leftstatus[2]<<0) & (leftstatus[3]<<8 | leftstatus[4]<<0)
#         rightstatus=(rightstatus[1]<<8 | rightstatus[2]<<0) & (rightstatus[3]<<8 | rightstatus[4]<<0)
#         return (leftstatus & rightstatus)==1
        
    def hardStop(self):
        self.motorLeft.hardStop()
        self.motorRight.hardStop()
        
    def softStop(self):
        self.motorLeft.softStop()
        self.motorRight.softStop()
        
def main():
    print("init")
    motors=DualMotorController(0x60,0x61)
    motors.setOtpParam()
    print(str(motors.getFullStatus1()[0][:])+"\n"+str(motors.getFullStatus1()[1][:]))

    motors.setMotorParams(1, 0, 3, 3)
    motors.runInit()
    print(str(motors.getFullStatus1()[0][:])+"\n"+str(motors.getFullStatus1()[1][:]))


if __name__ == '__main__':
    main()
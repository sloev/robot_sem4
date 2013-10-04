'''
Created on Oct 2, 2013

@author: johannes, benjamin
'''

from Motor_I2C import Motor_I2C
import time as time


class DualMotorController:
    def __init__(self, add1, add2):
        self.left = Motor_I2C(add1)
        self.right = Motor_I2C(add2)
        
        self.posLeft=201
        self.posRight=201
        
    def dualSetOTPParam(self):
        self.left.setOTPParam()
        self.right.setOTPParam()
        
    def dualResettoDefault(self):
        self.left.resetToDefault()
        self.right.resetToDefault()
    
    def busy(self):
        leftstatus=self.left.getFullStatus2()
        rightstatus=self.right.getFullStatus2()
        leftstatus=(leftstatus[1]<<8 | leftstatus[2]<<0) | (leftstatus[3]<<8 | leftstatus[4]<<0)
        rightstatus=(rightstatus[1]<<8 | rightstatus[2]<<0) | (rightstatus[3]<<8 | rightstatus[4]<<0)
        return (leftstatus & rightstatus)==0
    
    def turnAround(self):
        self.turn90(1, 2)
    
    def turnLeft(self):
        self.turn90(1,1)
    
    def turnRight(self):
        self.turn90(0,1)
        
    def turn90(self,direction,times):
        self.dualSetDirection(direction)
        self.dualSetMaxVel(3)
        self.dualUpdateMotorParams()
        
        self.posLeft+=1579*times
        self.posRight+=1579*times

        self.left.setPosition(self.posLeft)
        self.right.setPosition(self.posRight)
    
    def runInit(self,posA,posB):
        self.left.runInit(posA, posB)
        self.right.runInit(posA, posB)
    
    def getActPosTarPosMatrix(self):
        leftstatus = self.left.getFullStatus2()
        rightstatus = self.right.getFullStatus2()
        leftActPos = leftstatus[1]<<8 | leftstatus[2]<<0
        leftTarPos= leftstatus[3]<<8 | leftstatus[4]<<0
        rightActPos = rightstatus[1]<<8 | rightstatus[2]<<0
        rightTarPos = rightstatus[3]<<8 | rightstatus[4]<<0
        return [[leftActPos,leftTarPos],[rightActPos,rightTarPos]]
    
 
    def dualSetPosition(self,position):        
        self.left.setPosition(position)
        self.right.setPosition(position)
    
    def dualUpdateMotorParams(self):
        self.left.setMotorParam()
        self.right.setMotorParam()
        
    def dualHardstop(self):
        self.left.hardStop()
        self.right.hardStop()
    
    def dualSoftstop(self):
        self.left.softStop()
        self.right.softStop()
        
    'set motor values:'
    
    def dualSetIrun(self,irun):
        self.left.setIrun(irun)
        self.right.setIrun(irun)
        
    def setLeftMaxVel(self,maxVelocity):
        self.left.setMaxVelocity(maxVelocity)
        
    def setRightMaxVel(self,maxVelocity):
        self.right.setMaxVelocity(maxVelocity)
        
    def dualSetMaxVel(self,maxVelocity):
        self.setLeftMaxVel(maxVelocity)
        self.setRightMaxVel(maxVelocity)
        
    def setLeftDirection(self,direction):
        self.left.setDirection(direction)
 
    def setRightDirection(self,direction):
        self.right.setDirection(direction)
    
    def dualSetDirection(self,direction):
        self.setRightDirection(direction)
        self.setLeftDirection(direction)
        
    def leftGetFullstatus1(self):
        r=self.left.getFullStatus1()
        return r
        
    def rightGetFullstatus1(self):
        r=self.right.getFullStatus1()
        return r
     
def main():
    print("create motor instances")
    dualMotors=DualMotorController(0x60,0x61)
    print("current positions (act/tar/act/tar):"+str(dualMotors.getActPosTarPosMatrix()))
    dualMotors.dualSetOTPParam()
    dualMotors.dualSetIrun(11)
    #dualMotors.dualSetMaxVel(3)
    dualMotors.setLeftDirection(1)
    dualMotors.setRightDirection(0)
    dualMotors.dualUpdateMotorParams()
    
    print("running init")
    dualMotors.runInit(100, 200)
    position=1500
    dualMotors.dualSetPosition(position)

    for i in range(1,30):
        position+=4000
        index=(i%6)+1
        dualMotors.dualSetMaxVel(index)

        dualMotors.dualUpdateMotorParams()
        
        dualMotors.dualSetPosition(position)
        print("IRun is="+str(i)+" current positions (act/tar/act/tar):"+str(dualMotors.getActPosTarPosMatrix()))
        time.sleep(1)
    #time.sleep(8)
    #dualMotors.dualHardstop()
    print(dualMotors.leftGetFullstatus1())
    time.sleep(0.1)
    print(dualMotors.rightGetFullstatus1())
        
        
        
     
if __name__ == '__main__':
    main()
'''
Created on Oct 2, 2013

@author: johannes, benjamin
'''

from Motor_I2C import Motor_I2C
import time as time

'in full steps'
halfRevolution=135 
quarterRevolution=67

class DualMotorController:
    def __init__(self, add1, add2):
        self.left = Motor_I2C(add1)
        self.right = Motor_I2C(add2)
        self.stepsPrStep=8
        self.posLeft=201
        self.posRight=201
        self.targetPosition=400
        
        
    def dualSetOTPParam(self):
        self.left.setOTPParam()
        time.sleep(0.1)
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
        self.dualUpdateMotorParams()
        
        incpos=(quarterRevolution*self.stepsPrStep)*times
        self.dualIncTargetPosition(incpos)

    def runInit(self,posA,posB):
        self.left.runInit(posA, posB)
        time.sleep(0.1)
        self.right.runInit(posA, posB)
    
    def getActPosTarPosMatrix(self):
        leftstatus = self.left.getFullStatus2()
        rightstatus = self.right.getFullStatus2()
        leftActPos = leftstatus[1]<<8 | leftstatus[2]<<0
        leftTarPos= leftstatus[3]<<8 | leftstatus[4]<<0
        rightActPos = rightstatus[1]<<8 | rightstatus[2]<<0
        rightTarPos = rightstatus[3]<<8 | rightstatus[4]<<0
        return [[leftActPos,leftTarPos],[rightActPos,rightTarPos]]
    
    def dualIncTargetPosition(self,incPosition):   
        self.targetPosition+=incPosition     
        self.left.setPosition(self.targetPosition)
        self.right.setPosition(self.targetPosition)
    
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
    dualMotors.dualSetIrun(10)
    dualMotors.dualSetMaxVel(5)
    dualMotors.setLeftDirection(1)
    dualMotors.setRightDirection(0)
    dualMotors.dualUpdateMotorParams()
    
    print("running init")
    dualMotors.runInit(100, 200)
    dualMotors.dualIncTargetPosition(3000)
    time.sleep(3)
    dualMotors.turnLeft()
    while(dualMotors.busy()):
        time.sleep(0.1)
    print("turned left")
    time.sleep(3)
    
    dualMotors.turnRight()
    while(dualMotors.busy()):
        time.sleep(0.1)
    print("turned right")
    time.sleep(3)

#     for i in range(1,30):
#         index=(i%6)+1
#         dualMotors.dualSetMaxVel(index)
# 
#         dualMotors.dualUpdateMotorParams()
#         dualMotors.dualIncTargetPosition(4000)
# #        print("IRun is="+str(i)+" current positions (act/tar/act/tar):"+str(dualMotors.getActPosTarPosMatrix()))
#         time.sleep(1)
#     print("IRun is="+str(i)+" current positions (act/tar/act/tar):"+str(dualMotors.getActPosTarPosMatrix()))

    print(dualMotors.leftGetFullstatus1())
    time.sleep(0.1)
    print(dualMotors.rightGetFullstatus1())
        
        
        
     
if __name__ == '__main__':
    main()
'''
Created on Oct 2, 2013

@author: johannes, benjamin
'''
from Motor_I2C import Motor_I2C
import time as time

class DualMotorController:
    def __init__(self, add1, add2):
        self.ad1=add1
        self.add2=add2
        self.left = Motor_I2C(add1)
        self.right = Motor_I2C(add2)
        
        self.posLeft=201
        self.posRight=201
        
        self.leftDir=0
        self.rightDir=1
        
        self.leftSpeed=3
        self.rightSpeed=3
        
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
    
    def turn180(self):
        self.turn90(1, 2)
    
    def turnLeft(self):
        self.turn90(1,1)
    
    def turnRight(self):
        self.turn90(0,1)
        
    def turn90(self,direction,times):
        self.left.setMotorParam(direction,3,1)
        self.right.setMotorParam(direction,3,1)
        
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
    
    def setLeftSpeed(self,leftSpeed):
        self.leftSpeed=leftSpeed
        self.updateMotorParams()
 
    def setRightSpeed(self,rightSpeed):
        self.rightSpeed=rightSpeed
        self.updateMotorParams()
        
    def setLeftDirection(self,leftDir):
        self.leftDir=leftDir
        self.updateMotorParams()
 
    def setRightDirection(self,rightDir):
        self.rightDir=rightDir
        self.updateMotorParams()
    
    def setDualPosition(self,position):
        self.posLeft=position
        self.posRight=position
    
    def dualUpdateMotorParams(self):
        self.left.setMotorParam(self.leftDir,self.leftSpeed,1)
        self.right.setMotorParam(self.rightDir,self.rightSpeed,1)
        
    def dualHardstop(self):
        self.left.hardStop()
        self.right.hardStop()
    
    def dualSoftstop(self):
        self.left.softStop()
        self.right.softStop()

def main():
    print("create motor instances")
    dualMotors=DualMotorController(0x60,0x61)
    print("current positions (act/tar/act/tar):"+str(dualMotors.getActPosTarPosMatrix()))
    dualMotors.dualSetOTPParam()
    dualMotors.dualUpdateMotorParams()
    print("running init")
    dualMotors.runInit(3000, 4000)
    time.sleep(7)
    print("current positions (act/tar/act/tar):"+str(dualMotors.getActPosTarPosMatrix()))
 
    print("turning left 90")
    dualMotors.turnLeft()
    while 1:
        tmp=dualMotors.getActPosTarPosMatrix()
        if(tmp[0][0]==tmp[0][1] and tmp[1][0]==tmp[1][1]):
            break 
        print("turning:"+str(tmp))
        time.sleep(0.1)
     
    print("current positions (act/tar/act/tar):"+str(dualMotors.getActPosTarPosMatrix()))
    print("sleeping in 3 seconds")
    time.sleep(3)
     
    print("turning 180")
    dualMotors.turn180()
    while 1:
        tmp=dualMotors.getActPosTarPosMatrix()
        if(tmp[0][0]==tmp[0][1] and tmp[1][0]==tmp[1][1]):
            break 
        print("turning:"+str(tmp))
        time.sleep(0.1)
    print("current positions (act/tar/act/tar):"+str(dualMotors.getActPosTarPosMatrix()))
    time.sleep(1)
    dualMotors.dualResettoDefault()   
     
if __name__ == '__main__':
    main()
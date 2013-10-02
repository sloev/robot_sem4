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
        
        self.posleft=0
        self.posRight=0
        
        self.left.setOTPParam()
        self.rigth.setOTPParam()
    
    def busy(self):
        leftstatus=self.left.getFullStatus2
        rightstatus=self.right.getFullStatus2
        leftstatus=(leftstatus[1]<<8 | leftstatus[2]<<0) | (leftstatus[3]<<8 | leftstatus[4]<<0)
        rightstatus=(rightstatus[1]<<8 | rightstatus[2]<<0) | (rightstatus[3]<<8 | rightstatus[4]<<0)
        return (leftstatus & rightstatus)==0
    
    def turn180(self):
        self.turn90(0, 2)
    
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

def main():
    dualMotors=DualMotorController(0x60,0x61)
    
    dualMotors.turnLeft()
    while(dualMotors.busy()):
        print("turning left")
        time.sleep(1)
    print("finished...not busy")
    
    time.sleep(1)

    dualMotors.turnRight()
    while(dualMotors.busy()):
        print("turning right")
        time.sleep(1)
    print("finished...not busy")
    
    time.sleep(1)

    dualMotors.turn180()
    while(dualMotors.busy()):
        print("turning right")
        time.sleep(1)
    print("finished...not busy")

if __name__ == '__main__':
    main()
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
        self.logger = logging.getLogger('robot.dualMotors')

        self.turn90Steps=1270
        self.turn180Steps=2540
        
        self.logger.info("Initializing DualMotorController")
        self.motorLeft = Motor_I2C(add1)
        self.motorRight = Motor_I2C(add2)
        self.positionLeft=0
        self.positionRight=0
        self.logger.info("Initializing DualMotorController DONE")

    
    def setOtpParam(self):
        self.logger.debug("setOtpParam")

        self.motorLeft.setOTPParam()
        self.motorRight.setOTPParam()
    
        
    def runInit(self):
        self.logger.info("runInit")

        self.motorLeft.runInit()
        self.motorRight.runInit()
    
    def setMotorParams(self,leftDir,rightDir,leftMaxVel,rightMaxVel):
        self.logger.info("setMotorParams")
        while True:
            try:
                self.motorLeft.setMotorParam(leftDir, leftMaxVel)
                self.motorRight.setMotorParam(rightDir, rightMaxVel)
                break
            except IOError:
                pass
        
    
    def getFullStatus1(self):
        self.logger.info("getFullStatus1")
        while True:
            try:
                var=[self.motorLeft.getFullStatus1(),self.motorRight.getFullStatus1()]
                break
            except IOError:
                pass
        return var
    
    def getFullStatus2(self):
        self.logger.info("getFullStatus2")
        while True:
            try:
                left=self.motorLeft.getFullStatus2()
                right=self.motorRight.getFullStatus2()
                break
            except IOError:
                print "GF2Error"
        var=[left,right]
        self.logger.info("/left/fullstatus2/"+str(left))
        self.logger.info("/right/fullstatus2/"+str(right))
        return var
    
    def turn90(self,direction,maxVel):
        self.logger.info('turn 90:'+str(direction))

        self.motorLeft.setMotorParam(direction, maxVel)
        self.motorRight.setMotorParam(direction, maxVel)
        
        self.setPosition(self.turn90Steps, self.turn90Steps)
        
    def turn180(self,maxVel):
        self.logger.info("turn180")

        self.motorLeft.setMotorParam(1, maxVel)
        self.motorRight.setMotorParam(1, maxVel)
        
        self.setPosition(self.turn180Steps, self.turn180Steps)
        
    def setTurnPosition(self,left,right):
        self.motorLeft.setPosition(left)
        self.motorRight.setPosition(right)

        
             
    def setPosition(self,incLeftPos,incRightPos):
        self.logger.info("setPosition"+str(incLeftPos)+","+str(incRightPos))
        fullstatus2=self.getFullStatus2()
        
        positionLeft=fullstatus2[0][1]<<8 | fullstatus2[0][2]<<0
        positionRight=fullstatus2[1][1]<<8 | fullstatus2[1][2]<<0
        
        #print(str(positionLeft)+"\t"+str(positionRight))
        
        positionLeft+=incLeftPos
        positionRight+=incRightPos
        while True:
            try:
                self.motorLeft.setPosition(positionLeft)
                self.motorRight.setPosition(positionRight)
                break
            except IOError:
                pass
        

        
    def getOfflinePosition(self):
        return [self.positionLeft,self.positionRight]
    
    def isBusy(self):
        fullstatus2=self.getFullStatus2()
        
        actLeft=fullstatus2[0][1]<<8 | fullstatus2[0][2]<<0
        actRight=fullstatus2[1][1]<<8 | fullstatus2[1][2]<<0
        
        tarLeft=fullstatus2[0][3]<<8 | fullstatus2[0][4]<<0
        tarRight=fullstatus2[1][3]<<8 | fullstatus2[1][4]<<0

        value=(actLeft==tarLeft) and (actRight==tarRight)
        
        value = not value
        #print("isbusy="+str(value))
        print str(actLeft)
        print str(tarLeft)
        self.logger.info("isBusy="+str(value))
        return value
        
    def hardStop(self):
        self.logger.info("hardStop")

        self.motorLeft.hardStop()
        self.motorRight.hardStop()
        
    def softStop(self):
        self.logger.info("softStop")
        while True:
            try:
                self.motorLeft.softStop()
                self.motorRight.softStop()
                break
            except IOError:
                pass
def main():

    motors=DualMotorController(0x60,0x61)

    times=1
    if(len(sys.argv)>2):
        speed=int(sys.argv[1])
        times=int(sys.argv[2])
        print ("times ="+str(times)  +"speed"+str(speed))      

    motors.setOtpParam()
    #print(str(motors.getFullStatus1()[0][:])+"\n"+str(motors.getFullStatus1()[1][:]))
    tmp=motors.getFullStatus2()
    #print("busy="+motors.isBusy(tmp))
    motors.setMotorParams(1, 1, speed, speed)
    motors.runInit()
    time.sleep(5)
    for i in range(0,times):
        print("turning 180")
        motors.turn180(speed)
        time.sleep(4)
        #print(str(motors.getFullStatus1()[0][:])+"\n"+str(motors.getFullStatus1()[1][:]))
        time.sleep(0.1)
        
    for i in range(0,times):
        print("turning left")
        motors.turn90(1,speed)
        time.sleep(4)
        #print(str(motors.getFullStatus1()[0][:])+"\n"+str(motors.getFullStatus1()[1][:]))
        time.sleep(0.1)

    for i in range(0,times):
        print("turning right")
        motors.turn90(0,speed)
        time.sleep(4)
        #print(str(motors.getFullStatus1()[0][:])+"\n"+str(motors.getFullStatus1()[1][:]))
        time.sleep(0.1)
    motors.setPosition(12000, 12000)
    time.sleep(10)
        
   # print(str(motors.getFullStatus1()[0][:])+"\n"+str(motors.getFullStatus1()[1][:]))

   # motors.turn90(0, 5)
    #time.sleep(6)
    #print(str(motors.getFullStatus1()[0][:])+"\n"+str(motors.getFullStatus1()[1][:]))
    #motors.setPosition(2000, 2000)

if __name__ == '__main__':
    main()
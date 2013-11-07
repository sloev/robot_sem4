'''
Created on Nov 7, 2013

@author: johannes
'''
import logging
from IR_Sensors.IR_Sensors_Controller import IR_Sensors_Controller
from Motor_control.DualMotorController import DualMotorController
from Pid import Pid
from WallsChecker import WallsChecker
from TurnThread import TurnThread
import threading
import time
import sys
import select
import os
import math

Vin1                                =   0x08
Vin2                                =   0x09
Vin3                                =   0x0A

sensorChannels=[Vin1,Vin2,Vin3]

class IterativeNavigator():
    def __init__(self):
        '''
        direction:
        if direction is 1 then the robot drives in the direction of its sensor head
        '''
        direction=1
        self.left=not direction
        self.right=direction
        self.front=2
        self.maxWidth=34

        self.minMaxSetpoint=[5,self.maxWidth,16]
        
        self.distanceInBetweenSensors=4
        self.cmPrHalfCell=30
        
        self.tuneFactor=0.1
        try:
            os.remove("/home/pi/robot_sem4/robot.log")
        except OSError:
            pass
        self.logger = logging.getLogger('robot')
        self.logger.setLevel(logging.INFO)
        
        fh = logging.FileHandler('robot.log')
        fh.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s/%(name)s/%(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        
        'sensors'
        self.ir_sensors = IR_Sensors_Controller(0x20)
        self.ir_sensors.setConfigurationRegister(0x00,0x7F)

        'motors'
        self.dual_motors=DualMotorController(0x60,0x61)
        self.dual_motors.hardStop()
        self.dual_motors.getFullStatus1()
        self.dual_motors.setOtpParam()
        self.dual_motors.setMotorParams(self.left, self.right, 2, 2)
        time.sleep(2)
        
        
        'wallchecker'
        self.wallChecker=WallsChecker(self.minMaxSetpoint,self.left,self.right,self.front)
        'turn thread'
        self.turnThread=TurnThread(self.dual_motors,self.left,self.right)

        self.lastAngle=0
        self.navigatorStopEvent=threading.Event()
        
    def runNavigator(self):
        print("making and starting nav thread")
        self.navigatorStopEvent.clear()
        self.navigatorThread=threading.Thread(target=self.navigator)
        self.navigatorThread.start()
        print ("made nav thread and started it ")
        
        
    def stopNavigator(self):
        print("stopping nav thread")
        self.navigatorStopEvent.set()
        self.navigatorThread.join()
        print("stopped and joined nav thread")
        
    def navigator(self):
        while not self.navigatorStopEvent.is_set():
            sample=self.ir_sensors.multiChannelReadCm(sensorChannels, 10)
            walls=self.wallChecker.checkWalls(sample)
            choice=self.makeChoice(walls)
            self.turnThread.checkForTurn(choice)
            
            steps=self.currentAngle(sample)
            self.drive(steps)

    def makeChoice(self,walls):
        print(str(walls))
        if(walls[self.right]==0):
            return 4
        elif(walls[self.left]==0):
            return 2
        elif(walls[self.left]==1 and walls[self.right]==1 and walls[self.front]==0):
            self.pid.reset()
            return 0
        else:
            return 0
        
    def drive(self,steps):
        self.dual_motors.setMotorParams(self.left, self.right, 2, 2)
        self.dual_motors.setPosition(steps, steps)
        while(self.dual_motors.isBusy()):
            time.sleep(0.1)
 
    def currentAngle(self,sample):
        'alt er i cm'
        lastWasLeft=self.lastAngle>0
        
        left=sample[self.left]+(self.distanceInBetweenSensors/2)
        right=sample[self.right]+(self.distanceInBetweenSensors/2)
        
        angleV=math.cos(self.maxWidth/(left+right))
        if lastWasLeft:
            direction=self.right
            lengthE=math.cos(angleV)*right
            lengthD=self.maxWidth-lengthE
            lengthC=lengthD-(self.maxWidth/2)
            lengthB=math.sqrt( ( math.pow(lengthC,2) +math.pow(self.cmPrHalfCell,2) ) )
            angleF=(math.pi/2)-math.acos( lengthC/lengthB )#!!! rigtigt?
            currentAngle=angleF+angleV
        else:
            direction=self.left
            lengthD=math.cos(angleV)*left
            lengthE=self.maxWidth-lengthD
            lengthC=lengthE-(self.maxWidth/2)
            lengthB=math.sqrt( ( math.pow(lengthC,2) +math.pow(self.cmPrHalfCell,2) ) )
            angleF=math.acos( lengthC / lengthB )
            currentAngle=angleF+angleV

        self.dual_motors.setMotorParams(direction, direction, 1, 1)
        steps=self.dual_motors.stepsData.radiansToSteps(currentAngle)
        self.drive(steps)
        self.lastAngle=currentAngle
        
        return self.dual_motors.stepsData.cmToSteps(lengthB)

        
def main():
    navigator = IterativeNavigator()
    print("init'ed navigator")
    navigator.runNavigator()
    print("running navigator")
    time.sleep(20)
    print("stopping navigator")
    navigator.stopNavigator()
    print("navigator stopped")
    pass
if __name__ == '__main__':
    main()
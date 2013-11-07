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

class IterativeNavigation():
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
        self.distanceInBetweenSensors=4
        self.cmPrHalfCell=self.stepstoCm(2000)
        
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
        
        'pid and direction'
        self.pid=Pid(self.left,self.right,self.ir_sensors, self.dual_motors)
        
        'wallchecker'
        self.wallChecker=WallsChecker(self.pid.getMinMaxSetpoint(),self.left,self.right,self.front)
        self.lastAngle=0
        
    def driveStraight(self,steps):
        self.dual_motors.setMotorParams(self.left, self.right, 2, 2)
        self.dual_motors.setPosition(steps, steps)
        while(self.dual_motors.isBusy()):
            self.logger.info("turning")
            time.sleep(0.1)
    def cmToSteps(self):
        pass
    def stepstoCm(self,steps):
        'todo!!!'
        return 30 
    
    def retOp(self):
        self.lastAngle=currentAngle
        
    def radiansToSteps(self,radians):
        steps=808.5071*radians
        return steps

    def currentAngle(self,):
        'alt er i cm'
        lastWasLeft=self.lastAngle>0
        sample=self.ir_sensors.multiChannelReadCm(sensorChannels, 3)
        
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
        steps=self.radiansToSteps(currentAngle)
        self.lastAngle=currentAngle
        self.dual_motors.setPosition(steps,steps)
        
    def turn(self):
        pass
def main():
    pass
if __name__ == '__main__':
    pass
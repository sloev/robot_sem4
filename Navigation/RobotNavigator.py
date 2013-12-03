#!/usr/bin/python
# -*- coding: ascii -*-
'''
Created on Oct 15, 2012

@author: johannes
'''
import logging
from IR_Sensors.IR_Sensors_Controller import IR_Sensors_Controller
from Motor_control.DualMotorController import DualMotorController
from Navigation.StepCounter import StepCounter
from Maze.Mapping import Mapping
from Pid import Pid
from WallsChecker import WallsChecker
from TurnThread import TurnThread
import threading
import time
import json
from Network.ZeroconfServer import ZeroconfTcpServer

import os

Vin1                                =   0x08
Vin2                                =   0x09
Vin3                                =   0x0A

sensorChannels=[Vin1,Vin2,Vin3]


class RobotNavigator():
    '''
        used to tune the pid gain factors using keyboard input
        press q to save
        
        tune    wheel    +    -        
        pGain   left     a    z
        pGain   right    s    x
        
        iGain   left     d    c
        iGain   right    f    v
        
        dGain   left     g    b
        dGain   right    h    n
           
    '''
    stepsPrCell=6000
    def __init__(self):
        '''
        direction:
        if direction is 1 then the robot drives in the direction of its sensor head
        '''
        
        self.mode=1#mapping mode
        self.firstCell=True
        direction=1
        self.left=not direction
        self.right=direction
        self.front=2
        setPoint=14.9
        cmMaxPid=35
        cmMaxWallChecker=26
        cmMin=5


        self.Lock=threading.Event()
        self.Lock.clear()#locks for tcp communication

        self.server=ZeroconfTcpServer()
        self.server.addHandler("maze", self.sendMaze)
        self.server.addHandler("path", self.receivePath)
        self.server.addHandler("currentPosition", self.sendCurrentPosition)
        self.server.initThreads()
        self.server.start()
        try:
            os.remove("/home/pi/robot_sem4/robot.log")
        except OSError:
            pass
        logger = logging.getLogger('robot')
        logger.setLevel(logging.INFO)
        
        fh = logging.FileHandler('robot.log')
        fh.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s/%(name)s/%(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        inited=False
        while not inited:
            try:
                'sensors'
                self.ir_sensors = IR_Sensors_Controller(0x20)
                #self.ir_sensors.setConfigurationRegister(0x00,0x7F)
        
                'motors'
                self.dual_motors=DualMotorController(0x64,0x61)
                self.dual_motors.hardStop()
                self.dual_motors.getFullStatus1()
                self.dual_motors.setOtpParam()
                self.dual_motors.setMotorParams(self.left, self.right, 2, 2)
                self.dual_motors.resetPosition()
                #self.dual_motors.runInit()
                time.sleep(2)
                
                'pid and direction'
                self.pid=Pid(self.left,self.right,self.ir_sensors, self.dual_motors,cmMin,cmMaxPid,setPoint)
                
                'wallchecker'
                self.wallChecker=WallsChecker(self.left,self.right,self.front,cmMin,cmMaxWallChecker,setPoint)
                
                'turnThread'
                self.turnThread=TurnThread(self.ir_sensors,self.wallChecker,self.dual_motors,self.left,self.right)
                
                'StepCounter'
                self.stepCounter = StepCounter()
                
                'Mapping'
                self.mapping = Mapping()
                
                'load gainfactors'
                gainfactors=self.pid.getGainFactors()
                self.pGain=gainfactors[0]
                self.dGain=gainfactors[1]
                self.iGain=gainfactors[2]
                
                'stateMachineThread'
                self.stateThread=threading.Thread(target=self.doMapping)
                self.stateThread.daemon = True
                self.stateThread.start()
                inited=True
            except IOError as e:         
                print("error in doPid: "+str(e))
                
    def printGains(self):
        print("gains="+str(self.pid.getGainFactors()))
       
    def doPathing(self):
        print "running Paathing thread"
        mode=1
        first=True
        while not self.Lock.is_set():
            #print "no lock"
            self.Lock.wait(0.001)
            try:
                self.dual_motors.setMotorParams(self.left, self.right, 1, 1)
                sample=self.ir_sensors.multiChannelReadCm(sensorChannels,1)
                walls=self.wallChecker.checkWalls(sample)
                #print "has sampled"
                if mode:
                    self.dual_motors.setPosition(32767, 32767)
                if walls==[1,1,0] and not first and self.dual_motors.isBusy():
                    if mode:
                        self.dual_motors.setPosition(32767, 32767)
                    sample=self.ir_sensors.multiChannelReadCm(sensorChannels,1)
                    walls=self.wallChecker.checkWalls(sample)  
                    self.pid.doPid(sample)
                    self.Lock.wait(0.001)
                else:
                    #print "making choice"
                    choice=self.mapping.getChoice()
                    print choice
                    if choice==[0,0]:
                        #print "out of mode 2 clearet lock"
                        self.Lock.set()
                    else:
                        if not first:
                            self.turnThread.checkForTurn(-1)
                        self.turnThread.checkForTurn(choice[1])
                        self.pid.reset()
                        mode=1
                            
                        if choice[0]!=0:
                            steps=choice[0]-self.stepsPrCell/2
                            self.dual_motors.setMotorParams(self.left, self.right, 1, 1)
                            self.dual_motors.setPosition(steps,steps)
                            mode=0
                    first=False
            except IOError as e:         
                print("error in doPid: "+str(e))
        print "closing Paathing thread"
      
    def doMapping(self):
        print "running mapping thread"
        while not self.Lock.is_set():
            self.Lock.wait(0.001)
            try:
                print "start sampling section"
                sample=self.ir_sensors.multiChannelReadCm(sensorChannels,1)
                walls=self.wallChecker.checkWalls(sample)  
                self.dual_motors.setMotorParams(self.left, self.right, 1, 1)
    
                print "end of sampling section"
                print walls
                if(walls==[1, 1, 0]):
                    self.stepCounter(self.dual_motors.setPosition(32767, 32767))
                    self.pid.doPid(sample)
                else:  
                    steps=self.stepCounter.getSteps()
                    if self.firstCell:
                        steps-=self.stepsPrCell
                        self.firstCell=False
                    print steps

                    self.turnThread.checkForTurn(-1)
                    sample=self.ir_sensors.multiChannelReadCm(sensorChannels,1)
                    walls=self.wallChecker.checkWalls(sample)  
                    choice = self.mapping.getChoice(steps,walls)
                    self.turnThread.checkForTurn(choice)

                    if not choice:
                        print "mapped Ok waiting for instructions\n heres the maze:"
                        print self.mapping.getMaze()
                        print "lock cleared in mode 1"
                        self.Lock.set()
                    self.pid.reset()
                    if walls==[1,1,1]:
                        self.stepCounter.resetSteps(-800)
                    self.stepCounter.resetSteps()
                    self.dual_motors.resetPosition()
            except IOError as e:         
                print("error in doPid: "+str(e))
        print "closing mapping thread"
            
    def stop(self):
        self.Lock.set()
        self.stateThread.join()
        self.dual_motors.softStop()
        self.server.stop()

    def sendMaze(self,params=0):
        print "in sendMaze"
        if self.stateThread.is_alive():
            return json.dumps({'status':"error",'cause':"robot is busy"})
        else:
            maze=self.mapping.getMaze() 
            print "sendMaze got maze"+str(maze)
            currentPos=self.mapping.getCurrentPosition()
            print "sendMaze got current position"+str(currentPos)
            mazeDict=maze.getDict()
            print "sendMaze got dict:"+str(mazeDict)
            returner={'status':"success",'currentpos':currentPos,'maze':mazeDict}
            print "returner"+str(returner)
            return json.dumps(returner)    
        
    def sendCurrentPosition(self,params=0):
        if self.stateThread.is_alive():
            return json.dumps({'status':"error",'cause':"robot is busy"})
        else:
            currentPos=self.mapping.getCurrentPosition()
            returner= {'status':"success",'currentPosition':currentPos}
            self.Lock.clear()
            return json.dumps(returner)
    
    def receivePath(self,params=0):
        if self.stateThread.is_alive():
            return json.dumps({'status':"error",'cause':"robot is busy"})
        else:
            self.mapping.receiveStack(params)
            self.Lock.clear()
            self.stateThread=threading.Thread(target=self.doPathing)
            self.stateThread.daemon = True
            self.stateThread.start()
            print "receive path success"
            return json.dumps({'status':"success"})
            
def main():
    robot=RobotNavigator()

    print("\
        used to tune the pid gain factors using keyboard input\
        \n    npress q to save\
        \n    ntune    wheel    +    -    \
        \n    npGain   left     a    z    \
        \n    npGain   right    s    x    \
        \n    ndGain   left     d    c    \
        \n    ndGain   right    f    v    \
        \n    niGain   left     g    b    \
        \n    niGain   right    h    n    \
        ")
    try:
        robot.printGains()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        robot.stop()
        
if __name__ == '__main__':
    main()

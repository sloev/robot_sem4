'''
Created on Oct 15, 2013

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
        


        self.Lock=threading.Event()
        self.Lock.set()#locks for tcp communication

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
                self.dual_motors=DualMotorController(0x60,0x61)
                self.dual_motors.hardStop()
                self.dual_motors.getFullStatus1()
                self.dual_motors.setOtpParam()
                self.dual_motors.setMotorParams(self.left, self.right, 2, 2)
                self.dual_motors.resetPosition()
                #self.dual_motors.runInit()
                time.sleep(2)
                
                'pid and direction'
                self.pid=Pid(self.left,self.right,self.ir_sensors, self.dual_motors)
                
                'wallchecker'
                self.wallChecker=WallsChecker(self.pid.getMinMaxSetpoint(),self.left,self.right,self.front)
                
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
                inited=True
            except IOError as e:         
                print("error in doPid: "+str(e))
    def printGains(self):
        print("gains="+str(self.pid.getGainFactors()))
    
    def doPid(self):
        try:
            'start sampling section'
            sample=self.ir_sensors.multiChannelReadCm(sensorChannels,1)
            walls=self.wallChecker.checkWalls(sample)  
            self.dual_motors.setMotorParams(self.left, self.right, 1, 1)
            self.dual_motors.setAccelerations(self.left, self.right, 3)

            'end of sampling section'
            #print "walls"+str(walls)
            if self.mode==1:#mapping mode
                print "MODE 1"
                if(walls==[1, 1, 0]):
                    self.pid.doPid(sample)
                    self.stepCounter(self.dual_motors.setPosition(32767, 32767))
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
                        self.mode=0
                        print "mapped Ok waiting for instructions\n heres the maze:"
                        print self.mapping.getMaze()     
                        self.Lock.clear()#muliggor tcp communication
                    self.pid.reset()
                    if walls==[1,1,1]:
                        self.stepCounter.resetSteps(-800)
                    self.stepCounter.resetSteps()
                    self.dual_motors.resetPosition()
            elif self.mode==2:#goTo mode
                print "MODE 2"
                choice=self.mapping.getChoice()
                if choice==[0,0]:
                    self.mode=0
                    self.Lock.clear()
                else:
                    #self.turnThread.checkForTurn(-1)
                    self.turnThread.checkForTurn(choice[1])
                    self.dual_motors.setMotorParams(self.left, self.right, 1, 1)
                    self.dual_motors.setAccelerations(self.left, self.right, 3)
                    self.dual_motors.setPosition(choice[0], choice[0])
                    while self.dual_motors.isBusy():
                        self.pid.doPid(sample)
                        time.sleep(0.001)
                    self.pid.reset()
        except IOError as e:         
            print("error in doPid: "+str(e))
        
    def stop(self):
        self.dual_motors.softStop()
        self.server.stop()

    def sendMaze(self,params=0):
        print "in sendMaze"
        if self.Lock.is_set():
            return json.dumps({'status':"error",'cause':"robot is busy"})
        else:
            self.Lock.set()
            print "sendMaze got lock"
            maze=self.mapping.getMaze() 
            print "sendMaze got maze"+str(maze)
            currentPos=self.mapping.getCurrentPosition()
            print "sendMaze got current position"+str(currentPos)
            mazeDict=maze.getDict()
            print "sendMaze got dict:"+str(mazeDict)
            returner={'status':"success",'currentpos':currentPos,'maze':mazeDict}
            print "returner"+str(returner)
            self.Lock.clear()
            return json.dumps(returner)    
        
    def sendCurrentPosition(self,params=0):
        if self.Lock.is_set():
            return json.dumps({'status':"error",'cause':"robot is busy"})
        else:
            self.Lock.set()
            currentPos=self.mapping.getCurrentPosition()
            returner= {'status':"success",'currentPosition':currentPos}
            self.Lock.clear()
            return json.dumps(returner)
    
    def receivePath(self,params=0):
        if self.Lock.is_set() or not params:
            return json.dumps({'status':"error",'cause':"robot is busy"})
        else:
            self.Lock.set()
            self.mapping.receiveStack(params)
            self.mode=2
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
            time.sleep(0.001)
            robot.doPid()
    except KeyboardInterrupt:
        robot.stop()
        
if __name__ == '__main__':
    main()

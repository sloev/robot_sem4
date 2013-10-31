'''
Created on Oct 15, 2013

@author: johannes
'''
import logging
from IR_Sensors.IR_Sensors_Controller import IR_Sensors_Controller
from Motor_control.DualMotorController import DualMotorController
from Pid import Pid
from WallsChecker import WallsChecker
from TurnThread import TurnThread
from threading import Thread
import time
import sys
import select
import os

Vin1                                =   0x08
Vin2                                =   0x09
Vin3                                =   0x0A

sensorChannels=[Vin1,Vin2,Vin3]


class PidTuner():
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
    def __init__(self):
        '''
        direction:
        if direction is 1 then the robot drives in the direction of its sensor head
        '''
        direction=1
        self.left=not direction
        self.right=direction
        self.front=2
        
        self.tuneFactor=0.01
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
        
        'sensors'
        self.ir_sensors = IR_Sensors_Controller(0x20)
        self.ir_sensors.setConfigurationRegister(0x00,0x7F)

        'motors'
        self.dual_motors=DualMotorController(0x60,0x61)
        self.dual_motors.hardStop()
        self.dual_motors.getFullStatus1()
        self.dual_motors.setOtpParam()
        self.dual_motors.setMotorParams(self.left, self.right, 2, 2)
        #self.dual_motors.runInit()
        time.sleep(2)
        
        'pid and direction'
        self.pid=Pid(self.left,self.right,self.ir_sensors, self.dual_motors)
        
        'wallchecker'
        self.wallChecker=WallsChecker(self.pid.getMinMaxSetpoint(),self.left,self.right,self.front)
        
        'turnThread'
        self.turnThread=TurnThread(self.dual_motors)
        
        'load gainfactors'
        gainfactors=self.pid.getGainFactors()
        self.pGain=gainfactors[0]
        self.dGain=gainfactors[1]
        self.iGain=gainfactors[2]
        
    def lpgadd(self):
        self.pGain=[self.pGain[self.left]+self.tuneFactor,self.pGain[self.right]]
        self.pid.pTune(self.pGain)
        
    def rpgadd(self):
        self.pGain=[self.pGain[self.left],self.pGain[self.right]+self.tuneFactor]
        self.pid.pTune(self.pGain)

    def lpgsub(self):
        self.pGain=[self.pGain[self.left]-self.tuneFactor,self.pGain[self.right]]
        self.pid.pTune(self.pGain)
        
    def rpgsub(self):
        self.pGain=[self.pGain[self.left],self.pGain[self.right]-self.tuneFactor]
        self.pid.pTune(self.pGain)
    
    def ldgadd(self):
        self.dGain=[self.dGain[self.left]+self.tuneFactor,self.dGain[self.right]]
        self.pid.dTune(self.dGain)
      
    def rdgadd(self):
        self.dGain=[self.dGain[self.left],self.dGain[self.right]+self.tuneFactor]
        self.pid.dTune(self.dGain)
 
    def ldgsub(self):
        self.dGain=[self.dGain[self.left]-self.tuneFactor,self.dGain[self.right]]
        self.pid.dTune(self.dGain)
       
    def rdgsub(self):
        self.dGain=[self.dGain[self.left],self.dGain[self.right]-self.tuneFactor]
        self.pid.dTune(self.dGain)

    def ligadd(self):
        self.iGain=[self.iGain[self.left]+self.tuneFactor,self.iGain[self.right]]
        self.pid.iTune(self.iGain)
        
    def rigadd(self):
        self.iGain=[self.iGain[self.left],self.iGain[self.right]+self.tuneFactor]
        self.pid.iTune(self.iGain)
 
    def ligsub(self):
        self.iGain=[self.iGain[self.left]-self.tuneFactor,self.iGain[self.right]]
        self.pid.iTune(self.iGain)
       
    def rigsub(self):
        self.iGain=[self.iGain[self.left],self.iGain[self.right]-self.tuneFactor]
        self.pid.iTune(self.iGain)
        
    def printGains(self):
        print("gains="+str(self.pid.getGainFactors()))
    
    def save(self):
        return self.pid.pickleGainFactors()
        
    def doPid(self):
        try:
            self.printGains()
            sample=self.ir_sensors.multiChannelReadCm(sensorChannels,5)
            
            self.dual_motors.setMotorParams(self.left, self.right, 2, 2)
            self.dual_motors.setPosition(32767, 32767)
            self.pid.doPid(sample)
            
            
            walls=self.wallChecker.checkWalls(sample)  
            debounce=self.wallChecker.compareSides()   
                
            choice=self.makeChoice(walls, debounce)

            thread = Thread(target=self.turnThread.checkForTurn, args=[choice])
            thread.start()
            thread.join
     
        except IOError:
            pass

    def makeChoice(self,walls,debounce):
        if(debounce):
            if(walls[self.left]==0):
                return 4
            elif(walls[self.right]==0):
                return 2
        else:
            return 0
        
        
    def stop(self):
        self.dual_motors.softStop()
   
def main():

    pidtuner=PidTuner()

    print("\
        used to tune the pid gain factors using keyboard input\
        \    npress q to save\
        \    ntune    wheel    +    -    \
        \    npGain   left     a    z    \
        \    npGain   right    s    x    \
        \    ndGain   left     d    c    \
        \    ndGain   right    f    v    \
        \    niGain   left     g    b    \
        \    niGain   right    h    n    \
        ")
    try:
        while True:
            time.sleep(0.3)
    
            # get keyboard input, returns -1 if none available
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                c = sys.stdin.readline()
                c=c[0:1]
                print("c is =|"+c+"|")
                if(c=='a'): 
                    pidtuner.lpgadd()
                    print("left pgain inc")
                elif(c=='z'): pidtuner.lpgsub()
                elif(c=='s'): pidtuner.rpgadd()
                elif(c=='x'): pidtuner.rpgsub()
                elif(c=='d'): pidtuner.ligadd()
                elif(c=='c'): pidtuner.ligsub()
                elif(c=='f'): pidtuner.rigadd()
                elif(c=='v'): pidtuner.rigsub()
                elif(c=='g'): pidtuner.ldgadd()
                elif(c=='b'): pidtuner.ldgsub()
                elif(c=='h'): pidtuner.rdgadd()
                elif(c=='n'): pidtuner.rdgsub()
                elif(c=='q'): 
                    print("saved="+str(bool(pidtuner.save()))) 
                else: # an empty line means stdin has been closed
                    print('eof')
            pidtuner.doPid()
    except KeyboardInterrupt:
        print("saving")
        if(pidtuner.save()):
            print"saved"
        else:
            print("not saved")
        pidtuner.stop()
        
            
            
        
            
if __name__ == '__main__':
    main()
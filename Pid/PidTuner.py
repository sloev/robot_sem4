'''
Created on Oct 15, 2013

@author: johannes
'''
import logging
from IR_Sensors.IR_Sensors_Controller import IR_Sensors_Controller
from Motor_control.DualMotorController import DualMotorController
from Pid import Pid
import time
import sys
import select
import os

class PidTuner():
    '''
        used to tune the pid gain factors using keyboard input
        press q to save
        
        tune    wheel    +    -        
        pGain   left     a    z
        pGain   right    s    x
        
        dGain   left     d    c
        dGain   right    f    v
        
        iGain   left     g    b
        iGain   right    h    n
           
    '''
    def __init__(self):
        '''
        direction:
        if direction is 1 then the robot drives in the direction of its sensor head
        '''
        direction=1
        self.left=not direction
        self.right=direction
        
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
        self.ir_sensor = IR_Sensors_Controller(0x20)
        self.ir_sensor.setConfigurationRegister(0x00,0x7F)

        'motors'
        self.dual_motors=DualMotorController(0x60,0x61)
        self.dual_motors.setOtpParam()
        'pid and direction'
        self.pid=Pid(self.left,self.right,self.ir_sensor, self.dual_motors)
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
            self.dual_motors.setMotorParams(self.left, self.right, 2, 2)
            self.dual_motors.setPosition(32767, 32767)
            walls=self.pid.doPid()
            #print("[walls="+str(walls)+"]")
        
            if(walls[self.left]==0):
                self.turn(self.right)
            elif(walls[self.right]==0):
                self.turn(self.left)                
        except IOError as ex:
            pass
            #print("fuck you error\n"+str(ex))
            
    def turn(self,direction):
        #print("turning wheel="+str(direction))
        time.sleep(1)
        self.dual_motors.softStop()
        time.sleep(0.3)
        self.dual_motors.turn90(direction, 2)
        time.sleep(0.8)
        
        self.dual_motors.setMotorParams(self.left, self.right, 2, 2)
        self.dual_motors.setPosition(32767, 32767)
        '''
        driving straight until scenario in turn is overdone
        which means drive out of corner
        '''
        time.sleep(1)
        self.pid.reset()
# 
#         walls=oldWalls=self.pid.detectMissingWalls(self.pid.sampleDistances())
#         while(walls==oldWalls):
#             try:
#                 walls=self.pid.detectMissingWalls(self.pid.sampleDistances())
#             except IOError:
#                 print("got ioerror in sampling ir sensors")
#             time.sleep(0.1)
        print("turning finnished")
        
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
                elif(c=='d'): pidtuner.ldgadd()
                elif(c=='c'): pidtuner.ldgsub()
                elif(c=='f'): pidtuner.rdgadd()
                elif(c=='v'): pidtuner.rdgsub()
                elif(c=='g'): pidtuner.ligadd()
                elif(c=='b'): pidtuner.ligsub()
                elif(c=='h'): pidtuner.rigadd()
                elif(c=='n'): pidtuner.rigsub()
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
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
        
        self.left=0
        self.right=1
        self.tuneFactor=0.01
        logging.basicConfig(filename='myLog.log', level=logging.INFO)
        self.ir_sensor = IR_Sensors_Controller(0x20)
        self.ir_sensor.setConfigurationRegister(0x00,0x7F)
        self.dual_motors=DualMotorController(0x60,0x61)
        self.dual_motors.setOtpParam()
        self.pid=Pid(self.ir_sensor, self.dual_motors)
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
        print("\n"+str(self.pGain)+"\t"+str(self.dGain)+"\t"+str(self.iGain)+"\n")
    
    def save(self):
        self.pid.pickleGainFactors()
        
    def doPid(self):
        try:
            self.dual_motors.setPosition(32767, 32767)
            walls=self.pid.doPid()
            self.printGains()
            print("[walls="+str(walls)+"]")
            if(walls[self.left]==0):
                print("turning left")
                self.dual_motors.softStop()
                time.sleep(1)
                self.dual_motors.turn90(self.left, 2)
                time.sleep(3)
            elif(walls[self.right]==0):
                print("turning right")
                self.dual_motors.softStop()
                time.sleep(1)
                self.dual_motors.turn90(self.right, 2)
                time.sleep(3)
        except IOError as ex:
            print("fuck you error\n"+str(ex))
        
    def loop(self):
        while(1):
            time.sleep(0.05)
            tmp=self.pid.doPid()
   

            
            
def main():

    pidtuner=PidTuner()
    fncDict = {'a': pidtuner.lpgadd(),
               'z': pidtuner.lpgsub(),
               's': pidtuner.rpgadd(),
               'x': pidtuner.rpgsub(),
               'd': pidtuner.ldgadd(),
               'c': pidtuner.ldgsub(),
               'f': pidtuner.rdgadd(),
               'v': pidtuner.rdgsub(),
               'g': pidtuner.ligadd(),
               'b': pidtuner.ligsub(),
               'h': pidtuner.rigadd(),
               'n': pidtuner.rigsub(),
               'q': pidtuner.save()
                }
    print("\
        used to tune the pid gain factors using keyboard input\
        \npress q to save\
        \ntune    wheel    +    -     \
        \npGain   left     a    z \
        \npGain   right    s    x\
        \ndGain   left     d    c\
        \ndGain   right    f    v\
        \niGain   left     g    b\
        \niGain   right    h    n\
        ")
    while 1:
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
            elif(c=='q'): pidtuner.save()            
            else: # an empty line means stdin has been closed
                print('eof')
        pidtuner.doPid()
            
if __name__ == '__main__':
    main()
'''
Created on Oct 15, 2013

@author: johannes
'''
import logging
from IR_Sensors import IR_Sensors_Controller
from Motor_control import DualMotorController
from Pid import Pid
import time
import curses
left=0
right=1
tuneFactor=0.01
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
        logging.basicConfig(filename='myLog.log', level=logging.INFO)
        self.ir_sensor = IR_Sensors_Controller(0x20)
        self.ir_sensor.setConfigurationRegister(0x00,0x7F)
        self.dual_motors=DualMotorController(0x60,0x61)
        self.dual_motors.setOtpParam()
        self.pid=Pid(self.ir_sensors, self.dual_motors)
        gainfactors=self.pid.getGainFactors()
        self.pGain=gainfactors[0]
        self.dGain=gainfactors[1]
        self.iGain=gainfactors[2]
        
    def lpgadd(self):
        self.pGain=[self.pGain[left]+tuneFactor,self.pGain[right]]
        self.pid.pTune(self.pGain)
        
    def rpgadd(self):
        self.pGain=[self.pGain[left],self.pGain[right]+tuneFactor]
        self.pid.pTune(self.pGain)

    def lpgsub(self):
        self.pGain=[self.pGain[left]-tuneFactor,self.pGain[right]]
        self.pid.pTune(self.pGain)
        
    def rpgsub(self):
        self.pGain=[self.pGain[left],self.pGain[right]-tuneFactor]
        self.pid.pTune(self.pGain)
    
    def ldgadd(self):
        self.dGain=[self.dGain[left]+tuneFactor,self.dGain[right]]
        self.pid.dTune(self.dGain)
      
    def rdgadd(self):
        self.dGain=[self.dGain[left],self.dGain[right]+tuneFactor]
        self.pid.dTune(self.dGain)
 
    def ldgsub(self):
        self.dGain=[self.dGain[left]-tuneFactor,self.dGain[right]]
        self.pid.dTune(self.dGain)
       
    def rdgsub(self):
        self.dGain=[self.dGain[left],self.dGain[right]-tuneFactor]
        self.pid.dTune(self.dGain)

    def ligadd(self):
        self.iGain=[self.iGain[left]+tuneFactor,self.iGain[right]]
        self.pid.iTune(self.iGain)
        
    def rigadd(self):
        self.iGain=[self.iGain[left],self.iGain[right]+tuneFactor]
        self.pid.iTune(self.iGain)
 
    def ligsub(self):
        self.iGain=[self.iGain[left]-tuneFactor,self.iGain[right]]
        self.pid.iTune(self.iGain)
       
    def rigsub(self):
        self.iGain=[self.iGain[left],self.iGain[right]-tuneFactor]
        self.pid.iTune(self.iGain)
        
    def printGains(self):
        print(str(self.pGain)+"\t"+self.dGain+"\t"+self.iGain)
    
    def save(self):
        self.pid.pickleGainFactors()
    
    def loop(self):
        while(1):
            time.sleep(0.05)
            self.pid.doPid()
            
def main(stdscr):
    PidTuner=PidTuner()
    stdscr.nodelay(1)
    fncDict = {'a': PidTuner.lpgadd(),
               'z': PidTuner.lpgsub(),
               's': PidTuner.rpgadd(),
               'x': PidTuner.rpgsub(),
               'd': PidTuner.ldgadd(),
               'c': PidTuner.ldgsub(),
               'f': PidTuner.ldgadd(),
               'v': PidTuner.ldgsub(),
               'g': PidTuner.ligadd(),
               'b': PidTuner.ligsub(),
               'h': PidTuner.ligadd(),
               'n': PidTuner.ligsub(),
               'q': PidTuner.save()
                }
    while 1:
        # get keyboard input, returns -1 if none available
        c = stdscr.getch()
        if c != -1:
            fncDict.get(c, "error")()
            PidTuner.printGains()
if __name__ == '__main__':
    curses.wrapper(main)

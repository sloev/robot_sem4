'''
Created on Oct 15, 2013

@author: johannes
'''
import logging
from IR_Sensors import IR_Sensors_Controller
from Motor_control import DualMotorController
from Pid import Pid
import time

class PidTuner():
    '''
        used to tune the pid gain factors
    '''
    def __init__(self):
        logging.basicConfig(filename='mother_log.log', level=logging.INFO)
        self.ir_sensor = IR_Sensors_Controller(0x20)
        self.ir_sensor.setConfigurationRegister(0x00,0x7F)
        self.dual_motors=DualMotorController(0x60,0x61)
        self.dual_motors.setOtpParam()
        self.pid=Pid(self.ir_sensors, self.dual_motors)
        
    def loop(self):
        while(1):
            time.sleep(0.05)
            self.pid.doPid()
def main():
    PidTuner=PidTuner()
    
if __name__ == '__main__':
    pass
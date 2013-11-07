'''
Created on Nov 7, 2013

@author: johannes
'''
from DualMotorController import DualMotorController
import time as time
import logging
import sys

def main():
    motors=DualMotorController(0x60,0x61)

    motors.setOtpParam()
    tmp=motors.getFullStatus2()
    motors.setMotorParams(0,1, 2, 2)
    steps=5000
    motors.runInit()
    string="press enter to drive %d steps",steps
    while True:
        try:
            raw_input(string)
            motors.setPosition(steps, steps)
        except KeyboardInterrupt:
            break
if __name__ == '__main__':
    main()
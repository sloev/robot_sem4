'''
Created on Sep 23, 2013

@author: Daniel Machon
'''

'''
Motor commands:        Description:                                        ByteCode:

GetFullStatus1:        Returns complete status of the chip                 0x81 
GetFullStatus2:        Returns actual, target and secure position          0xFC 
GetOTPParam:           Returns OTP parameter                               0x82 
GotoSecurePosition:    Drives motor to secure position                     0x84 
HardStop:              Immediate full stop                                 0x85 
ResetPosition:         Sets actual position to zero                        0x86 
ResetToDefault:        Overwrites the chip RAM with OTP contents           0x87 
RunInit:               Reference Search                                    0x88 
SetMotorParam:         Sets motor parameter                                0x89 
SetOTPParam:           Zaps the OTP memory                                 0x90 
SetPosition:           Programmers a target and secure position            0x8B 
SoftStop:              Motor stopping with deceleration phase              0x8F
'''

import smbus
import time

class Motor_I2C:
    '''
    classdocs
    '''


    def __init__(self, devAddress):
        self.devAddress = devAddress
        self.bus = smbus.SMBus(0)
        
        '''Status of circuit and stepper motor'''
    def getFullStatus1(self):
        response = self.bus.write_byte(self.devAddress, 0x81)
        return response
        
        '''Status of the position of the stepper motor'''
    def getFullstatus2(self):
        response = self.bus.write_byte(self.devAddress, 0xFC)
        return response
    
    def getOTPParam(self):
        pass
    
    def goToSecurePosition(self):
        pass
    
    def hardStop(self):
        pass
    
    def resetPosition(self):
        pass
    
    def resetToDefault(self):
        pass
    
    def runInit(self):
        pass
    
    def setMotorParam(self):
        pass
    
    def setOTPParam(self):
        pass
    
    def setPosition(self):
        pass
    
    def softStop(self):
        pass
              
    def writeToMotor(self, value):
        self.bus.write_byte_data(self.address, 0, value)
        
    
    
        
    
def main():
    pass

if __name__== '__main__':
    main()
       
        
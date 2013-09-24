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

''' 
StepMode parameter:         Mode: 
        
00                          Half Stepping 
01                          1/4 µStepping 
10                          1/8 µStepping 
11                          1/16 µStepping
'''  

import smbus

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
        
        '''Read OTP *One-Time Programmable) memory''' 
    def getOTPParam(self):
        response = self.bus.write_byte(self.address, 0x82)
        return response
    
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
        
        '''Set the stepper motor parameters in the RAM:
          
           Byte 1: 0xFF
           Byte 2: 0xFF
           Byte 3: 7-4=Coil peak current value (Irun), 3-0=Coil hold current value (Ihold) 
           Byte 4: 7-4=Max velocity, 3-0=Min velocity
           Byte 5: 7-5=Secure position, 4=Motion direction, 3-0=Acceleration
           Byte 6: 7-0=Secure position of the stepper motor
           Byte 7: 4=Acceleration shape, 3-2=Stepmode      
        '''          
    def setMotorParam(self):          
        byteCode = bytes([0xFF, 0xFF, 0x86, 0xA4, 0x08, 0x98, 0x1C])
        self.bus.write_block_data(self.address, 0x89, byteCode)
    
        '''Drive the motor to a given position relative to 
           the zero position, defined in number of half or micro steps, 
           according to StepMode[1:0] value:
           
           Byte 1: 0xFF
           Byte 2: 0xFF
           Byte 3: 
           Byte 4: 
        '''   
    def setOTPParam(self):
        byteCode = bytes([0xFF, 0xFF, 0x00, 0x00])
        self.bus.write_block_data(self.address, 0x90 ,byteCode)
    
        
        
    def setPosition(self):
        self.bus.write_block_data(self.address, 0x8B)
        self.byteCode = bytes([0xFF, 0xFF, 0xFF, 0xFF])
    
    def softStop(self):
        pass
              
    def writeToMotor(self, value):
        self.bus.write_byte_data(self.address, 0, value)
        
    
    
        
    
def main():
    motor = Motor_I2C(0x60)
    motor.setPosition()
    

if __name__== '__main__':
    main()
       
        
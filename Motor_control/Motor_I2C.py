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
01                          1/4 Stepping 
10                          1/8 Stepping
11                          1/16 Stepping
'''  

import smbus
import time as time

class Motor_I2C:
    '''
    Stepper motor driver module.
    '''


    def __init__(self, devAddress1, devAddress2):
        self.devAddress1 = devAddress1
        self.devAddress2 = devAddress2
        self.bus = smbus.SMBus(1)
        
        '''Status of circuit and stepper motor'''
    def getFullStatus1(self):
        response1 = self.bus.read_i2c_block_data(self.devAddress1, 0x81, 11)
        response2 = self.bus.read_i2c_block_data(self.devAddress2, 0x81, 11)
        return str(response1)+"\n"+str(response2)
        
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
        self.bus.write_byte(self.devAddress1, 0x85)
        self.bus.write_byte(self.devAddress2, 0x85)
    
    def resetPosition(self):
        self.bus.write_byte(self.devAddress1, 0x86)
        self.bus.write_byte(self.devAddress2, 0x86)
    
    def resetToDefault(self):
        self.bus.write_byte(self.devAddress2, 0x87)
        self.bus.write_byte(self.devAddress2, 0x87)
    
    def runInit(self):
        byteCode1 = [0xFF, 0xFF, 0x84, 0x00, 0x50, 0xAA, 0x10]
        byteCode2 = [0xFF, 0xFF, 0x84, 0x00, 0x50, 0xAA, 0x10]
        self.bus.write_i2c_block_data(self.devAddress1, 0x88, byteCode1) 
        self.bus.write_i2c_block_data(self.devAddress2, 0x88, byteCode2)
        
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
        byteCode1 = [0xFF, 0xFF, 0x84, 0x84, 0x98, 0x00, 0x08]
        byteCode2 = [0xFF, 0xFF, 0x84, 0x84, 0x98, 0x00, 0x08]
        #byteCode = [255, 255, 96, 241, 146, 00, 28]
        self.bus.write_i2c_block_data(self.devAddress1, 0x89, byteCode1)
        self.bus.write_i2c_block_data(self.devAddress2, 0x89, byteCode2)  
         

              
    
        '''Drive the motor to a given position relative to 
           the zero position, defined in number of half or micro steps, 
           according to StepMode[1:0] value:
           
           Byte 1: 0xFF
           Byte 2: 0xFF
           Byte 3: 
           Byte 4: 
        ''' 
        
        '''Zap the One-Time Programmable memory'''  
    def setOTPParam(self):
        byteCode1 = [0xFF, 0xFF, 0xFB, 0xD5]
        byteCode2 = [0xFF, 0xFF, 0xFB, 0xD5]
        self.bus.write_i2c_block_data(self.devAddress1, 0x90, byteCode1)
        self.bus.write_i2c_block_data(self.devAddress2, 0x90, byteCode2)
        
        
        '''Drive the motors to a given position in number of
           steps or microsteps:
        '''   
    def setPosition(self):
        byteCode1 = [0xFF, 0xFF, 0xA5, 0x00]
        byteCode2 = [0xFF, 0xFF, 0xA5, 0x00]
        self.bus.write_i2c_block_data(self.devAddress1, 0x8B, byteCode1)
        self.bus.write_i2c_block_data(self.devAddress2, 0x8B, byteCode2)
    
    def softStop(self):
        self.bus.write_byte(self.devAddress1, 0x8F)
        self.bus.write_byte(self.devAddress2, 0x8F)
              
    def writeToMotor(self, value):
        self.bus.write_i2c_block_data(self.devAddress1, 0x00, 0x00)
    
    def driveAngle(self):
        pass
    
        
    
def main():
    motor = Motor_I2C(0x60, 0x61)
    motor.getFullStatus1()
    motor.setOTPParam()
    motor.setMotorParam()
    motor.runInit()        
    motor.setPosition()
    
    

if __name__== '__main__':
    main()
       
        
'''
Created on Oct 6, 2013

@author: slavegnuen
'''
from Decorators.TMC222Status import TMC222Status
import smbus
import time as time

'class variables:'

#Motor commands:        ByteCode:    Description:                                        
cmdGetFullStatus1     = 0x81       # Returns complete status of the chip 
cmdGetFullStatus2     = 0xFC       # Returns actual, target and secure position 
cmdGetOTPParam        = 0x82       # Returns OTP parameter        
cmdGotoSecurePosition = 0x84       # Drives motor to secure position 
cmdHardStop           = 0x85       # Immediate full stop 
cmdResetPosition      = 0x86       # Sets actual position to zero   
cmdResetToDefault     = 0x87       # Overwrites the chip RAM with OTP contents   
cmdRunInit            = 0x88       # Reference Search              
cmdSetMotorParam      = 0x89       # Sets motor parameter      
cmdSetOTPParam        = 0x90       # Zaps the OTP memory    
cmdSetPosition        = 0x8B       # Programmers a target and secure position 
cmdSoftStop           = 0x8F       # Motor stopping with deceleration phase 

minVelocity           = 2
stepModeByte          = 8
currentByte           = 0x52

class Motor_I2C:
    def __init__(self, devAddress):
        self.devAddress=devAddress
        self.bus = smbus.SMBus(1)

            
        '''Status of circuit and stepper motor'''
    def getFullStatus1(self):
        return self.bus.read_i2c_block_data(self.devAddress, cmdGetFullStatus1, 9)

        '''Status of circuit and stepper motor'''
    @TMC222Status    
    def printFullStatus1(self):
        return self.bus.read_i2c_block_data(0x60, 0x81, 9)

        '''Status of the position of the stepper motor'''
    def getFullStatus2(self):
        return self.bus.write_byte(self.devAddress, cmdGetFullStatus2)

        '''Read OTP *One-Time Programmable) memory''' 
    def getOTPParam(self):
        return self.bus.write_byte(self.devAddress, cmdGetOTPParam)
    
    def hardStop(self):
        self.bus.write_byte(self.devAddress, cmdHardStop)
    
    def resetPosition(self):
        self.bus.write_byte(self.devAddress, cmdResetPosition)
    
    def resetToDefault(self):
        self.bus.write_byte(self.devAddress, cmdResetToDefault)
    
    def runInit(self):
        byteCode = [0xFF, 0xFF, 0x80, 0x00, 0x50, 0xAA, 0x10]              
        self.bus.write_i2c_block_data(self.devAddress, cmdRunInit, byteCode) 
    
        '''Set the stepper motor parameters in the RAM:
          
           Byte 1: 0xFF
           Byte 2: 0xFF
           Byte 3: 7-4=Coil peak current value (Irun), 3-0=Coil hold current value (Ihold) 
           Byte 4: 7-4=Max velocity, 3-0=Min velocity
           Byte 5: 7-5=Secure position, 4=Motion direction, 3-0=Acceleration
           Byte 6: 7-0=Secure position of the stepper motor
           Byte 7: 4=Acceleration shape, 3-2=Stepmode      
        '''          
    def setMotorParam(self,direction,maxVelocity):          
        byte4=maxVelocity << 4 | minVelocity<<0 
        byte5=0x88 | direction<<4
        #byteCode = [0xFF, 0xFF, 0x32, 0x32, 0x88, 0x00, 0x08]
        byteCode = [0xFF, 0xFF, 0x32, byte4, byte5, 0x00, stepModeByte]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetMotorParam, byteCode)
    
        '''Zap the One-Time Programmable memory'''  
    def setOTPParam(self):
        byteCode = [0xFF, 0xFF, 0xFB, 0xD5]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetOTPParam, byteCode)
        
        '''Drive the motors to a given position in number of
           steps or microsteps:
        '''   
    def setPosition(self,newPosition):
        byte3,byte4=divmod(newPosition,0x100)
        byteCode = [0xFF, 0xFF, byte3, byte4]
        #byteCode = [0xFF, 0xFF, 0xAA, 0x10]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetPosition, byteCode)
        
    def softStop(self):
        self.bus.write_byte(self.devAddress, cmdSoftStop)
              
    def writeToMotor(self, value):
        self.bus.write_i2c_block_data(self.devAddress, 0x00, 0x00)
         
        
    
def main():
    motor = Motor_I2C(0x60)
    motor.setOTPParam()
    motor.setMotorParam(1,3)
    motor.runInit()        
    motor.setPosition(3000)
    
    time.sleep(3)
    
    motor = Motor_I2C(0x61)
    motor.setOTPParam()
    motor.setMotorParam(0,3)
    motor.runInit()        
    motor.setPosition(3000)
    
if __name__ == '__main__':
    pass
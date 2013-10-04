'''
Created on Sep 23, 2013

@author: Daniel Machon
eview:johannes, benjamin
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

from Decorators.TMC222Status import TMC222Status
import smbus
import time as time

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

class Motor_I2C:
    '''

    Stepper motor driver module.
    '''

    '''Constructor'''
    def __init__(self, devAddress):
        self.devAddress = devAddress
        self.bus = smbus.SMBus(1)
        self.irun=6
        self.ihold=1
        self.maxVelocity=3
        self.minVelocity=2
        self.direction=0
        
        '''This method returns the status of the circuit of the
           stepper motor'''
    def getFullStatus1(self):
        response = self.bus.read_i2c_block_data(self.devAddress, cmdGetFullStatus1, 9)
        return self.lol(response)
    
    @TMC222Status    
    def lol(self,str):
        return str
        
        '''This method returns the actual- and target position of
           the stepper motor'''
    def getFullStatus2(self):
        response = self.bus.read_i2c_block_data(self.devAddress, cmdGetFullStatus2)
        return response
    
        
        '''This method returns the content of the OTP (One Time Programmable)
           memory''' 
    def getOTPParam(self):
        response = self.bus.read_i2c_block_data(self.devAddress, cmdGetOTPParam)
        return response
    
    
    def goToSecurePosition(self):
        pass
    
    
    def hardStop(self):
        self.bus.write_byte(self.devAddress, cmdHardStop)
        
    
        '''This method resets the actual position of the stepper motor'''
    def resetPosition(self):
        self.bus.write_byte(self.devAddress, cmdResetPosition)
        
    
    def resetToDefault(self):
        self.bus.write_byte(self.devAddress, cmdResetToDefault)
        #self.bus.write_byte(self.devAddress, 0x87)
#old     def runInit(self):
#         byteCode1 = [0xFF, 0xFF, 0x80, 0x00, 0x50, 0xAA, 0x10]
#         byteCode2 = [0xFF, 0xFF, 0x80, 0x00, 0x50, 0xAA, 0x10]
#         self.bus.write_i2c_block_data(self.devAddress1, 0x88, byteCode1)
#         self.bus.write_i2c_block_data(self.devAddress2, 0x88, byteCode2)
        
    def runInit(self,position1, position2):
        position1=self.toTwoBytes(position1)
        position2=self.toTwoBytes(position2)        
        byteCode = [0xFF, 0xFF, 0x80, position1[0],position1[1],position2[0],position2[1]]              
        self.bus.write_i2c_block_data(self.devAddress, cmdRunInit, byteCode) 
         
         
        
        '''This method sets the stepper parameters in the TMC222 RAM.
           The parameters are as follows:
          
           Byte 1: 0xFF
           Byte 2: 0xFF
           Byte 3: 7-4=Coil peak current value (Irun), 3-0=Coil hold current value (Ihold) 
           Byte 4: 7-4=Max velocity, 3-0=Min velocity
           Byte 5: 7-5=Secure position, 4=Motion direction, 3-0=Acceleration
           Byte 6: 7-0=Secure position of the stepper motor
           Byte 7: 4=Acceleration shape, 3-2=Stepmode      
        '''          
    def setMotorParam(self): 
        byte3=self.irun<<4 | self.ihold<<0
        byte4=self.minVelocity<<0 | self.maxVelocity << 4
        byte5=0x88 | self.direction<<4
        byteCode = [0xFF, 0xFF, byte3, byte4, byte5, 0x00, 0x08]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetMotorParam, byteCode)
    
           
    
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
        byteCode = [0xFF, 0xFF, 0xFB, 0xD5]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetOTPParam, byteCode)
        #self.bus.write_i2c_block_data(self.devAddress, 0x90, byteCode)
        
        
        '''This methods drives the motors to a given position in number of
           steps or microsteps:
        '''   
    def setPosition(self, position):
        position=self.toTwoBytes(position)        
        byteCode = [0xFF, 0xFF, position[0],position[1]]
        self.bus.write_i2c_block_data(self.devAddress, cmdSetPosition, byteCode)
        
        
    
    def softStop(self):
        self.bus.write_byte(self.devAddress, cmdSoftStop)
        #self.bus.write_byte(self.devAddress, 0x8F)
              
    def writeToMotor(self, value):
        self.bus.write_i2c_block_data(self.devAddress, 0x00, 0x00)
    
    
    '''''''''''''''''''''''
       Additional methods:
    '''''''''''''''''''''''
        
    
    def driveAngle(self):
        pass
    
    '''
       toTwoBytes returns a list with two ints maximum value 255
    '''
    
    def toTwoBytes(self,temp):
        a,b=divmod(temp,0x100)
        return [a,b]
    
    '''
       to metoder til at satte torque for drift og stilstand lrun/lhol
    '''
    
    def setIrun(self,irun):
        self.irun=irun
    
    
    def setIhold(self,lhold):
        self.lhold=lhold
    
    def setMaxVelocity(self,maxVelocity):
        self.maxVelocity=maxVelocity
    
    def setMinVelocity(self,minVelocity):
        self.minVelocity=minVelocity
        
    def setDirection(self,direction):
        self.direction=direction
    
    
def main():
    time.sleep(5)
    
    motor1 = Motor_I2C(0x60)
    motor2 = Motor_I2C(0x61)
            
    motor1.setOTPParam()
    motor2.setOTPParam()
    #time.sleep(2)
    
    motor1.setMotorParam(0,3,2)
    motor2.setMotorParam(1,3,2)
    #time.sleep(2)
    position=20000
    
    print("runInit:")
    motor1.runInit(100,200)  
    motor2.runInit(100,200)  
    time.sleep(7)
    
    motor2.setPosition(position)
    motor1.setPosition(position)

    for i in range(0,15):
        returner=motor2.getFullStatus2()
        #position+=16
        #motor2.setPosition(position)
        motor2.setMotorParam(1,(i%5)+1,2)

        str1="length="+str(len(returner))+"\t"+hex(returner[0])+"\t"+str(returner[1]<<8 | returner[2]<<0 )+"\t"+str(returner[3]<<8 | returner[4]<<0 )+"\t"+hex(returner[5])+"\t"+hex(returner[6])+"\t"+hex(returner[7])
        #str1="\t".join(map(hex, returner))
        print(str1)
        time.sleep(1)
        
        
        
    for j in range(0,25):
        returner=motor2.getFullStatus2()
        position+=2500
        motor2.setPosition(position)
        str1="length="+str(len(returner))+"\t"+hex(returner[0])+"\t"+str(returner[1]<<8 | returner[2]<<0 )+"\t"+str(returner[3]<<8 | returner[4]<<0 )+"\t"+hex(returner[5])+"\t"+hex(returner[6])+"\t"+hex(returner[7])
        #str1="\t".join(map(hex, returner))
        print(str1)
        time.sleep(1)

  

if __name__== '__main__':
    main()
       
        

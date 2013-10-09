'''
Created on Oct 8, 2013

@author: Daniel Machon
'''

'''''''''''''''''''''''''''''''''''''''''''''''''''''
This class handles converted input from the Sharp IR ' 
Sensors                                              ' 
'''''''''''''''''''''''''''''''''''''''''''''''''''''

slaveAddress = 0x20

import smbus

 
 
#Read/Write registers               #byteCode 4 LSB's
ConversionResultReg                 =   0x00
AlertStatusReg                      =   0x01
ConfigurationReg                    =   0x02
CycleTimerReg                       =   0x03        
DataLowRegCH1                       =   0x04
DataHighRegCH1                      =   0x05
HysteresisRegCH1                    =   0x06
DataLowRegCH2                       =   0x07
DataHighRegCH2                      =   0x08
HysteresisRegCH2                    =   0x09
DataLowRegCH3                       =   0x0A
DataHighRegCH3                      =   0x0B
HysteresisRegCH3                    =   0x0C
DataLowRegCH4                       =   0x0D
DataHighRegCH4                      =   0x0E
HysteresisRegCH4                    =   0x0F

#Channels                           "ByteCode" 4 MSB's
NotSelected                         =   0x00
Vin1                                =   0x08
Vin2                                =   0x09
Vin3                                =   0x0A
Vin4                                =   0x0B
Vin5                                =   0x0C
Vin6                                =   0x0D
Vin7                                =   0x0E
Vin8                                =   0x0F
multiChannels                       =   0x07


class IR_Sensors_Controller():
    
    
    def __init__(self):
        self.bus = smbus.SMBus(1)
        
        
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Select the sequence of channels to read                  Chan
    D11  D10  D9   D8   |    D7   D6   D5  D4              
    0    0    0    0    |    0    0    0    1                Vin1
    0    0    0    0    |    0    0    1    0                Vin2
    0    0    0    0    |    0    1    0    0                Vin3        
    0    0    0    0    |    1    0    0    0                Vin4
    0    0    0    1    |    0    0    0    0                Vin5
    0    0    1    0    |    0    0    0    0                Vin6
    0    1    0    0    |    0    0    0    0                Vin7
    1    0    0    0    |    0    0    0    0                Vin8
    
    
    Byte 1 = 0000+D11+D10+D9+D8
    Byte 2 = D7+D6+D5+D4+1+AlertEN+Busy/Alert+Alert/BusyPolatiry
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def setConfigurationRegister(self, MSBs, LSBs):
        global ConfigurationReg, multiChannels
        chosenRegister = ConfigurationReg | multiChannels << 4
        byte1 = MSBs
        byte2  = 0x0F | LSBs << 4
        self.bus.write_i2c_block_data(slaveAddress, chosenRegister,[byte1, byte2])
        
    
    
    '''Read input from IR sensor'''
    def readSensor(self, channel, register):
        chosenRegister = register | channel << 4
        self.bus.write_byte(slaveAddress, chosenRegister)
        sensorInput = self.bus.read_byte(slaveAddress)
        return sensorInput
    
    
def main():
    test = IR_Sensors_Controller()
    inp1 = test.readSensor(Vin1, DataHighRegCH1)
    print inp1
    inp2 = test.readSensor(Vin1, DataLowRegCH1)
    print inp2
    inp3 = test.readSensor(Vin1, HysteresisRegCH1)
    print inp3
    inp4 = test.readSensor(Vin2, DataHighRegCH2)
    print inp4
    inp5 = test.readSensor(Vin2, DataLowRegCH2)
    print inp5
    inp6 = test.readSensor(Vin2, HysteresisRegCH2)
    print inp6
    inp7 = test.readSensor(Vin3, DataHighRegCH3)
    print inp7
    inp8 = test.readSensor(Vin3, DataLowRegCH3)
    print inp8
    inp9 = test.readSensor(Vin3, HysteresisRegCH3)
    print inp9
    inp10 = test.readSensor(Vin4, DataHighRegCH4)
    print inp10
    inp11 = test.readSensor(Vin4, DataLowRegCH4)
    print inp11
    inp12 = test.readSensor(Vin4, HysteresisRegCH4)
    print inp12
    
    
    
if __name__== '__main__':
    main() 
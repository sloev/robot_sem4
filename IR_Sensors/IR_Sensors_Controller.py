'''
Created on Oct 8, 2013

@author: Daniel Machon, 
        Johannes
'''

'''''''''''''''''''''''''''''''''''''''''''''''''''''
This class handles converted input from the Sharp IR ' 
Sensors                                              ' 
'''''''''''''''''''''''''''''''''''''''''''''''''''''
from RangeTable import RangeTable
import smbus
import time as time
import logging
 
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

lastSamples = [14.9, 14.9, 0, 0]


class IR_Sensors_Controller():
    
    
    '''
        Constructor
    '''
    def __init__(self, slaveAddress):
        self.logger=logging.getLogger("robot.IrSensorsController")
        self.bus = smbus.SMBus(1)
        self.slaveAddress = slaveAddress
        self.rangeTable=RangeTable.unpickleTable()
        if(self.rangeTable==0):
            self.rangeTable=RangeTable()
           
        
        
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
    
    
    '''
        Configure the configurationregister. Can be used to read from
        a sequence of channels automatically.
    '''
    def setConfigurationRegister(self, MSBs, LSBs):
        chosenRegister = ConfigurationReg | multiChannels << 4
        byte1 = MSBs
        byte2  = 0x0F | LSBs << 4
        self.bus.write_i2c_block_data(self.slaveAddress, chosenRegister,[byte1, byte2])
        
    
    '''
        Read input from IR sensor
    '''
    def readSensorBlock(self, channel, register):
        chosenRegister = register | channel << 4
        try:
            sensorInput=self.bus.read_i2c_block_data(self.slaveAddress,chosenRegister, 2)
        except IOError:
            print 'Error in ReadSensorBlock'
            
        return sensorInput
    
        
    '''
        Extract the raw distance from the 2 received bytes (12 LSB's)
    '''
    def extractRawDistance(self,sensorRead):
        le=len(sensorRead)

        if(le>1):
            tmp=(sensorRead[0] & 0b00001111) <<8 | sensorRead[1]<<0
            return int(tmp)
        return -1
    
        
    '''
        takes sensorRead as param and returns the distance in cm float
    '''
    def lookupCm(self,rawDistance):
        if (rawDistance>0):
            return self.rangeTable.lookUpDistance(rawDistance)
        return -1
    
    '''
        takes sensorRead as param and returns the alerts from a conversion
    '''
    def getAlerts(self,sensorRead):
        if(len(sensorRead)>1):
            alert=sensorRead[0] >> 7
            return alert
        return -1
    
    
    '''
        Read average measurement from a single sensor
    '''
    def getAverageInCm(self,channel,amount):
        average=0
        for i in range(0,amount):
            tmp = self.readSensorBlock(channel, ConversionResultReg)
            tmp = self.extractRawDistance(tmp)
            average+=tmp
            time.sleep(0.10)
        return self.lookupCm(int(average/amount))
    
    
    '''
        Read input from channels described in the channels list
        Returns a list with sensor distances in cm
    '''
    def multiChannelReadCm(self,channels, amount):
        
        distances = [0 for i in range(len(channels)+1)]
        global lastSamples
        for i in range(amount):
            for j in range(len(distances)-1):
                reading = self.extractRawDistance(self.readSensorBlock(channels[j], ConversionResultReg))
                value = self.lookupCm(reading)
                
                if(j == 0 or j == 1):
                    if(value > lastSamples[j]+4):
                        print 'GAP'
                        value = 14.9
                        distances[j] += value
                        
                        if(j == 0):
                            distances[len(channels)+1] = 1
                        if(j == 1):
                            distances[len(channels)+1] = 2 
                        
                        lastSamples[j] = value
                    
                    else:
                        print 'OK'
                        distances[j] += value
                        lastSamples[j] = value
                else:
            
                    distances[j] += value
                    lastSamples[j] = value

                      
                if(amount-i==1):
                    distances[j]=(int(distances[j]/amount))
                    print distances
        self.logger.info("sampleAverage/"+str(distances))   
        return distances
    
    
    '''
        Print the content of the distance list (Redundant!)
    '''
    def printMultiChannelReadCm(self,distances):
        print("sensor readout in cm:")
        for i in range(len(distances)):
            print("sensor "+str(i)+"\t\t")
        for i in range(len(distances)):
            print(str(distances[i]))
        
    
    
def main():
    IR_sensor = IR_Sensors_Controller(0x20)
    IR_sensor.setConfigurationRegister(0x00,0x7F)
    sensorChannels=[Vin1,Vin2,Vin3]

    while(1):
        print IR_sensor.multiChannelReadCm(sensorChannels,5)
        time.sleep(0.2)
        
            
if __name__== '__main__':
    main() 
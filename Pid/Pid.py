'''
Created on Oct 15, 2013

@author: slavegnuen
'''
Vin1                                =   0x08
Vin2                                =   0x09
Vin3                                =   0x0A
class Pid():
    '''
    creates a a conversion ookup table from sharp ir adc values to centimeters 
    using an approximated linear equation based on mesurements
    
    adcmax sAEtter hvilken spEndevide vi kan opleve adc outputted i
    '''

    def __init__(self,ir_sensors, dual_motors):
        self.ir_sensors=ir_sensors
        self.dual_motors=dual_motors
        self.setPoint=10
        self.cmMax=20
        self.cmMin=5
        self.sensorChannels=[Vin1,Vin2,Vin3]

        '''left and right'''
        self.right=1
        self.left=0
        self.lastError=[0,0] #last error 
        self.currentError=[0,0]
        self.dError=[0,0] #differential error
        self.iError=[0,0]
        self.pGain=[0,0]  #proportional gain factor
        self.dGain=[0,0]  #differential gain factor
        self.controlValues=[0,0]
        
    def doPd(self):
        sample=self.ir_sensors.multiChannelReadCm(self.sensorChannels,5)
        self.error=[self.setPoint-sample[self.left],self.setPoint-sample[self.right]]
        
        self.dError=[self.error[self.left]-self.lastError[self.left],self.error[self.right]-self.lastError[self.right]]
        
        
    def constrain(self,cm):
        if(cm > self.cmMax):
            return self.cmMax
        elif(cm < self.cmMin):
            return self.cmMin
        return cm
    
    def convertCmToVelocity(self,cm):
        velocity=((cm/(self.cmMax-self.cmMin))*6)+1
        return velocity
        
if __name__ == '__main__':
    pass
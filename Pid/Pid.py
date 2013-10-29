'''
Created on Oct 15, 2013

@author: Johannes Jorgensen
'''

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'PID control                                                                                '
'Inspired by:                                                                               ' 
'http://letsmakerobots.com/node/865                                                         '
'                                                                                           ' 
'Uses three sharp ir sensors connected through i2c with ad7998 ad-converter                 '
'and for output it uses two stepper motors                                                  '
'                                                                                           '
'If self.left =0 and self.right=1 it will drive towards the direction of its sensor head    '
'                                                                                           ' 
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import logging
import cPickle as pickle
import os.path

Vin1                                =   0x08
Vin2                                =   0x09
Vin3                                =   0x0A

sensorChannels=[Vin1,Vin2,Vin3]

class Pid():

    '''
        Constructor
    '''
    def __init__(self,left,right,ir_sensors, dual_motors):
        self.left=left
        self.right=right
        self.front=2
        
        self.logger = logging.getLogger('robot.pid')
        self.logger.info("Initializing Pid")
        self.ir_sensors=ir_sensors
        self.dual_motors=dual_motors
        self.setPoint=16
        self.cmMax=25
        self.cmMin=5
        
        self.lastError=[0,0] #last error 
        self.iError=[0,0]
        
        '''gain factors'''
        self.pGain=[0,0]  #proportional gain factor
        self.dGain=[0,0]  #differential gain factor
        self.iGain=[0,0]  #integral gain factor
        gainFactors=self.unpickleGainFactors()

        if(gainFactors==0):           
            self.logger.info("gainFactors not unpickled")
        else:
            self.pGain=gainFactors[0]
            self.dGain=gainFactors[1]
            self.iGain=gainFactors[2]
            self.logger.info("gainFactors loaded from pickle")
        self.logger.info("Initializing Pid DONE")
        
    '''
        Resets the integral error
    '''
    def reset(self):
        self.logger.info("/resetting ierrors")
        self.iError=[0,0]
        
    '''
        PID controller:
        calculates errors according to setpoint
        sends calculated new velocities to motors
    '''    
    def doPid(self):

        self.logger.info("Doing pid")
        self.sampleDistances()
        
        walls=self.detectMissingWalls(self.sample)
        self.logger.info("walls/"+str(walls))
        self.left

        if(walls[self.left] == 1 and walls[self.right] ==1 ):
            pError=[self.setPoint-self.sample[self.right],self.setPoint-self.sample[self.left]] 
            #print("currentError:"+str(currentError))            
            
            dError=[pError[self.left]-self.lastError[self.left],pError[self.right]-self.lastError[self.right]]
            
            controlValues=[self.computeControlValues(self.left,pError,dError),self.computeControlValues(self.right,pError,dError)]
            
            self.lastError=pError
            self.iError=[pError[self.left]+self.iError[self.left] , pError[self.right]+self.iError[self.right]]
            
            self.setMotors(controlValues)
            
            self.logger.info("left/controlValues/%d",controlValues[self.left])
            self.logger.info("right/controlValues/%d",controlValues[self.right])
            
            self.logger.info("left/pError/%f",pError[self.left])
            self.logger.info("right/pError/%f",pError[self.right])
            
            self.logger.info("left/iError/%f",self.iError[self.left])
            self.logger.info("right/iError/%f",self.iError[self.right])
            
            self.logger.info("left/dError/%f",dError[self.left])
            self.logger.info("right/dError/%f",dError[self.right])
 
        else:
            msg="walls missing at:"
            if(walls[self.left]==0):
                msg+=" self.left "
            if(walls[self.right]==0):
                msg+=" self.right "
            self.logger.info(msg)
        self.logger.info("Doing pid DONE")
        return walls
    
    
    '''
        Get input from the three IR-sensors
    '''
    def sampleDistances(self):
        self.sample=self.ir_sensors.multiChannelReadCm(sensorChannels,5)
        self.logger.info("sample:"+str(self.sample))
        #print("sample="+str(self.sample))
        
        
    '''
        Set the motor parameters
    '''
    def setMotors(self,controlValues):

        if((controlValues[self.left]>=5 or controlValues[self.right]>=5) and self.sample[self.front] < self.setPoint/2):
            self.dual_motors.setMotorParams(self.left, self.right, controlValues[self.right], controlValues[self.left])
            self.logger.info("/setMotors/frontSensorLarge/"+str(controlValues))
        else:
            self.dual_motors.setMotorParams(self.left, self.right, controlValues[self.left], controlValues[self.right])
            self.logger.info("/setMotors/frontSensorIgnored/"+str(controlValues))
#         self.dual_motors.setMotorParams(self.left, self.right, controlValues[self.left], controlValues[self.right])
#         self.logger.info("/setMotors/frontSensorIgnored/"+str(controlValues))

        #print("control values="+str(controlValues))
        
    '''
        Use the input from IR-sensors to determine if any side
        walls are missing
    '''
    def detectMissingWalls(self,sample):
        walls=[1,1,0]
        if(sample[self.left]>self.cmMax):
            walls[self.left]=0
        if(sample[self.right]>self.cmMax):
            walls[self.right]=0
        if(sample[self.front]<self.setPoint):
            walls[self.front]=1
        return walls  
      
    '''
        Tunes the proportional gain
    '''
    def pTune(self,pGain):
        if(pGain[self.left]==0):
            self.pGain=[self.pGain[self.left],pGain[self.right]]
        elif(pGain[self.right]==0):
            self.pGain=[pGain[self.left],self.pGain[self.right]]
        else:
            self.pGain=pGain
        self.logger.info("pTune new pGain:"+str(self.pGain))

            
    '''
        Tunes the derivative gain
    '''
    def dTune(self,dGain):
        if(dGain[self.left]==0):
            self.dGain=[self.dGain[self.left],dGain[self.right]]
        elif(dGain[self.right]==0):
            self.dGain=[dGain[self.left],self.dGain[self.right]]
        else:
            self.dGain=dGain
        self.logger.info("pTune new dGain:"+str(self.dGain))

      
    '''
        Tunes the integral gain
    '''
    def iTune(self,iGain):
        if(iGain[self.left]==0):
            self.iGain=[self.iGain[self.left],iGain[self.right]]
        elif(iGain[self.right]==0):
            self.iGain=[iGain[self.left],self.iGain[self.right]]
        else:
            self.iGain=iGain
        self.logger.info("pTune new iGain:"+str(self.iGain))
        
        
    '''
        Fetch current gain factors
    '''
    def getGainFactors(self):
        return [self.pGain,self.iGain,self.dGain]

            
    '''
        Computes the overall error using the PID controller algorithm
    '''
    def computeControlValues(self,wheel,pError,dError):
        value=self.pGain[wheel]*pError[wheel]
        value+=self.dGain[wheel]*dError[wheel]
        value+=self.iGain[wheel]*self.iError[wheel]
        value=self.convertCmToVelocity(value)
        return value
    
        
    '''
        Checks if the overall error is within a certain threshhold
    '''
    def constrain(self,cm):
        if(cm > self.cmMax-self.setPoint):
            return self.cmMax-self.setPoint
        elif(cm < self.cmMin-self.setPoint):
            return self.cmMin-self.setPoint
        return cm
    
    
    ''' 
        input cm is ranged from -10 to 10
    '''
    
    def convertCmToVelocity(self,cm):
        #print("raw cm ="+str(cm))
        #cm=self.constrain(cm)
        #print("soft cm="+str(cm))
        value=2
        if(cm < -0.5):
            if(cm < -0.5 and cm > -2):
                value=3
            elif(cm < -2 and cm > -4):
                value=4  
            elif(cm < -4 and cm > -10):
                value=5 
            elif(cm < -10 and cm > - self.setPoint):
                value=6     
        return value
    
    '''
        Serializes gain-factors
    '''
    def pickleGainFactors(self):
        gainFactors=[self.pGain,self.dGain,self.iGain]
        try:
            pickle.dump(gainFactors, open("PidGainFactors.p", "wb"), protocol=-1)
            return 1
        except IOError:
            pass
        return 0     
     
      
    '''
        Deseriallizes gain-factors
    '''
    def unpickleGainFactors(self):
        returnValue=0
        if(os.path.exists("PidGainFactors.p")):
            try:
                returnValue = pickle.load(open("PidGainFactors.p", "rb"))
            except EOFError:
                print("Error unpickling pid")
        return returnValue
        
def main():
    pass

if __name__ == '__main__':
    pass
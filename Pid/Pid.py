'''
Created on Oct 15, 2013

@author: johannes
'''
import logging
import cPickle as pickle
import os.path


Vin1                                =   0x08
Vin2                                =   0x09
Vin3                                =   0x0A

right=1
left=0

sensorChannels=[Vin1,Vin2,Vin3]

class Pid():
    '''
    pid control
    inspired by:
    http://letsmakerobots.com/node/865
    
    uses three sharp ir sensors connected through i2c with ad7998 ad-converter
    and for output it uses two stepper motors
    '''

    def __init__(self,ir_sensors, dual_motors):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing Pid")
        self.ir_sensors=ir_sensors
        self.dual_motors=dual_motors
        self.setPoint=10
        self.cmMax=20
        self.cmMin=5
        
        self.lastError=[0,0] #last error 
        self.iError=[0,0]
        
        '''gain factors'''
        gainFactors=self.unpickleGainFactors()
        self.pGain=[0,0]  #proportional gain factor
        self.dGain=[0,0]  #differential gain factor
        self.iGain=[0,0]  #integral gain factor
        if(gainFactors==0):           
            self.logger.debug("gainFactors not unpickled")
        else:
            self.pGain=gainFactors[0]
            self.dGain=gainFactors[1]
            self.iGain=gainFactors[2]
            self.logger.debug("gainFactors loaded from pickle")
        self.logger.debug("Initializing Pid DONE")
        
    '''
        doPid:
        calculates errors according to setpoint
        sends calculated new velocities to motors
    '''
    def doPid(self):
        self.logger.debug("Doing pid")
        sample=self.ir_sensors.multiChannelReadCm(sensorChannels,5)
        self.logger.info("sample:"+str(sample))
        walls=self.detectMissingWalls(sample)
        if(walls==[1,1]):
            currentError=[self.setPoint-sample[left],self.setPoint-sample[right]] 
            self.logger.info("currentError:"+str(currentError))
            
            dError=[currentError[left]-self.lastError[left],currentError[right]-self.lastError[right]]
            self.logger.info("dError:"+str(dError))        
            
            controlValues=[self.computeControlValues(left,currentError,dError),self.computeControlValues(right,currentError,dError)]
            self.logger.info("controlValues:"+str(controlValues))
            
            self.lastError=currentError
            self.iError=[currentError[left]+self.iError[left],currentError[right]+self.iError[right]]
            self.logger.info("iError:"+str(self.iError))
            
            self.setMotors(controlValues)
        else:
            msg="walls missing at:"
            if(walls[left]==0):
                msg+=" left "
            if(walls[right]==0):
                msg+=" right "
            self.logger.warning(msg)
        self.logger.debug("Doing pid DONE")
        return walls
    
    def setMotors(self,controlValues):
        self.dual_motors.setMotorParams(1, 0, controlValues[left], controlValues[right])
    
    def detectMissingWalls(self,sample):
        walls=[1,1]
        if(sample[left]>self.cmMax):
            walls[left]=0
        elif(sample[left]>self.cmMax):
            walls[right]=0
        return walls
    
    def pTune(self,pGain):
        if(pGain[left]==0):
            self.pGain=[self.pGain[left],pGain[right]]
        elif(pGain[right]==0):
            self.pGain=[pGain[left],self.pGain[right]]
        else:
            self.pGain=pGain
        self.logger.debug("pTune new pGain:"+str(self.pGain))

            
    def dTune(self,dGain):
        if(dGain[left]==0):
            self.dGain=[self.dGain[left],dGain[right]]
        elif(dGain[right]==0):
            self.dGain=[dGain[left],self.dGain[right]]
        else:
            self.dGain=dGain
        self.logger.debug("pTune new dGain:"+str(self.dGain))

        
    def iTune(self,iGain):
        if(iGain[left]==0):
            self.iGain=[self.iGain[left],iGain[right]]
        elif(iGain[right]==0):
            self.iGain=[iGain[left],self.iGain[right]]
        else:
            self.iGain=iGain
        self.logger.debug("pTune new iGain:"+str(self.iGain))
    
    def getGainFactors(self):
        return [self.pGain,self.dGain,self.iGain]

            
    def computeControlValues(self,wheel,currentError,dError):
        value=self.pGain[wheel]*currentError[wheel]
        value+=self.dGain[wheel]*dError[wheel]
        value+=self.iGain[wheel]*self.iError[wheel]
        value=self.convertCmToVelocity(value)
        return value
        
    def constrain(self,cm):
        if(cm > self.cmMax):
            return self.cmMax
        elif(cm < self.cmMin):
            return self.cmMin
        return cm
    
    def convertCmToVelocity(self,cm):
        cm=self.constrain(cm)
        velocity=((cm/(self.cmMax-self.cmMin))*6)+1
        return velocity
    
    def pickleGainFactors(self):
        gainFactors=[self.pGain,self.dGain,self.iGain]
        pickle.dump(gainFactors, open("PidGainFactors.p", "wb"), protocol=-1)
        
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
'''
Created on Sep 16, 2013

@author: johannes, ivo, daniel
'''

import cPickle as pickle
import math
import os.path

adcMax=3000
class RangeTable:
    '''
    creates a a conversion ookup table from sharp ir adc values to centimeters 
    using an approximated linear equation based on mesurements
    
    adcmax sAEtter hvilken spEndevide vi kan opleve adc outputted i
    '''

    def __init__(self):
        self.lookupTable = self.unpickleTable()
        
        if(self.lookupTable==0):
            self.initLookupTable()
            self.pickleTable()
        
    def initLookupTable(self):
        for i in range (0,adcMax):
            self.lookupTable.extend([self.calcAdcToCm(i)])
            
        '''praecis conversion skal indsaettes'''
    def calcAdcToCm(self,adc):
        a =       46.25  ;
        b =   -0.004601  ;
        c =       22.92  ;
        d =  -0.0007897 ;
        
        cm = a*math.exp(b*adc) + c*math.exp(d*adc)
        return cm
            
    def lookUpDistance(self,adc):
        if(adc>0 and adc <adcMax):
            return self.lookupTable[adc]
        return -1
    
    def pickleTable(self):
        pickle.dump(self, open("rangeTable.p", "wb"), protocol=-1)
        
    @staticmethod
    def unpickleTable():
        returnValue=0
        if(os.path.exists("rangeTable.p")):
            try:
                returnValue = pickle.load(open("rangeTable.p", "rb"))
            except EOFError:
                pass
        return returnValue

def main():
    LUT = RangeTable()
    print(LUT.lookupCM(900))
    
if __name__== '__main__':
    main()
    
        
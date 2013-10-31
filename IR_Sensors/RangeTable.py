'''
Created on Sep 16, 2013

@author: Johannes, Ivo, Daniel
'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'This class creates a conversion lookup table from the Sharp IR ADC values,    '
'and converts them to centimeters using an approximated linear equation,       '
'based on measurements.                                                        '    
'                                                                              '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''    


import cPickle as pickle
import math
import os.path


class RangeTable():

    '''
        Constructor
    '''
    def __init__(self):
        self.adcMax=3000
        self.lookupTable = []
        self.initLookupTable()
        self.pickleTable()
        
    '''
        Create a lookup table for all possible distances
    '''
    def initLookupTable(self):
        self.lookupTable = []
        for i in range (0,self.adcMax):
            self.lookupTable.extend([self.calcAdcToCm(i)])
            
       
    '''
        Convert the ADC input to centimeters
    '''        
    def calcAdcToCm(self,adc):
        a =       46.25  ;
        b =   -0.004601  ;
        c =       22.92  ;
        d =  -0.0007897 ;
        
        cm = a*math.exp(b*adc) + c*math.exp(d*adc)
        return cm
            
    
    '''
        Perform a table lookup
    '''
    def lookUpDistance(self,adc):
        if(adc>0 and adc <self.adcMax):
            return self.lookupTable[adc]
        return -1
    
    '''
        Serialize the lookup table
    '''
    def pickleTable(self):
        pickle.dump(self, open("rangeTable.p", "wb"), protocol=-1)
        
    
    '''
        Deseriallize lookup table
    '''
    @staticmethod
    def unpickleTable():
        returnValue=0
        if(os.path.exists("rangeTable.p")):
            try:
                returnValue = pickle.load(open("rangeTable.p", "rb"))
            except EOFError:
                print "Error"
        return returnValue


def main():
    LUT = RangeTable.unpickleTable()
    if(LUT==0):
        LUT=RangeTable()
    print(LUT.lookUpDistance(900))
    
if __name__== '__main__':
    main()
    
        
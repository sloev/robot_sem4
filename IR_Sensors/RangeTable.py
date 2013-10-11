'''
Created on Sep 16, 2013

@author: johannes, ivo
'''

import cPickle as pickle
import math

adcMax=3000
class RangeTable:
    '''
    creates a a conversion ookup table from sharp ir adc values to centimeters 
    using an approximated linear equation based on mesurements
    
    adcmax sAEtter hvilken spEndevide vi kan opleve adc outputted i
    '''

    def __init__(self):
        self.lookupTable = []      
        self.initLookupTable()
        
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
        "{0:.4f}".format(cm)
        return cm
            
    def lookUpDistance(self,adc):
        if(adc>0 and adc <adcMax):
            return self.lookupTable[adc]
        return -1
    
    def LookUpDistances(self, distances):
        result = [self.lookupTable[distances[0]], self.lookupTable[distances[1]], self.lookupTable[distances[2]]]
        return result
    
    def pickleTable(self):
        pickle.dump(self, open("rangeTable.p", "wb"), protocol=-1)
        
    @staticmethod
    def unpickleTable():
        RangeTable = pickle.load(open("rangeTable.p", "rb"))
        return RangeTable

def main():
    LUT = RangeTable.unpickleTable()
    print(LUT.lookupCM(900))
    
if __name__== '__main__':
    main()
    
        
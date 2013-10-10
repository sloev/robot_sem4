'''
Created on Sep 16, 2013

@author: johannes
'''

import cPickle as pickle

adcMax=512
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
        return 1
            
    def lookupCm(self,adc):
        return self.lookupTable[adc]
                
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
    
        
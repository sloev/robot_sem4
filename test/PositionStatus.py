'''
Created on Oct 2, 2013

@author: Daniel Machon
'''

from Decorators.TMC222Status import TMC222Status

class PositionStatus(object):
    '''
    classdocs
    '''


    def __init__(self):
        pass
        
    @TMC222Status
    def getFullStatus1(self):
        r = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x0F, 0x8B, 0xFF, 0xFF]
        return r
 
def main():      
    Posi = PositionStatus()
    Posi.getFullStatus1()
        
if __name__== '__main__':
    main()         
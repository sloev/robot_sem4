'''
Created on Sep 16, 2013

@author: machon
@review: johannes
'''

from numpy import *
import math
from Mouse import Mouse
from decimal import *

Table = empty((256,256), dtype=object)

class LookUpTable:
    '''
    Creates an array of Mouse objects, that each contains
    x,y coordinates an angle and a length
    '''
    

    def __init__(self):
        global Table
        entries = 0

        for x in range(0, 255):
            newx = x-128
            for y in range(0, 255):
                newy = y-128
                if(newx!=0 and newy!=0):
                    angle = float(math.atan(Decimal(newy)/Decimal(newx)))     
                    if(angle==0 or angle==math.pi):
                        length=math.fabs(newx)
                    else:                          
                        length = math.fabs((newy)/(math.sin(angle)))
                        Table[x][y] = Mouse(newx,newy,angle,length)
                    #print(Table[x][y].toString())
                    #entries = entries + 1          
                    print(Table[x][y].toString())
        #print(entries)
        
        
        def getTable(self):
            return Table
        
                           
            

def main():

    app = LookUpTable()

    
if __name__== '__main__':
    main()
    
        
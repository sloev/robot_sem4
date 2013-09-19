'''
Created on Sep 16, 2013

@author: machon
@review: johannes, benjamin
'''

from numpy import *
import math
from Mouse import Mouse
from decimal import *

angLenTable = empty((256,256), dtype=object)
cosTable = empty((1,512),dtype=object)

class LookUpTable:
    '''
    Creates an array of Mouse objects, that each contains
    x,y coordinates an angle and a length
    '''
    

    def __init__(self):
        initCosTable()
        initAngLenTable()
        
        def initCosTable(self):
            global cosTable
            for i in range (0,511):
                cosTable[i]=cos(i*(math.pi/512))
            
        def initAngLenTable(self):
            global angLenTable
#            entries = 0

            for y in range(0, 255):
                newy = y-128
                for x in range(0, 255):
                    newx = x-128
                    if(newx!=0 and newy!=0):
                        angle = float(math.atan(Decimal(newy)/Decimal(newx)))     
                        if(angle==0 or angle==math.pi):
                            length=math.fabs(newx)
                        else:                          
                            length = math.fabs((newy)/(math.sin(angle)))
                            #angLenTable[x][y] = Mouse(newx,newy,angle,length)
                            angLenTable[x][y] = angle,length
        
        def getCos(angle):
            index=round(angle*(1/(math.pi/512)))
            return cosTable[index]
        
        def getAngLen(x,y):
            return angLenTable[x][y]
        
        def printAngLenTable(self):
            for y in range (0,255):
                for x in range(0,255):
                    print(angLenTable[x][y].toString())

        

def main():

    app = LookUpTable()

    
if __name__== '__main__':
    main()
    
        
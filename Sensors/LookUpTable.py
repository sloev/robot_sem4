'''
Created on Sep 16, 2013

@author: machon
@review: johannes, benjami
'''

from numpy import array,empty
import math
from Mouse import Mouse
from decimal import *

angLenTable = empty((256,256), dtype=object)
cosTable = empty((512),dtype=object)

class LookUpTable:
    '''
    Creates an array of Mouse objects, that each contains
    x,y coordinates an angle and a length
    '''
    

    def __init__(self):
        self.initCosTable()
        self.initAngLenTable()
        
    def initCosTable(self):
#        global cosTable
        for i in range (0,512):
            cosTable[i]=math.cos(i*(math.pi/512))
            
    def initAngLenTable(self):
 #       global angLenTable
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
                        angLenTable[x][y] = Mouse(newx,newy,angle,length)
                        #angLenTable[x][y] = array([angle,length])
                else:
                    angLenTable[x][y]=Mouse(0,0,0,0)
    def getCos(self,angle):
        index=round(angle*(1/(math.pi/512)))
        return cosTable[index]
        
    def getAngLen(self,x,y):
        a=angLenTable[x][y]
        return a
        
    def printAngLenTable(self):
        for y in range (0,255):
            for x in range(0,255):
                print(angLenTable[x][y].toString())

        

def main():

    app = LookUpTable()

    
if __name__== '__main__':
    main()
    
        
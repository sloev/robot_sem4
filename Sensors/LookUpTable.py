'''
Created on Sep 16, 2013

@author: machon
@review: johannes, benjamin
'''

from numpy import array,empty
import math
from Mouse import Mouse
from decimal import Decimal
import cPickle as pickle

class LookUpTable:
    '''
    Creates an array of Mouse objects, that each contains
    x,y coordinates an angle and a length
    '''
    

    def __init__(self):
        self.angLenTable = empty((256,256), dtype=object)
        self.cosTable = empty((512),dtype=object)        
        self.initCosTable()
        self.initAngLenTable()
        
    def initCosTable(self):
#        global cosTable
        for i in range (0,512):
            self.cosTable[i]=math.cos(i*(math.pi/512))
            
    def initAngLenTable(self):

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
                        self.angLenTable[x][y] = Mouse(newx,newy,angle,length)
                else:
                    self.angLenTable[x][y]=Mouse(0,0,0,0)
                    
    
    def getCos(self,angle):
        index=round(angle*(1/(math.pi/512)))
        return self.cosTable[index]
    
        
    def getAngLen(self,x,y):
        x+=128
        y+=128
        a=self.angLenTable[x][y]
        
        return a
        
    def printAngLenTable(self):
        for y in range (0,255):
            for x in range(0,255):
                print(self.angLenTable[x][y].toString())
                
                
    def pickleTable(self):
        pickle.dump(self, open("table.p", "wb"), protocol=-1)
        
        
    @staticmethod
    def unpickleTable():
        LookUpTable = pickle.load(open("table.p", "rb"))
        return LookUpTable
        
        
    def toString(self):
        return self.angLenTable.shape                  
        
        

def main():
   
    Table = LookUpTable.unpickleTable()
    mus2 = Table.getAngLen(129,129)
    print mus2.toString()
    
    if(isinstance(mus2, Mouse)):
        print "Yes"
    else:
        print "No"
 
    
    
if __name__== '__main__':
    main()
    
        
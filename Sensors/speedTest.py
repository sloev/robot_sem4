'''
Created on Oct 8, 2013

@author: machon
'''
from numpy import array,empty
import math
from decimal import Decimal
from Mouse import Mouse
import timeit

if __name__ == '__main__':

    angLenTable = empty((256,256), dtype=object)
    
    def foo():
        angLenTable = empty((256,256), dtype=object)

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
                else:
                    angLenTable[x][y]=Mouse(0,0,0,0)
    
    def calcAngLen(x,y):
        angle = float(math.atan(Decimal(y)/Decimal(x)))
        length = math.fabs(x)
                    
    def getAngLen(x,y):
        x+=128
        y+=128
        a=angLenTable[x][y]
        
        return a
                    
t1 = timeit.Timer(stmt="foo()", setup="from __main__ import foo")
print t1.timeit(1)
t2 = timeit.Timer(stmt="getAngLen(100, 100)", setup="from __main__ import getAngLen")
print t2.timeit(1)
t3 = timeit.Timer(stmt="calcAngLen(100, 100)", setup="from __main__ import calcAngLen")
print t3.timeit(100)
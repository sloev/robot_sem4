'''
Created on Sep 16, 2013

@author: machon
'''

from numpy import *
import math

class LookUpTable:
    '''
    classdocs
    '''


    def __init__(self):

        table = arange(65536).reshape(256,256)
        for x in range(1, 256):
            newx = x-129
            for y in range(1, 256):
                newy = y-129
                alpha = math.atan(newy/newx)                                  
                #arcLength = math.fabs((newx/newy)/math.sin(alpha));
                tuple = (math.degrees(alpha))
                table[x][y] = tuple
                print(tuple) 
        pass
                           
            

def main():
    app = LookUpTable()
    

    
if __name__== '__main__':
    main()
    
        
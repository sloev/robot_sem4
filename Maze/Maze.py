'''
Created on Nov 12, 2013

@author: johannes
'''
from collections import defaultdict
class Maze():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.table=defaultdict(dict)
    
    def set(self,x,y,value):
        self.table[x][y]=value
        
    def get(self,x,y):
        return self.table[x][y]
    
    def __str__(self): 
        string=""
        for x in range(len(self.table)):
            for y in range(len(self.table[0])):
                string+=str(self.table[x][y])+"\t"
            string+="\n"
        return string
        
    
'''
Created on Nov 12, 2013

@author: johannes
'''
from collections import defaultdict

class Maze():
    '''
    classdocs
    '''
    def __init__(self,table=None):
        self.table=defaultdict(lambda:defaultdict(int))
        if table!=None:
            xRange=len(table)
            yRange=len(table[str(0)])
            for y in range(yRange):
                for x in range(xRange):
                    self.set(x, y, table[str(x)][str(y)])
            self.width= len(self.table)
            self.height=len(self.table[0])
                    
    def set(self,x,y,value):
        self.table[x][y]=value
        self.width= len(self.table)
        self.height=len(self.table[0])

    def getWidth(self):
        return len(self.table)

    def getHeight(self):
        return len(self.table[0])
    
    def get(self,x,y):
        if self.table[x][y]:
            return self.table[x][y]
        return 0
    
    def getDict(self):
        return self.table
    
    def __str__(self): 
        string=""
        for y in range(self.getHeight()):
            for x in range(self.getWidth()):
                string+=str(self.get(x, y))+"      \t"
            string+="\n"
        return string
    
        
    
'''
Created on Nov 14, 2013

@author: johannes
'''

class Node():
    '''
    classdocs
    '''
    def __init__(self,x,y,walls,cornerExtraCost,straightCost):
        '''
        Constructor
        '''
        self.cornerExtraCost=cornerExtraCost
        self.straightCost=straightCost
        self.walls=walls
        self.x=x
        self.y=y
        self.visited=False
        
        self.g = 0
        self.origCost=0
        self.h = 0
        self.parent = None
        
    def moveCost(self, otherNode,currentParrent):
        cost=self.straightCost
        if currentParrent!=None:
            if(abs(currentParrent.x - otherNode.x) != 0 and abs(currentParrent.y - otherNode.y) != 0):
                cost+=self.cornerExtraCost
        return cost
    
    def __str__(self):
        string="["+str(self.x)+","+str(self.y)+"]"
        return string
        
            
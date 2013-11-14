'''
Created on Nov 14, 2013

@author: johannes
'''

class Node():
    '''
    classdocs
    '''
    def __init__(self,x,y,walls,cornerExtraCost=0.5,straightCost=2):
        '''
        Constructor
        '''
        self.cornerExtraCost=cornerExtraCost
        self.straightCost=straightCost
        self.walls=walls
        self.x=x
        self.y=y
        
        self.g = 0
        self.h = 0
        self.parent = None
        
    def move_cost(self, otherNode):
        corner = abs(self.x - otherNode.x) != 0 or abs(self.y - otherNode.y) != 0
        cost=self.straightCost
        if corner:
            cost+=self.cornerExtraCost
        return cost
    
    def __str__(self):
        return "[%d,%d]"%(self.x,self.y)
        
            
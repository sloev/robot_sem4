'''
Created on Nov 14, 2013

@author: johannes
'''

class Node():
    '''
    classdocs
    '''
    cornerExtraCost=0.5
    straightCost=2
    
    def __init__(self,x,y,walls):
        '''
        Constructor
        '''
        self.walls=walls
        self.x=x
        self.y=y
        
        self.g = 0
        self.h = 0
        self.parent = None
        
    def move_cost(self, otherNode):
        corner = abs(self.x - otherNode.x) != 0 or abs(self.y - otherNode.y) != 0
        cost=0
        cost+=self.straightCost
        if corner:
            cost+=self.cornerCost
        
            
'''
Created on Nov 14, 2013

@author: johannes
'''

class Node():
    '''
    classdocs
    '''
    def __init__(self,x,y,direction,cornerExtraCost,straightCost):
        '''
        Constructor
        '''
        self.cornerExtraCost=cornerExtraCost
        self.straightCost=straightCost
        self.direction
        self.x=x
        self.y=y
        self.cost
        
        self.g = 0
        self.f=-1
        self.h=0
        self.parent = None
        self.directionToMe=None
        
    def moveCost(self, node,dirToNode):
        cost=self.straightCost
        if not dirToNode==self.directionToMe and self.directionToMe!=None:
            cost+=self.cornerExtraCost
#         if currentParrent!=None:
#             if(abs(currentParrent.x - otherNode.x) != 0 and abs(currentParrent.y - otherNode.y) != 0):
#                 cost+=self.cornerExtraCost
        return cost
    
    def __str__(self):
        string="["+str(self.x)+","+str(self.y)+"]"
        return string
        
            
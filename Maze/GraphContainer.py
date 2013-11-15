'''
Created on Nov 14, 2013

@author: johannes
'''
from itertools import product
from Node import Node
class GraphContainer():
    '''
    classdocs
    '''
    def __init__(self,mazeModel,cornerExtraCost,straightCost):
        '''
        Constructor
        '''
        self.graph={}
        self.mazeModel=mazeModel
        self.nodes=[[Node(x,y,mazeModel.get(x,y),cornerExtraCost,straightCost) for y in range(mazeModel.getHeight())] for x in range(mazeModel.getWidth())]                                                                                      
        for x, y in product(range(self.mazeModel.width), range(self.mazeModel.height)):        
            node = self.nodes[x][y]
            self.graph[node] = []
        self.make()
        
    def make(self):
        for x, y in product(range(self.mazeModel.width), range(self.mazeModel.height)):        
            node = self.nodes[x][y]
            walls=node.walls
            if not((walls & 0b1000) >>3):#north
                self.graph[self.nodes[x][y]].append(self.nodes[x][y-1])
                self.graph[self.nodes[x][y-1]].append(self.nodes[x][y])                
            if not ((walls & 0b0100) >>2):#east
                self.graph[self.nodes[x][y]].append(self.nodes[x+1][y])
                self.graph[self.nodes[x+1][y]].append(self.nodes[x][y])
            if not ((walls & 0b0010) >>1):#south
                self.graph[self.nodes[x][y]].append(self.nodes[x][y+1])
                self.graph[self.nodes[x][y+1]].append(self.nodes[x][y])
            if not (walls & 0b0001):#west
                self.graph[self.nodes[x][y]].append(self.nodes[x-1][y])
                self.graph[self.nodes[x-1][y]].append(self.nodes[x][y])
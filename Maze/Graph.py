'''
Created on Nov 14, 2013

@author: johannes
'''
from itertools import product
from Node import Node
class Graph():
    '''
    classdocs
    '''
    def __init__(self,mazeModel):
        '''
        Constructor
        '''
        self.mazeModel=mazeModel()
        self.nodes=[[Node(x,y,mazeModel.get(x,y)) for y in range(mazeModel.getHeight())] for x in range(mazeModel.getWidth())]                                                                                      
        self.graph = {}
        
    def make(self):
        for x, y in product(range(self.mazeModel.width), range(self.mazeModel.height)):        
            node = self.nodes[x][y]
            walls=node.walls
            self.graph[node] = []
            if not((walls & 0b1000) >>3):#north
                self.graph[self.nodes[x][y]].append(self.nodes[x][y-1])
            if not ((walls & 0b0100) >>2):#east
                self.graph[self.nodes[x][y]].append(self.nodes[x+1][y])
            if not ((walls & 0b0010) >>1):#south
                self.graph[self.nodes[x][y]].append(self.nodes[x][y+1])
            if not (walls & 0b0001):#west
                self.graph[self.nodes[x][y]].append(self.nodes[x-1][y])
                
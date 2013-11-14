'''
Created on Nov 14, 2013

@author: johannes
'''
from GraphContainer import GraphContainer
class Astar():
    '''
    classdocs
    '''


    def __init__(self,mazeModel):
        '''
        Constructor
        '''
        cornerExtraCost=0.5
        straightCost=2
        graphContainer=GraphContainer(mazeModel,cornerExtraCost,straightCost)
        self.nodes=graphContainer.nodes
        self.graph=graphContainer.graph
        print "made maze"
        
    def heuristic(self, currentNode, endNode):
        #manhattan heuristic
        #corner = abs(self.x - otherNode.x) != 0 or abs(self.y - otherNode.y) != 0
        hx=abs(currentNode.x-endNode.x)
        hy=abs(currentNode.y-endNode.y)
        return hx+hy

    def search(self, startx,starty, endx,endy):
        start=self.nodes[startx][starty]
        end=self.nodes[endx][endy]
        
        openset = set()
        closedset = set()
        current = start
        openset.add(current)
        while openset:
            current = min(openset, key=lambda o:o.g + o.h)
            if current == end:
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent
                path.append(current)
                return path[::-1]#baglaens
            openset.remove(current)
            closedset.add(current)
            for node in self.graph[current]:
                if node in closedset:
                    continue
                if node in openset:
                    new_g = current.g + current.move_cost(node)
                    if node.g > new_g:
                        node.g = new_g
                        node.parent = current
                else:
                    node.g = current.g + current.move_cost(node)
                    node.h = self.heuristic(node, end)
                    node.parent = current
                    openset.add(node)
        return None
 

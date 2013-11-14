'''
Created on Nov 14, 2013

@author: johannes
'''
from GraphContainer import GraphContainer
from Path import Path
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

    def search(self, sourceNode,targetNode):
        start=self.nodes[sourceNode[0]][sourceNode[1]]
        end=self.nodes[targetNode[0]][targetNode[1]]
        
        openset = set()
        closedset = set()
        current = start
        openset.add(current)
        while openset:
            current = min(openset, key=lambda o:o.g + o.h)
            if current == end:
                path = Path()
                while current.parent:
                    path.append(current)
                    current = current.parent
                path.append(current)
                return path
            openset.remove(current)
            closedset.add(current)
            for node in self.graph[current]:
                if node in closedset:
                    continue
                if node in openset:
                    new_g = current.g + current.moveCost(node,current.parent)
                    if node.g > new_g:
                        node.g = new_g
                        node.parent = current
                else:
                    node.g = current.g + current.moveCost(node,current.parent)
                    node.h = self.heuristic(node, end)
                    node.parent = current
                    openset.add(node)
        return None
 

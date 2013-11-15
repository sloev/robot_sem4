'''
Created on Nov 14, 2013

@author: johannes
http://www.python.org/doc/essays/graphs.html
http://stackoverflow.com/questions/4159331/python-speed-up-an-a-star-pathfinding-algorithm
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
        cornerExtraCost=1.5
        self.straightCost=2
        graphContainer=GraphContainer(mazeModel,cornerExtraCost,self.straightCost)
        self.nodes=graphContainer.nodes
        self.graph=graphContainer.graph
        print "made maze"
        
    def heuristic(self, currentNode, endNode):
        #manhattan heuristic
        #corner = abs(self.x - otherNode.x) != 0 or abs(self.y - otherNode.y) != 0
        hx=abs(currentNode.x-endNode.x)*(self.straightCost*2)
        hy=abs(currentNode.y-endNode.y)*(self.straightCost*2)
        return hx+hy

    def retracePath(self,c):
        def parentgen(c):
            while c:
                yield c
                c = c.parent
        result = [element for element in parentgen(c)]
        path=Path(result)
        return path
    
    def search(self,sourceNode,targetNode):
        start=self.nodes[sourceNode[0]][sourceNode[1]]
        end=self.nodes[targetNode[0]][targetNode[1]]
        start.h=self.heuristic(start, end)

        openList = set()
        closedList = set()
        openList.add(start)
        while openList:
            current = sorted(openList, key=lambda inst:inst.g)[0]
            if current == end:
                return self.retracePath(current)
            openList.remove(current)
            closedList.add(current)
            for node in self.graph[current]:
                if node not in closedList:
                    newG = current.g + current.moveCost(node,current.parent)
                    if node in openList and newG >= node.g:
                        continue
                    if node not in openList or newG < node.g:             
                        node.g=newG
                        node.g = current.g + current.moveCost(node,current.parent)
                        node.h = self.heuristic(node, end)#(abs(targetNode.x-tile.x)+abs(targetNode.y-tile.y))*10 
                        openList.add(node)
                        node.parent = current
        return Path()

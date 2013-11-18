'''
Created on Nov 14, 2013

@author: johannes
http://www.python.org/doc/essays/graphs.html
http://forrst.com/posts/Dijkstras_algorithm_in_Python-B4U
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
        self.cornerExtraCost=0
        self.straightCost=2
        graphContainer=GraphContainer(mazeModel,self.cornerExtraCost,self.straightCost)
        self.nodes=graphContainer.nodes
        self.graph=graphContainer.graph
        self.gain=1
        print "made maze"
        
    def heuristic(self, currentNode, endNode):
        #manhattan heuristic
        #corner = abs(self.x - otherNode.x) != 0 or abs(self.y - otherNode.y) != 0
        hx=abs(currentNode.x-endNode.x)
        hy=abs(currentNode.y-endNode.y)
        value=(self.gain*self.straightCost)*(hx+hy)
        if hx>0:
            value+=self.cornerExtraCost*2
        if hy>0:            
            value+=self.cornerExtraCost*2
        return value

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
        start.g=0
        start.f=start.g+self.heuristic(start, end)
        end.f=-1
        
        openList.add(start)
        visited=[]
        while openList:
            current = sorted(openList, key=lambda inst:inst.f)[0]
            visited.append(current)
            if current == end:
                return [self.retracePath(current),visited]
            openList.remove(current)
            closedList.add(current)
            
            for nodePair in self.graph[current]:
                node=nodePair[0]
                nodeDir=nodePair[1]
                g_score = current.g + current.moveCost(node,nodeDir)
                h_score=self.heuristic(node, end)
                f_score = g_score + h_score
                if node in closedList and f_score >= node.f:
                    continue
                if node not in openList or f_score < node.f or nodeDir==current.directionToMe or current.directionToMe==None:
                    node.parent = current
                    node.directionToMe=nodeDir
                    node.g=g_score
                    node.f=f_score
                    node.h=h_score
                    if node not in openList:  
                        openList.add(node)
        return [None,visited]
  
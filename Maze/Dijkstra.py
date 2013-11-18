'''
Created on Nov 18, 2013

@author: johannes
'''
from collections import defaultdict
from Path import Path
class Node():
    def __init__(self,x,y,d):
        self.x=x
        self.y=y
        self.d=d
        self.prev=None
        self.visited=False
        self.cost=100000
        
    def costTo(self,node):
        cost=1
        tmp=node.d-2
        if tmp < 0 :
            tmp=3-abs(tmp)
        if tmp!=self.d:
            cost=cost+1
        return cost
    def __str__(self):
        string="[%d,%d,%d]"%(self.x,self.y,self.d)
        return string

class Graph():
    def __init__(self,mazeModel):
        self.mazeModel=mazeModel
        self.nodes=defaultdict(lambda:defaultdict(lambda:defaultdict(int)))
        self.graph={}
        self.distances=set()
        self.straightCost=1
        self.cornerCost=3
        self.makeWAR()
        
    def __str__(self):
        string=""
        for y in range(self.mazeModel.height):
            for x in range(self.mazeModel.width):
                string=string+"["
                for d in range(4):
                    if self.nodes[x][y][d]:
                        node=self.nodes[x][y][d]
                        string=string+str(node.d)+","
                    else:
                        string=string+"x,"
                string=string+"]\t"
            string=string+"\n"
        return string
    
    def getD(self,walls):
        if not((walls & 0b1000) >>3):#north
            return 1
        elif not ((walls & 0b0100) >>2):#east
            return 1
        elif not ((walls & 0b0010) >>1):#south
            return 1
        elif not (walls & 0b0001):#west
            return 1
        else:
            return 0
    def makeWAR(self):          
        for y in range(self.mazeModel.getHeight()):
            for x in range(self.mazeModel.getWidth()):  
                walls=self.mazeModel.get(x,y)   
#                string=""+ bin(walls)
                for d in range(4):
                    tmp=1
                    if not (walls &(1<<(3-d))):
                        tmp=0
                   # string = string + ","+str(tmp)
                    #print string
                    self.nodes[x][y][d]=Node(x,y,tmp)
                    self.graph[self.nodes[x][y][d]]=[]
                for i in range(4):
                    for j in range(4):
                        cost=self.straightCost
                        if(abs(i-j)!=2):
                            cost=self.cornerCost
                        if i!=j:
                            if self.nodes[x][y][i] and self.nodes[x][y][j]:
                                self.graph[self.nodes[x][y][i]].append((self.nodes[x][y][j],cost))
                                self.graph[self.nodes[x][y][j]].append((self.nodes[x][y][i],cost))   
                            
        for y in range(self.mazeModel.getHeight()):
            for x in range(self.mazeModel.getWidth()):
                #east
                if(self.nodes[x][y][1] and self.nodes[x+1][y][3]):
                    if(self.nodes[x][y][1].d!=1 and self.nodes[x+1][y][3].d!=1):
                        self.graph[self.nodes[x][y][1]].append((self.nodes[x+1][y][3],self.straightCost))
                        self.graph[self.nodes[x+1][y][3]].append((self.nodes[x][y][1],self.straightCost))
                    
                if(self.nodes[x][y][2] and self.nodes[x][y+1][0]):
                    if(self.nodes[x][y][2].d!=1 and self.nodes[x][y+1][0].d!=1):
                        self.graph[self.nodes[x][y][2]].append((self.nodes[x][y+1][0],self.straightCost))
                        self.graph[self.nodes[x][y+1][0]].append((self.nodes[x][y][2],self.straightCost)) 
                    
class Dijkstra():
    def __init__(self,mazeModel):

        self.mazeModel=mazeModel
        self.graphObj=Graph(self.mazeModel)
        #print self.graphObj
        self.graph=self.graphObj.graph
        self.nodes=self.graphObj.nodes


    def retracePath(self,c):
        def parentgen(c):
            while c:
                yield c
                c = c.prev
        result = [element for element in parentgen(c)]
        path=Path(result)
        return path
           
    def search(self,source,target):
        self.source=source
        self.target=target
        #print self.nodes
        openList=set()

        for i in range(4):
            if self.nodes[self.source[0]][self.source[1]][i]:
                self.nodes[source[0]][source[1]][i].cost=0
                self.start=self.nodes[source[0]][source[1]][i]
                openList.add(self.start)

        for i in range(4):
            if self.nodes[self.target[0]][self.target[1]][i]:
                self.end=self.nodes[target[0]][target[1]][i]
                break
        visited=[]
        closedList = set()

        while openList:
            current = sorted(openList, key=lambda inst:inst.cost)[0]
            #print current
            if current.x==self.end.x and current.y==self.end.y:
                return [self.retracePath(current),visited]
                
            visited.append(current)
            openList.remove(current)
            closedList.add(current)
            
            for p in self.graph[current]:
                n=p[0]
                cost=p[1]
                dist=current.cost+cost
                if dist <= n.cost and not n.visited:
                    n.cost=dist
                    n.prev=current
                    openList.add(n)
        print visited
        return [None,visited]
def main():
    pass
    

if __name__ == '__main__':
    main()
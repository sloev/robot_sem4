'''
Created on Nov 14, 2013

@author: johannes
'''
from itertools import product
from collections import defaultdict
from Node import Node

class Graph(object):
    def __init__(self,maseModel):
        self.mazeModel
        
        self.nodes = set()
        self.edges = {}
        self.distances = {}
        
    def getD(self,walls):
        if not((walls & 0b1000) >>3):#north
            return 0
        elif not ((walls & 0b0100) >>2):#east
            return 1
        elif not ((walls & 0b0010) >>1):#south
            return 2
        elif not (walls & 0b0001):#west
            return 3
        else:
            return -1
        
    def make(self):          
        for y in range(self.mazeModel.getHeight()):
            for x in range(self.mazeModel.getWidth()):     
                for d in range(4):
                    tmp=self.getD(self.mazeModel.get(x,y))
                    if tmp>-1:
                        self.add_node(tmp)
        for y in range(self.mazeModel.getHeight()):
            for x in range(self.mazeModel.getWidth()):     
                for d in range(4):                    
                    Node
    
    def add_node(self, value):
        self.nodes.add(value)
    
    def add_edge(self, from_node, to_node, distance):
        self._add_edge(from_node, to_node, distance)
        self._add_edge(to_node, from_node, distance)
 
    def _add_edge(self, from_node, to_node, distance):
        self.edges.setdefault(from_node, [])
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance
 
class pathFind():
    def __init__(self,mazeModel):
        self.graph=Graph()
         
    def dijkstra(self,graph, initial_node):
        visited = {initial_node: 0}
        current_node = initial_node
        path = {}
        nodes = set(graph.nodes)
        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node
 
            if min_node is None:
                break
     
            nodes.remove(min_node)
            cur_wt = visited[min_node]
            for edge in graph.edges[min_node]:
                wt = cur_wt + graph.distances[(min_node, edge)]
                if edge not in visited or wt < visited[edge]:
                    visited[edge] = wt
                    path[edge] = min_node
                
        return visited, path

    def shortest_path(self, initial_node, goal_node):
        distances, paths = self.dijkstra(self.graph, initial_node)           
        route = [goal_node]

        while goal_node != initial_node:
            route.append(paths[goal_node])
            goal_node = paths[goal_node]

        route.reverse()
        return route
    
class Node():
    def __init__(self,x,y,d):
        self.d=d
        self.x=x
        self.y=y
import fileinput
import numpy
import collections
from dijkstar import Graph, find_path
import math
from functools import cache
import sys
from collections import defaultdict

# From https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm
class Graph:
    """
    This class represents a directed graph using
    adjacency matrix representation.
    """

    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.row = len(graph)

    def bfs(self, s, t, parent):
        """
        Returns true if there is a path from
        source 's' to sink 't' in residual graph.
        Also fills parent[] to store the path.
        """

        # Mark all the vertices as not visited
        visited = [False] * self.row

        # Create a queue for BFS
        queue = collections.deque()

        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        # Standard BFS loop
        while queue:
            u = queue.popleft()

            # Get all adjacent vertices of the dequeued vertex u
            # If an adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.graph[u]):
                if (visited[ind] == False) and (val > 0):
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        # If we reached sink in BFS starting from source, then return
        # true, else false
        return (visited[t], visited)

    # Returns the maximum flow from s to t in the given graph
    def edmonds_karp(self, source, sink):
        # This array is filled by BFS and to store path
        parent = [-1] * self.row

        max_flow = 0  # There is no flow initially

        notdone, _ = self.bfs(source, sink, parent)
        # Augment the flow while there is path from source to sink
        while notdone:
            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
            notdone, _ = self.bfs(source, sink, parent)
        return max_flow

graph = [[0 for _ in range(1475)] for _ in range(1475)]
nodes = []
for line in fileinput.input():
    line = line.strip().split(": ")
    src = line[0]
    dsts = line[1].split(" ")
    if not (src in nodes):
        nodes.append(src)
    for dst in dsts:
        if not (dst in nodes):
            nodes.append(dst)
        graph[nodes.index(src)][nodes.index(dst)] = 1
        graph[nodes.index(dst)][nodes.index(src)] = 1
g =  Graph(graph)

print(g.edmonds_karp(0, 1398))
_, visited = g.bfs(0, 1398, [-1] * 1475)
v =[x for x in visited if x==True]
print (len(v))

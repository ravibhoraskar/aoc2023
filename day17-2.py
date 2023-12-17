import fileinput
import numpy
import collections
from dijkstar import Graph, find_path
import math

m = []
total = 0
for line in fileinput.input():
    m.append([int(x) for x in list(line.strip())])

graph = Graph()

graph.add_edge("init", (0, 0, "R", 0), 0)
graph.add_edge("init", (0, 0, "D", 0), 0)

for i in range(len(m)):
    for j in range(len(m[0])):

        for x in range(10):
            if j != len(m[0]) - 1:
                graph.add_edge((i, j, "R", x), (i, j + 1, "R", x + 1), m[i][j + 1])
            if i != len(m) - 1:
                graph.add_edge((i, j, "D", x), (i + 1, j, "D", x + 1), m[i + 1][j])
            if i != 0:
                graph.add_edge((i, j, "U", x), (i - 1, j, "U", x + 1), m[i - 1][j])
            if j != 0:
                graph.add_edge((i, j, "L", x), (i, j - 1, "L", x + 1), m[i][j - 1])

        for x in range(4, 11):
            graph.add_edge((i, j, "L", x), (i, j, "U", 0), 0)
            graph.add_edge((i, j, "L", x), (i, j, "D", 0), 0)
            graph.add_edge((i, j, "R", x), (i, j, "U", 0), 0)
            graph.add_edge((i, j, "R", x), (i, j, "D", 0), 0)
            graph.add_edge((i, j, "U", x), (i, j, "L", 0), 0)
            graph.add_edge((i, j, "U", x), (i, j, "R", 0), 0)
            graph.add_edge((i, j, "D", x), (i, j, "L", 0), 0)
            graph.add_edge((i, j, "D", x), (i, j, "R", 0), 0)

output = math.inf

output = min(
    find_path(graph, "init", (len(m) - 1, len(m[0]) - 1, "L", 0)).total_cost,
    find_path(graph, "init", (len(m) - 1, len(m[0]) - 1, "U", 0)).total_cost,
)

print(output)

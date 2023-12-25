import fileinput
import numpy
import collections
from dijkstar import Graph, find_path
import math
from functools import cache
import sys
from random import randint

m = []
for line in fileinput.input():
    m.append([x for x in list(line.strip())])
end = len(m) - 1

sys.setrecursionlimit(end**2)


def get_neighbors(i, j):
    n = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
    n = [x for x in n if x[0] >= 0 and x[0] < len(m) and x[1] >= 0 and x[1] < len(m[0])]
    n = [x for x in n if m[x[0]][x[1]] != "#" and m[x[0]][x[1]] != "O"]
    return n


decision_points = [(0, 1)]
for i in range(len(m)):
    for j in range(len(m[0])):
        if m[i][j] != "#" and len(get_neighbors(i, j)) > 2:
            decision_points.append((i, j))

for j in range(len(m[0])):
    if m[end][j] == ".":
        decision_points.append((end, j))

graph = {x: [] for x in decision_points}
distances = {}
for p in decision_points:
    for nbr in get_neighbors(p[0], p[1]):
        l = 1
        prev = p
        while not nbr in decision_points:
            l += 1
            nbrs = get_neighbors(nbr[0], nbr[1])
            nbrs = [x for x in nbrs if x != prev]
            if len(nbrs) != 1:
                raise Exception("Too many neighbors", nbr, nbrs)
            prev, nbr = nbr, nbrs[0]
        graph[p].append(nbr)
        distances[(p, nbr)] = l


maxsofar = 0


def recurse(node, seen, length):
    if len(seen) > 0:
        length = length + distances[(seen[-1], node)]
    if node in seen:
        return -math.inf
    elif node[0] == end:
        global maxsofar
        if length > maxsofar:
            maxsofar = length
        if randint(0, 100000) < 10:
            print(f"Found {length}, max so far {maxsofar}")
        return
    else:
        seen.append(node)
        for nbr in graph[node]:
            if not nbr in seen:
                recurse(nbr, seen, length)
        seen.pop()


recurse((0, 1), [], 0)
print(maxsofar)

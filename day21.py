import fileinput
import numpy
import collections
from dijkstar import Graph, find_path
import math
from functools import cache

m = []
total = 0
for line in fileinput.input():
    m.append([x for x in list(line.strip())])

m2 = [[0 for _ in range(len(m[0]))] for _ in range(len(m))]


@cache
def recurse(i, j, steps):
    if i < 0 or j < 0 or i >= len(m) or j >= len(m[0]):
        return 0
    elif m[i][j] == "#":
        return 0
    elif steps == 0:
        m2[i][j] = 1
        return 1
    else:
        return (
            recurse(i - 1, j, steps - 1)
            + recurse(i + 1, j, steps - 1)
            + recurse(i, j - 1, steps - 1)
            + recurse(i, j + 1, steps - 1)
        )


def find():
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] == "S":
                return (i, j)


startx, starty = find()
recurse(startx, starty, 64)
print(sum([sum(x) for x in m2]))

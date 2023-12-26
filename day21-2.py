import fileinput
import numpy
import collections
from dijkstar import Graph, find_path
import math
from functools import cache
from collections import defaultdict
from scipy.interpolate import lagrange


# x = []
# y = []
# for line in fileinput.input():
#     line = line.strip().split(" ")
#     x.append(int(line[0]))
#     y.append(int(line[1]))
# f = lagrange(x, y)
# print(f(26501365))

m = []
total = 0
for line in fileinput.input():
    m.append([x for x in list(line.strip())])

# Recursive is too slow, wrote an iterative one instead below
@cache
def recurse(i, j, steps, mi, mj):
    if i == -1:
        mi = mi - 1
        i = len(m) - 1
        return recurse(i, j, steps, mi, mj)
    elif j == -1:
        mj = mj - 1
        j = len(m[0]) - 1
        return recurse(i, j, steps, mi, mj)
    elif i == len(m):
        mi = mi + 1
        i = 0
        return recurse(i, j, steps, mi, mj)
    elif j == len(m[0]):
        mj = mj + 1
        j = 0
        return recurse(i, j, steps, mi, mj)
    if i < 0 or j < 0 or i >= len(m) or j >= len(m[0]):
        raise Exception("out of bounds")
    elif m[i][j] == "#":
        return set()
    elif steps == 0:
        ret = set()
        ret.add((i, j, mi, mj))
        return ret
    else:
        return set().union(
            recurse(i - 1, j, steps - 1, mi, mj),
            recurse(i + 1, j, steps - 1, mi, mj),
            recurse(i, j - 1, steps - 1, mi, mj),
            recurse(i, j + 1, steps - 1, mi, mj),
        )


def find_paths(i, j, steps, mi, mj):
    seen = []
    queue = [(i, j, steps, mi, mj)]
    output = 0
    while queue:
        i, j, steps, mi, mj = queue.pop(0)
        if (i, j, mi, mj) in seen:
            continue
        else:
            seen.append((i, j, mi, mj))

        if i == -1:
            queue.append((len(m) - 1, j, steps, mi - 1, mj))
        elif j == -1:
            queue.append((i, len(m[0]) - 1, steps, mi, mj - 1))
        elif i == len(m):
            queue.append((0, j, steps, mi + 1, mj))
        elif j == len(m[0]):
            queue.append((i, 0, steps, mi, mj + 1))
        elif m[i][j] == "#":
            continue
        elif steps == 0:
            # print (f"Adding {i},{j}")
            output += 1
        else:
            if steps%2 == 0:
                output += 1
                # print (f"Addin {i},{j}")

            queue.append((i - 1, j, steps - 1, mi, mj))
            queue.append((i + 1, j, steps - 1, mi, mj))
            queue.append((i, j - 1, steps - 1, mi, mj))
            queue.append((i, j + 1, steps - 1, mi, mj))
    return output

def find():
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] == "S":
                return (i, j)



startx, starty = find()
for i in [65, 196, 327, 458]:
    print(i, find_paths(startx, starty, i, 0, 0))
# Curve fit the answers to find f((n-65)/131)

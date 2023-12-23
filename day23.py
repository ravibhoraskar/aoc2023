import fileinput
import numpy
import collections
from dijkstar import Graph, find_path
import math
from functools import cache

m = []
for line in fileinput.input():
    m.append([x for x in list(line.strip())])

end = len(m) - 1


# def recurse(i, j):
#     result = None
#     if i < 0 or j < 0 or i >= len(m) or j >= len(m[0]):
#         return -math.inf
#     elif m[i][j] == "#" or m[i][j] == "O":
#         return -math.inf
#     elif i == end:
#         print(numpy.array(m))
#         return 1
#     elif m[i][j] == ">":
#         m[i][j] = "O"
#         result = 1 + recurse(i, j + 1)
#         m[i][j] = ">"
#     elif m[i][j] == "v":
#         m[i][j] = "O"
#         result = 1 + recurse(i + 1, j)
#         m[i][j] = "v"
#     else:
#         if m[i][j] != ".":
#             raise Exception("something went wrong. Found", m[i][j])
#         m[i][j] = "O"
#         result = 1 + max(
#             recurse(i + 1, j), recurse(i - 1, j), recurse(i, j + 1), recurse(i, j - 1)
#         )
#         m[i][j] = "."
#     return result

print(recurse(0, 1))

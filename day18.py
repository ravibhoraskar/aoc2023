import fileinput
import collections
import math
import numpy

total = 0
x, y = 0, 0
m = numpy.array([[]])
for line in fileinput.input():
    line = line.strip().split(" ")
    dir = line[0]
    num = int(line[1])
    if dir == "U":
        newx = x - num
        newy = y
    elif dir == "D":
        newx = x + num
        newy = y
    elif dir == "L":
        newx = x
        newy = y - num
    elif dir == "R":
        newx = x
        newy = y + num

    if newx < 0:
        m = numpy.pad(m, [(0 - newx, 0), (0, 0)])
        x, newx = x - newx, newx - newx
    if newx >= len(m):
        m = numpy.pad(m, [(0, newx - len(m) + 1), (0, 0)])
    if newy < 0:
        m = numpy.pad(m, [(0, 0), (0 - newy, 0)])
        y, newy = y - newy, newy - newy
    if newy >= len(m[0]):
        m = numpy.pad(m, [(0, 0), (0, newy - len(m[0]) + 1)])

    for i in range(x, newx, -1 if x > newx else 1):
        m[i][y] = 1
    for j in range (y, newy, -1 if y > newy else 1):
        if j < len(m[0]):
            m[x][j] = 1
    m[newx][newy] = 1
    x, y = newx, newy

#Flood fill solution
m = numpy.pad(m, [(1, 1), (1, 1)])
tovisit = [(0, 0)]
while len(tovisit) > 0:
    i,j = tovisit.pop()
    if i < 0 or j < 0 or i >= len(m) or j >= len(m[0]):
        continue
    elif m[i][j] == 0:
        m[i][j] = -1
        tovisit.append((i + 1, j))
        tovisit.append((i - 1, j))
        tovisit.append((i, j + 1))
        tovisit.append((i, j - 1))

sum = 0
print(sum)


# for i in range(len(m)):
#     for j in range(len(m[0])):
#         if m[i][j] == 0:
#             print ('.', end="")
#             sum += 1
#         elif m[i][j] == 1:
#             print ('#', end="")
#             sum += 1
#         else:
#             print ('X', end="")
#     print()

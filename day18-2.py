import fileinput
import collections
import math
import numpy

total, x, y = 0, 0, 0
for line in fileinput.input():
    line = line.strip().split("#")[1]
    num = int(line[0:5], 16)
    dir = int(line[5])
    dir = {0: "R", 1: "D", 2: "L", 3: "U"}[dir]

    # line = line.strip().split(" ")
    # dir = line[0]
    # num = int(line[1])
    print(x, y, total)
    if dir == "U":
        x = x - num
    elif dir == "D":
        x = x + num
        total += num
    elif dir == "L":
        y = y - num
        total += x * num
        total += num
    elif dir == "R":
        y = y + num
        total -= x * num
    else:
        raise Exception("Invalid direction " + dir)
print(total + 1)

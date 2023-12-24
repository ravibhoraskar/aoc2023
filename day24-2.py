import fileinput
import numpy as np
import math
from sympy import solve, symbols

hailstones = []
n = 0
expressions = []
x,y,z,u,v,w = symbols('x y z u v w')
for line in fileinput.input():
    line = line.strip().split(" @ ")
    position = tuple([int(x) for x in line[0].split(", ")])
    velocity = tuple([int(x) for x in line[1].split(", ")])
    hailstones.append((position, velocity))
    t = symbols('t'+str(n))
    expressions.append(x + u * t - position[0] - velocity[0]*t)
    expressions.append(y + v * t - position[1] - velocity[1]*t)
    expressions.append(z + w * t - position[2] - velocity[2]*t)
    n += 1
print (expressions)
print (solve(expressions))

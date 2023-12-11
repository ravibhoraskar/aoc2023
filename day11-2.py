import fileinput
import numpy

def print_matrix(m):
    for row in m:
        print(''.join(row))

input = fileinput.input()
output = 0
m = []

for line in input:
    line = line.strip()
    if not '#' in line:
        m.append(['x' for _ in range(len(line))])
    else:
        m.append(list(line))

m = numpy.transpose(m)
newm = []
for line in m:
    if not '#' in line:
        newm.append(['x' for _ in range(len(line))])
    else:
        newm.append(line)
m = numpy.transpose(newm)

galaxies = []
for i, _ in enumerate(m):
    for j, e in enumerate(m[i]):
        if (e == '#'):
            galaxies.append((i, j))

sum = 0
for p, g1 in enumerate(galaxies):
    for q, g2 in enumerate(galaxies):
        if g1 < g2:
            innersum = 0
            for i in range(g1[0], g2[0]+1):
                if m[i][g1[1]]  == 'x':
                    innersum += 1000000
                else:
                    innersum += 1
            start, end = g1[1], g2[1]
            if start > end:
                start, end = end, start
            for j in range(start, end+1):
                if m[g2[0]][j]  == 'x':
                    innersum += 1000000
                else:
                    innersum += 1
            innersum -=2
            sum += innersum
print(sum)

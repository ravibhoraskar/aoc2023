import fileinput
import numpy


def print_matrix(m):
    for row in m:
        print("".join(row))


input = fileinput.input()
output = 0
m = []

for line in input:
    line = line.strip()
    if not "#" in line:
        m.append(list(line))
    m.append(list(line))

m = numpy.transpose(m)
newm = []
for line in m:
    if not "#" in line:
        newm.append(line)
    newm.append(line)
m = numpy.transpose(newm)

galaxies = []
for i, _ in enumerate(m):
    for j, e in enumerate(m[i]):
        if e == "#":
            galaxies.append((i, j))

sum = 0
for g1 in galaxies:
    for g2 in galaxies:
        if g1 < g2:
            sum += abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
print(sum)

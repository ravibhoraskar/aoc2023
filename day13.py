import fileinput
import numpy


def count(m):
    return reflectionindex(m) * 100 + reflectionindex(numpy.transpose(m).tolist())


def reflectionindex(m):
    for i in range(1, len(m)):
        reflects = True
        for j in range(0, i):
            refindex = i + i - j - 1
            if refindex >= len(m):
                continue
            if m[j] != m[refindex]:
                reflects = False
                break
        if reflects:
            return i
    return 0


m = []
total = 0
for line in fileinput.input():
    if line.strip() != "":
        m.append(list(line.strip()))
    else:
        total += count(m)
        m = []
total += count(m)  # last one
print(total)

import fileinput
import numpy


def flip(c):
    return "." if c == "#" else "#"


def count(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            m[i][j] = flip(m[i][j])
            sum = reflectionindex(m, i) * 100 + reflectionindex(
                numpy.transpose(m).tolist(),
                j,
            )
            if sum > 0:
                return sum
            m[i][j] = flip(m[i][j])
    raise Exception("Couldn't find")


def flippedbitisinrange(flipped, mirroridx, totallength):
    if mirroridx < totallength / 2:
        return flipped in range(0, mirroridx * 2)
    else:
        return flipped in range(2 * mirroridx - totallength, totallength)


def reflectionindex(m, flippedi):
    for i in range(1, len(m)):
        reflects = True
        for j in range(0, i):
            refindex = i + i - j - 1
            if refindex >= len(m):
                continue
            if m[j] != m[refindex]:
                reflects = False
                break
        if reflects and flippedbitisinrange(flippedi, i, len(m)):
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

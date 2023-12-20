import fileinput
import numpy
import collections


def tiltwest(m):
    newm = []
    for i, l in enumerate(m):
        l = "".join(l)
        l = l.split("#")
        newl = []
        for item in l:
            c = collections.Counter(item)
            newl.append("O" * c["O"] + "." * c["."])
        l = newl
        newm.append(list("#".join(l)))
    m = newm
    return m


def tiltnorth(m):
    m = numpy.transpose(m)
    m = tiltwest(m)
    m = numpy.transpose(m)
    return m


def tiltsouth(m):
    m = numpy.flipud(m)
    m = tiltnorth(m)
    m = numpy.flipud(m)
    return m.tolist()


def tilteast(m):
    m = numpy.fliplr(m)
    m = tiltwest(m)
    m = numpy.fliplr(m)
    return m.tolist()


def getsum(m):
    sum = 0
    for i, l in enumerate(m):
        sum += l.count("O") * (len(m) - i)
    return sum


m = []
total = 0
for line in fileinput.input():
    m.append(list(line.strip()))


for i in range(1000):
    m = tiltnorth(m)
    m = tiltwest(m)
    m = tiltsouth(m)
    m = tilteast(m)
    print(getsum(m))

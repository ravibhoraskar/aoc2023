import fileinput
import numpy
import collections

m = []
total = 0
for line in fileinput.input():
    m.append(list(line.strip()))

m = numpy.transpose(m)

newm = []
for i, l in enumerate(m):
    l = ''.join(l)
    l = l.split('#')
    newl = []
    for item in l:
        c = collections.Counter(item)
        newl.append('O' * c['O'] + '.' * c['.'])
    l = newl
    newm.append(list('#'.join(l)))
m = newm
m = numpy.transpose(m).tolist()

sum = 0
for i, l in enumerate(m):
    sum += l.count('O') * (len(m) - i)
print(sum)

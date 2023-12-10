import fileinput
import functools
import numpy as np


@functools.cache
def generate_vector(t):
    A = np.vander(np.arange(t + 1, dtype=int), N=t, increasing=True)
    return np.einsum("i,ij->j", A[-1], np.linalg.inv(A[:-1]))


def get_next(seq):
    v = generate_vector(len(seq))
    return round(np.dot(v, seq))


def next(line):
    if all(x == 0 for x in line):
        return 0
    return next([line[i + 1] - line[i] for i in range(len(line) - 1)]) + line[-1]


input = fileinput.input()
output = 0
for line in input:
    line = line.strip().split(" ")
    line = [int(x) for x in line]
    output += next(line)
print(output)

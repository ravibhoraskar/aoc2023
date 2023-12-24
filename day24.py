import fileinput
import numpy as np
import math

hailstones = []
for line in fileinput.input():
    line = line.strip().split(" @ ")
    position = tuple([int(x) for x in line[0].split(", ")][0:2])
    velocity = tuple([int(x) for x in line[1].split(", ")][0:2])
    hailstones.append((position, velocity))
print(hailstones)


def normalize_slope(slope):
    gcd = math.gcd(slope[0], slope[1])
    return (slope[0] // gcd, slope[1] // gcd)


output = 0
for i in range(len(hailstones)):
    for j in range(i):
        hail1 = hailstones[i]
        hail2 = hailstones[j]
        if normalize_slope(hail1[1]) == normalize_slope(hail2[1]):
            print("Found parallel lines")
            continue
        else:
            x1, y1 = hail1[0]
            u1, v1 = hail1[1]
            x2, y2 = hail2[0]
            u2, v2 = hail2[1]
            x = (u2 * v1 * x1 - u1 * v2 * x2 + u2 * u1 * y2 - u2 * u1 * y1) / (
                u2 * v1 - u1 * v2
            )
            y = (v2 * u1 * y1 - v1 * u2 * y2 + v2 * v1 * x2 - v2 * v1 * x1) / (
                v2 * u1 - v1 * u2
            )
            print(x, y)
            if (x - x1) * u1 < 0 or (x - x2) * u2 < 0:
                print("Found intersection in the past")
            elif not (
                200000000000000 <= x <= 400000000000000
                and 200000000000000 <= y <= 400000000000000
            ):
                print("Found intersection out of bounds")
            else:
                output += 1
print(f"Anwer is {output}")

import fileinput
import numpy

bricks = []
for line in fileinput.input():
    brick = tuple(
        tuple(int(y) for y in tuple(x.split(","))) for x in line.strip().split("~")
    )
    bricks.append(brick)

def estaocupada(brick, ocupada):
    for i in range(brick[0][0], brick[1][0] + 1):
        for j in range(brick[0][1], brick[1][1] + 1):
            for k in range(brick[0][2], brick[1][2] + 1):
                if ocupada[i][j][k]:
                    return True
    return False

def fallbricks(bricks):
    bricks = sorted(bricks, key=lambda x: x[0][2])
    newbricks = []
    ocupada = numpy.zeros([20,20,400])
    numfell = 0
    for brick in bricks:
        prevbrick = None
        newbrick = None
        for z in range(brick[0][2], -1, -1):
            prevbrick = newbrick
            newbrick = (
                (brick[0][0], brick[0][1], z),
                (brick[1][0], brick[1][1], z + brick[1][2] - brick[0][2]),
            )
            if estaocupada(newbrick, ocupada) or z == 0:
                newbricks.append(prevbrick)
                if prevbrick != brick:
                    numfell += 1
                for i in range(prevbrick[0][0], prevbrick[1][0] + 1):
                    for j in range(prevbrick[0][1], prevbrick[1][1] + 1):
                        for k in range(prevbrick[0][2], prevbrick[1][2] + 1):
                            ocupada[i,j,k] = 1
                break
    return [newbricks, numfell]

newbricks, _ = fallbricks(bricks)

output = 0
for brick in newbricks:
    deleted_bricks = [x for x in newbricks if x != brick]
    _, numfell = fallbricks(deleted_bricks)
    output += numfell
print(output)

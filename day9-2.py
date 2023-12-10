import fileinput


def next(line):
    if all(x == 0 for x in line):
        return 0
    return line[0] - next([line[i + 1] - line[i] for i in range(len(line) - 1)])


input = fileinput.input()
output = 0
for line in input:
    line = line.strip().split(" ")
    line = [int(x) for x in line]
    output += next(line)

print(output)

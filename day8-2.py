import fileinput, math

total = 0
input = fileinput.input()
firstline = input.readline().strip()
input.readline()
graph = {}
for line in input:
    src = line.split("=")[0].strip()
    dst = line.split("=")[1].strip()[1:-1].split(", ")
    graph[src] = dst

inits = [x for x in graph.keys() if x[-1] == "A"]
ends = [x for x in graph.keys() if x[-1] == "Z"]

steplist = []
for init in inits:
    steps = 0
    current = init
    curridx = 0

    while not current in ends:
        steps += 1

        if firstline[curridx] == "L":
            current = graph[current][0]
        else:
            current = graph[current][1]

        curridx += 1
        if curridx == len(firstline):
            curridx = 0
    steplist.append(steps)

print(math.lcm(*steplist))

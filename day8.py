import fileinput

total = 0
input = fileinput.input()
firstline = input.readline().strip()
input.readline()
graph = {}
for line in input:
    src = line.split("=")[0].strip()
    dst = line.split("=")[1].strip()[1:-1].split(", ")
    graph[src] = dst

steps = 0
current = "AAA"
curridx = 0

while current != "ZZZ":
    steps += 1

    if firstline[curridx] == "L":
        current = graph[current][0]
    else:
        current = graph[current][1]

    curridx += 1
    if curridx == len(firstline):
        curridx = 0

print(steps)

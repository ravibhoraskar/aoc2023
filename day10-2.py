import fileinput

input = fileinput.input()
output = 0
graph = []

for line in input:
    graph.append(line.strip())

for i in range(len(graph)):
    for j in range(len(graph[0])):
        if graph[i][j] == "S":
            start = (i, j)

prev = start
current = (start[0], start[1] + 1)  # hardcode first neighbor
up = ["|", "L", "J", "S"] # hardcode S == L
down = ["|", "7", "F"]
left = ["-", "7", "J"]
right = ["-", "F", "L", "S"] # hardcode S == L

loop = {start}

while graph[current[0]][current[1]] != "S":
    loop.add(current)
    cur, i, j = graph[current[0]][current[1]], current[0], current[1]
    if cur in up and not (prev == (i - 1, j)) and graph[i - 1][j] in down + ["S"]:
        prev = current
        current = (i - 1, j)
    elif cur in down and not (prev == (i + 1, j)) and graph[i + 1][j] in up + ["S"]:
        prev = current
        current = (i + 1, j)
    elif cur in left and not (prev == (i, j - 1)) and graph[i][j - 1] in right + ["S"]:
        prev = current
        current = (i, j - 1)
    elif cur in right and not (prev == (i, j + 1)) and graph[i][j + 1] in left + ["S"]:
        prev = current
        current = (i, j + 1)
    else:
        raise Exception("Couldn't find neighbor for {}".format(current))

clean = [["." for _ in range(len(graph[0]))] for _ in range(len(graph))]
for i in range(len(graph)):
    for j in range(len(graph[0])):
        if (i, j) in loop:
            clean[i][j] = graph[i][j]

graph = clean

expanded = [["." for _ in range(len(graph[0]) * 2)] for _ in range(len(graph) * 2)]
for i in range(len(graph) * 2):
    for j in range(len(graph[0]) * 2):
        if i % 2 == 0 and j % 2 == 0:
            expanded[i][j] = graph[i // 2][j // 2]
        elif j > 0 and expanded[i][j -1] in right:
            expanded[i][j] = "-"
        elif i > 0 and expanded[i -1][j] in down:
            expanded[i][j] = "|"

# Flood fill
tovisit = [(i,0) for i in range(len(expanded))] + [(0,j) for j in range(len(expanded[0]))]
while tovisit:
    i, j = tovisit.pop()
    if i < 0 or j < 0 or i >= len(expanded) or j >= len(expanded[0]):
        continue
    elif expanded[i][j] != ".":
        # already visited or part of loop
        continue
    else:
        expanded[i][j] = "O"
        tovisit.append((i + 1, j))
        tovisit.append((i - 1, j))
        tovisit.append((i, j + 1))
        tovisit.append((i, j - 1))

for i in range(len(expanded)):
    for j in range(len(expanded[0])):
        if i % 2 == 0 and j % 2 == 0:
            if expanded[i][j] == ".":
                output += 1
print(output)

# for i in range(len(expanded)):
#     for j in range(len(expanded[0])):
#         print(expanded[i][j], end="")
#     print()

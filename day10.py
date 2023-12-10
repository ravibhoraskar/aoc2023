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
up = ["|", "L", "J"]
down = ["|", "7", "F"]
left = ["-", "7", "J"]
right = ["-", "F", "L"]
distance = 1

while graph[current[0]][current[1]] != "S":
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
    distance += 1

print(int(distance / 2))

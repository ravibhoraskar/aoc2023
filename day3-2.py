import fileinput

grid = []
# append '.' to the end of each row in the input to make sure we don't go out of bounds
for line in fileinput.input():
    grid.append(line.strip())

numbers_adjacent_to_gears = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
gear_factors = [[1 for _ in range(len(grid[0]))] for _ in range(len(grid))]


def processnumber(x, y, length, number):
    for i in range(x - 1, x + 2):  # range is inclusive-exclusive
        for j in range(y - 1, y + length + 1):
            if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
                continue
            if grid[i][j] == "*":
                # Found a gear next to this number
                numbers_adjacent_to_gears[i][j] += 1
                gear_factors[i][j] *= number


for i in range(len(grid)):
    currentnumber = ""
    for j in range(len(grid[i])):
        if grid[i][j].isdigit():
            currentnumber += grid[i][j]
        if currentnumber != "":
            if not grid[i][j].isdigit():
                # number has ended
                processnumber(
                    i, j - len(currentnumber), len(currentnumber), int(currentnumber)
                )
                currentnumber = ""

# print (numbers_adjacent_to_gears)
# print (gear_factors)

sum = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if numbers_adjacent_to_gears[i][j] == 2:
            sum += gear_factors[i][j]
print(sum)

import fileinput

grid = []
# append '.' to the end of each row in the input to make sure we don't go out of bounds
for line in fileinput.input():
    grid.append(line.strip())

def isvalid(x, y, length):
    for i in range(x-1, x+2): # range is inclusive-exclusive
        for j in range(y-1, y+length+1):
            if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
                continue
            if grid[i][j] != '.' and (not grid[i][j].isdigit()):
                return True
    return False

sum = 0
for i in range(len(grid)):
    currentnumber = ""
    for j in range(len(grid[i])):
        if grid[i][j].isdigit():
            currentnumber += grid[i][j]
        if currentnumber != "":
            if (not grid[i][j].isdigit()):
                # number has ended
                v = isvalid(i, j-len(currentnumber), len(currentnumber))
                if v:
                    sum += int(currentnumber)
                currentnumber = ""
print (sum)

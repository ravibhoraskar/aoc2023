import fileinput


def first_digit(s):
    for c in s:
        if c.isdigit():
            return c
    return -1


total = 0
for line in fileinput.input():
    first = first_digit(line)
    last = first_digit(line[::-1])
    num = int(first + last)
    total += num
print(total)

import fileinput, re

nums = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
regex = "|".join(nums.keys())
regex_reverse = regex[::-1]
total = 0
for line in fileinput.input():
    first = nums[re.search(regex, line).group(0)]
    last = nums[(re.search(regex_reverse, line[::-1]).group(0))[::-1]]
    num = int(first + last)
    total += num
print(total)

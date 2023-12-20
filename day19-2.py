import sys
from operator import mul
from functools import reduce
from copy import deepcopy

input = sys.stdin.read().split("\n\n")
workflows = input[0].strip().split("\n")
parts = input[1].strip().split("\n")


def parse(r):
    if "<" in r:
        typ = "<"
        nxt = r.split(":")[1]
        cat = r.split("<")[0]
        lim = int(r.split(":")[0].split("<")[1])
    elif ">" in r:
        typ = ">"
        nxt = r.split(":")[1]
        cat = r.split(">")[0]
        lim = int(r.split(":")[0].split(">")[1])
    else:
        typ = "O"
        nxt = r
        cat = ""
        lim = -1
    return (typ, nxt, cat, lim)


w = {}
for wf in workflows:
    spl = wf.split("{")
    name = spl[0]
    actions = spl[1].split("}")[0].split(",")
    w[name] = [parse(action) for action in actions]
workflows = w

r = []
for p in parts:
    pdict = {}
    for q in p.split("{")[1].split("}")[0].split(","):
        spl = q.split("=")
        pdict[spl[0]] = int(spl[1])
    r.append(pdict)
parts = r


def applyaction(action, part):
    for typ, nxt, cat, lim in workflows[action]:
        if "<" == typ:
            if part[cat] < lim:
                return nxt
        elif ">" == typ:
            if part[cat] > lim:
                return nxt
        elif "O" == typ:
            return nxt
        else:
            raise Exception("applyaction failed")
    raise Exception("applyaction failed")


def isaccepted(part):
    action = "in"
    while not action in ["A", "R"]:
        action = applyaction(action, part)
    return True if action == "A" else False


def traverse(
    action,
    idx,
    ranges,
):
    if action == "R":
        return 0
    elif action == "A":
        return reduce(mul, [b - a + 1 for a, b in ranges.values()], 1)

    typ, nxt, cat, lim = workflows[action][idx]
    if "O" == typ:
        return traverse(nxt, 0, ranges)
    elif "<" == typ:
        p, q = ranges[cat]
        if lim <= p:
            truecount = 0
            falsecount = traverse(action, idx + 1, ranges)
        elif lim > q:
            truecount = traverse(nex, 0, ranges)
            falsecount = 0
        else:
            r = deepcopy(ranges)
            r[cat] = (p, lim - 1)
            truecount = traverse(nxt, 0, r)
            r = deepcopy(ranges)
            r[cat] = (lim, q)
            falsecount = traverse(action, idx + 1, r)
        return truecount + falsecount
    elif ">" == typ:
        p, q = ranges[cat]
        if lim >= q:
            truecount = 0
            falsecount = traverse(action, idx + 1, ranges)
        elif lim < p:
            truecount = traverse(nxt, 0, ranges)
            falsecount = 0
        else:
            r = deepcopy(ranges)
            r[cat] = (lim + 1, q)
            truecount = traverse(nxt, 0, r)
            r = deepcopy(ranges)
            r[cat] = (p, lim)
            falsecount = traverse(action, idx + 1, r)
        return truecount + falsecount


print(
    traverse("in", 0, {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)})
)

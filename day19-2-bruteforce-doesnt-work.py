import sys

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


limits = {
    "x": [4000],
    "m": [4000],
    "a": [4000],
    "s": [4000],
}
for wf in workflows.values():
    for typ, nxt, cat, lim in wf:
        if typ in ["<", ">"]:
            limits[cat].append(lim)
limits = dict(map(lambda item: (item[0], sorted(item[1])), limits.items()))

# out = 0
# for p in parts:
#     if isaccepted(p):
#         out += sum(p.values())
# print(out)

out = 0
for x in range(len(limits["x"])):
    leftbound = 0 if x == 0 else limits["x"][x - 1]
    curx = limits["x"][x]
    xr = max(0, curx - leftbound - 1)
    for m in range(len(limits["m"])):
        leftbound = 0 if m == 0 else limits["m"][m - 1]
        curm = limits["m"][m]
        mr = max(0, curm - leftbound - 1)
        for a in range(len(limits["a"])):
            leftbound = 0 if a == 0 else limits["a"][a - 1]
            cura = limits["a"][a]
            ar = max(0, cura - leftbound - 1)
            for s in range(len(limits["s"])):
                leftbound = 0 if s == 0 else limits["s"][s - 1]
                curs = limits["s"][s]
                sr = max(0, curs - leftbound - 1)
                for numx, xtocheck in [(xr, curx - 0.5), (1, curx)]:
                    for numm, mtocheck in [(mr, curm - 0.5), (1, curm)]:
                        for numa, atocheck in [(ar, cura - 0.5), (1, cura)]:
                            for nums, stocheck in [(sr, curs - 0.5), (1, curs)]:
                                if isaccepted(
                                    {
                                        "x": xtocheck,
                                        "m": mtocheck,
                                        "a": atocheck,
                                        "s": stocheck,
                                    }
                                ):
                                    out += numx * numm * numa * nums
print(out)

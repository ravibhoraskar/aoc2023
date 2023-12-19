import sys

input = sys.stdin.read().split("\n\n")
workflows = input[0].strip().split("\n")
parts = input[1].strip().split("\n")

w = {}
for wf in workflows:
    spl = wf.split("{")
    name = spl[0]
    actions = spl[1].split("}")[0].split(",")
    w[name] = actions
workflows = w

r = []
for p in parts:
    pdict = {}
    for q in p.split("{")[1].split("}")[0].split(","):
        spl = q.split("=")
        pdict[spl[0]] = int(spl[1])
    r.append(pdict)
parts = r

def applyrule(rule, part):
    print ("  Applying rule", rule)
    for r in workflows[rule]:
        print ("    Rule", r)
        if '<' in r:
            nxt = r.split(':')[1]
            cat = r.split("<")[0]
            bu = int(r.split(':')[0].split("<")[1])
            if part[cat] < bu:
                return nxt
        elif '>' in r:
            nxt = r.split(':')[1]
            cat = r.split(">")[0]
            bu = int(r.split(':')[0].split(">")[1])
            if part[cat] > bu:
                return nxt
        else:
            return r
    raise Exception("applyrule failed")



accepted = []
for p in parts:
    print ("Processing part", p)
    rule = "in"
    while not rule in ["A", "R"]:
        rule = applyrule(rule, p)
    if rule == "A":
        accepted.append(p)
print (sum([sum(x.values()) for x in accepted]))

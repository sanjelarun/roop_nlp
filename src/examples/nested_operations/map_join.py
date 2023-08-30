"result = []\nfor x in xs:\n\tfor y in ys:\n\t\tresult.append((x, y**2))", ["map()", "join()"]
def increase_join(xs,ys):
    t = []
    result = []
    for y in ys:
        t.append(y*2)
    y
    for x in xs:
        for y in ys:
            result.append((x,y))
    return result
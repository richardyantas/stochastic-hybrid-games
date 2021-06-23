import json
# Brackets []
# Braces {}
# Parenthesis ()


def toBracesString(data):
    a = []
    for zonotopePats in data:
        b = []
        for zonotopePat in zonotopePats:
            b.append("{"+",".join(str(e) for e in zonotopePat)+"}")
        a.append("\n{" + ",".join(b) + "}")
    return "{" + ",".join(a) + "\n}"


def jsonParseUppaal():
    f = open("../sthocastic_hybrid_game/datasets/uppaal_data.txt", "w+")
    with open("../sthocastic_hybrid_game/datasets/uppaal_data.txt.json") as json_file:
        data = json.load(json_file)
        K = data["K"]
        # add export file
        M = 0

        p = []
        for zonotope in data["zonotope"]:
            q = []
            for zonotopeState in zonotope:
                q.append("{"+",".join(str(e) for e in zonotopeState)+"}")
            p.append("\n{" + ",".join(q) + "}")
        zonotopes = "\n{" + ",".join(p) + "\n}"

        for zonotopePats in data["patterns"]:
            M = max(len(zonotopePats), M)
        print("M:", M)
        for zonotopePats in data["patterns"]:
            for zonotopePat in zonotopePats:
                while len(zonotopePat) < K:
                    zonotopePat.append(-1)
            while len(zonotopePats) < M:
                zonotopePats.append([-2, -2, -2])
    f.write(toBracesString(data["patterns"]))
    f.write(zonotopes)


jsonParseUppaal()

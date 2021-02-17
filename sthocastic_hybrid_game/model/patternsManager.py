import json

pat = json.load(open("./sthocastic_hybrid_game/datasets/pattern.json"))

# Then add Json to UPPAAL
R = pat["R"]
S = pat["S"]
tau = pat["tau"]
factorTe = pat["factorTe"]
factorI = pat["factorI"]
factorKe = pat["factorKe"]
rate = pat["rate"]
TwaterIn = pat["TwaterIn"]
z = pat["z"]
x = pat["x"]

def query(X):
    for i in range(0,len(z)):
        if (z[i][0] <= X.T  and X.T < z[i][1]) and (z[i][2] <= X.V and X.V <= z[i][3]):
            #print("i: ",i,x[i][1]),
            #n = random.randint(0,len(x[i])-1) # 1
            n = 1
            return {"pat":list(x[i][n]),"i":i}    
    print("Not found state: ",X)
    return {"pat":[-1,-1,-1],"i":-1}
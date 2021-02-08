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
    a.append("{"+ ",".join(b) + "}\n" )
  return "{"+ ",".join(a) + "}"
  
def jsonParseUppaal():
  f = open("jsonToUppal.txt")  
  with open("pattern.json") as json_file:
    data = json.load(json_file)
    K = data["K"]    
    # add export file
    M=0
    for zonotopePats in data["x"]:
      M=max(len(zonotopePats),M)
    print("M:", M)
    for zonotopePats in data["x"]: # x is patterns
      for zonotopePat in zonotopePats:
        while len(zonotopePat)<K:
          zonotopePat.append(-1)
      while len(zonotopePats)<M:   # calculate the max
        zonotopePats.append([-2,-2,-2])

    print( toBracesString(data["x"]) )

jsonParseUppaal()
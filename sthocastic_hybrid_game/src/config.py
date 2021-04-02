import json
from .uncontrollableInput import setUncontrallableInput

# x=[E,V,T] d=[Te,Ti,I]
# mode p,r,v,f
# life_time = num-H_uppaal
#from .controllers import predictiveSafeController, initialSafeController, uppaalController


filepath1 = "sthocastic_hybrid_game/datasets/Solargis_min15_Almeria_Spain.csv"
filepath2 = "sthocastic_hybrid_game/datasets/valve.csv"  # sys.argv[2]'

safeConfig = json.load(open("sthocastic_hybrid_game/datasets/pattern.json"))

uInput = setUncontrallableInput()

modes  = [[1,0,0,0],
          [1,1,0,0], 
          [2,0,0,0], 
          [2,1,0,0], 
          [3,0,0,1], 
          [3,1,0,1], 
          [2,0,0,1],
          [2,1,0,1]]

controller_name = "normal"
lifeTime = 2*24*60+1
dt       = 60

R        = safeConfig["R"]
S        = safeConfig["S"]
tau      = safeConfig["tau"]
factorTe = safeConfig["factorTe"] 
factorKe = safeConfig["factorKe"]
factorI  = safeConfig["factorI"]
rate     = safeConfig["rate"]
TwaterIn = safeConfig["TwaterIn"] 
zonotopes= safeConfig["z"]
patterns = safeConfig["x"]
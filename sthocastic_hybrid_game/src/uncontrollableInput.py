import random
import numpy as np

def setUncontrallableInput():
  uInput = (np.zeros(24*12)).tolist()
  numInput = random.randrange(5,8)
  standardDeviation = 1*3  # 1*60/5
  for i in range(0,numInput):
    # int(random.gauss(7*60/5,1*60/5) )
    uInput[ int(random.gauss(7*60/5, standardDeviation) )  ] = 1
    uInput[ int(random.gauss(13*60/5,standardDeviation) )  ] = 1
    uInput[ int(random.gauss(19*60/5,standardDeviation) )  ] = 1
  print("uInput: ", uInput) 
  return uInput
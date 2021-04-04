
import multiprocessing
from .dataProcessing import DataProcessing
from .controllers import initialSafeController, predictiveSafeController, uppaalController, controllers
from .config import *

def supervisor(queue, pat, state, disturbances, index):
  if(len(pat) == 0):
    pat = queue.get()
    mode = modes[pat.pop(0)]
  elif(len(pat) == 1):
    mode = modes[pat.pop(0)]
    process = multiprocessing.Process(target=controllers[controller_name], args=(queue,state, mode, disturbances, index))
    process.start()
  elif(len(pat) > 1):
    mode = modes[pat.pop(0)]
  #mode[2] = uInput[index]
  mode[2] = 0
  return mode, pat

def simulation(control_name, so, disturbances):
  state   = so
  num_tau = tau/dt
  pat     = list( initialSafeController(so) )  
  queue   = multiprocessing.Queue()
  process = multiprocessing.Process(target=controllers[control_name], args=(queue, state, modes[pat.pop()], disturbances, 0))
  t = 0
  for i in range(0, lifeTime):
    if i >= (lifeTime - len(pat)*num_tau):
      break
    if i%(num_tau) == 0:
      mode, pat = supervisor(queue, pat, state, disturbances, int(i/num_tau))
    state = update_model_state(state, disturbances['Te'][i], disturbances['Ti'][i], disturbances['I'][i], mode)
    t = t + dt
  return state
 
def update_model_state(x, Te, Ti, I, mode):
  x[0] = x[0] + dt*mode[1]*2
  x[1] = x[1] + dt*0.01000*( 0.1*mode[0] - x[1] )
  x[2] = x[2] + dt*(1/(0.1*mode[0]))*(
                    - factorTe*2.8811059759131854e-06*(x[2]-Te)
                    - mode[2]*9.34673995175876e-05*(x[2]-Ti)
                    - mode[3]*factorKe*0.001005026*(0.1*mode[0]-x[1])*(x[2]-Ti)
                    + factorI*0.7*0.7*8.403225763080125e-07*I
                    + mode[1]*0.008801843 )
  return x

# if __name__ == '__main__':
#   data = DataProcessing(filepath1, filepath2)
#   simulation("normal", [0.1300, 50.0, 0.0], data.getDisturbanceSeries())
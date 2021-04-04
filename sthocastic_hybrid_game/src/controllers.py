import numpy as np
from interval import interval 
from .config import *

def query(state):   # state[0] = E, state[1] = V, state[2] = T        
    
    for i in range(0,len(zonotopes)):
        z0 = interval[zonotopes[i][0], zonotopes[i][1]] # z0 = T interval
        z1 = interval[zonotopes[i][2], zonotopes[i][3]] # z1 = V interval
        # print( state[2], z0, state[2] in z0 )        
        if (state[2] in z0 and state[1] in z1):
            # We can implement a optimal logical her e, deep learning
            # n = random.randint(0,len(x[i])-1) # 1
            n = 1            
            return {"pat":list(patterns[i][n]),"i":i}
    print("Not found state: ", state)
    
    return {"pat":[-1,-1,-1],"i":-1}

def initialSafeController(state):
    
    pattern = query(state)["pat"]
    
    # h = int( (state.t)/(60*60) ) 
    # m = (state.t)/60- h*60
    # print("time: %d h - %d min"%(h,m) , "-  pattern simple once controller: ",pattern, " +",len(pattern)*5)
    return pattern

def predict_model_state(x, Te, Ti, I, mode):
    x[0] = x[0] + dt*mode[1]*2 # E
    x[1] = x[1] + dt*0.01000*( 0.1*mode[0] - x[1] ) # v
    x[2] = x[2] + dt*(1/(0.1*mode[0]))*(  # T
                        - factorTe*2.8811059759131854e-06*(x[2]-Te)
                        - mode[2]*9.34673995175876e-05*(x[2]-Ti)
                        - mode[3]*factorKe*0.001005026*(0.1*mode[0]-x[1])*(x[2]-Ti)
                        + factorI*0.7*0.7*8.403225763080125e-07*I
                        + mode[1]*0.008801843 )
    return x

def predictiveSafeController(q, state, mode, disturbances, index):  # perturbations predictions
    taumin   = int(tau/60)
    for i in range(index, index + taumin):
        state = predict_model_state(state, disturbances['Te'][i], disturbances['Ti'][i], disturbances['I'][i], mode)
        #t = t + dt
        # s_future.t = s_future.t + dt
    res = query(state)
    pattern = res["pat"]
    # h = int( (state.t)/(60*60) ) 
    # m = (state.t)/60- h*60
    #p = patterns[ int((len(patterns)-1)/2) ]
    #print("time: %d h - %d min"%(h,m) ,"d: ",d, " mode: ", mode, "s: ",s," sfuture: ", s_future , " zonotope: ",z[iz],"-  patterns predictive safe controller: ",pattern)
    #print("s future: ",s_future, "valve: ", mode.v , "pattern predicted: ", pattern)
    #print("zonotope in controller: ", res["i"], " Te: {%d %d %d %d %d} "%(Te[it],Te[it+1],Te[it+2],Te[it+3],Te[it+4]),"pattern: ",pattern)
    q.put(pattern)
    return state

def uppaalController(q,s):
    it = int(it)
    f = ["./sources/uppaal/random.xml","./sources/uppaal/randomc.xml","./sources/uppaal/1c.q"]
    # configXML(f,it)
    # p = callUppaal(f)
    # h = int( (s.t)/(60*60) )
    # m = (s.t)/60- h*60
    # print("time: %d h - %d min"%(h,m) , "-  patterns uppaal controller: ",p, "  +",len(p)*5)
    q.put(p)

controllers = {"normal": predictiveSafeController, "uppaal": uppaalController}

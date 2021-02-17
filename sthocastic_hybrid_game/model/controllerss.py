import numpy as np



# class state:
#     def __init__(self, time, volume, temperature, energyComsuption ):
#         t = time
#         V = volume 
#         T = temperature
#         E = energyComsuption
#     def __str__(self):
#         return '(%5.5f,%5.5f,%5.5f)' % ( T,V,E)
 
# class action:
#     def __init__(self, piston=0, resistor=0, valve=0, expand=0):
#         p   = piston
#         r   = resistor 
#         v   = valve   
#         f   = expand
#     def __str__(self):
#         return '(p=%d,r=%d,v=%d,f=%d)' % (p, r,v,f)
        #return '(%5.2f,%5.2f,%5.2f,%5.2f)' % (p, r,v,f)


# dt_      = 15*60                          # Real time of the data 
# H   = 1*24*60*60                # Real time Interval from  [0-Horizont]
# H_uppaal = 25*8+10       
# nrSteps  = 15              # UPPAAL
# step     = tau/60          # UPPAAAL

# num_ = int(H/dt_)               # Num of intervals         [0 - num*tau]  , but there are num+1 points  t[0] - t[num]
# t_  = np.linspace(0,H,num_+1)

# si  = state(0 ,0.130000,50.000000,0.000000) 
# it  = 0
# state_curr   = si
# pattern_curr = []
# ai      = action()   #?
# actions = []
# states  = []
# actions.append(ai)        
# states.append(si)
# target = { 'Td' : 40, 'Vd' : 100,}, #data['Target'],   # 21 temperatura de comfort humanos
# modes  = [action(1,0,0,0), 
#                 action(1,1,0,0), 
#                 action(2,0,0,0), 
#                 action(2,1,0,0), 
#                 action(3,0,0,1), 
#                 action(3,1,0,1), 
#                 action(2,0,0,1),
#                 action(2,1,0,1)]

# def uppaalController(q,s):
#     it = int(it)
#     f = ["./sources/uppaal/random.xml","./sources/uppaal/randomc.xml","./sources/uppaal/1c.q"] 
#     configXML(f,it)
#     p = callUppaal(f)
#     h = int( (s.t)/(60*60) ) 
#     m = (s.t)/60- h*60
#     print("time: %d h - %d min"%(h,m) , "-  patterns uppaal controller: ",p, "  +",len(p)*5)
#     q.put(p)

# def initialSafeController(s):
#     pattern = query(s)["pat"]
#     print(":)) ",s.t,s.T,s.V, pattern)
#     h = int( (s.t)/(60*60) ) 
#     m = (s.t)/60- h*60
#     print("time: %d h - %d min"%(h,m) , "-  pattern simple once controller: ",pattern, " +",len(pattern)*5)
#     return pattern

# def predictiveSafeController(q,s):  # perturbations predictions
#     #pat = pattern_curr
#     #print("s func: ", s)
#     s_future = s
#     taumin   = int(tau/60)
#     for i in range(it,it+taumin):
#         E = s_future.E + dt*mode.r*2  # dt = 0.1
#         V = s_future.V + dt*rate*( 0.1*mode.p - s_future.V ) # 0.5 = rate 0.01 = rate            rate_volume_change = 0.0002 # 0.193 
#         T = s_future.T + dt*(1/(0.1*mode.p))*( 
#                     - factorTe*2.8811059759131854e-06*(s_future.T-Te[i]) 
#                     - mode.v*9.34673995175876e-05*(s_future.T-Ti[i])                 # valve
#                     - mode.f*factorKe*0.001005026*(0.1*mode.p-s_future.V)*(s_future.T-Ti[i])
#                     + factorI*0.7*0.7*8.403225763080125e-07*I[i]
#                     + mode.r*0.008801843 )#0.00048018432931886426
#         s_future.E = E
#         s_future.V = V
#         s_future.T = T
#         s_future.t = s_future.t + dt
#     obj = query(s_future)
#     pattern = obj["pat"]            
#     h = int( (s_future.t)/(60*60) ) 
#     m = (s_future.t)/60- h*60
#     #p = patterns[ int((len(patterns)-1)/2) ]
#     #print("time: %d h - %d min"%(h,m) ,"d: ",d, " mode: ", mode, "s: ",s," sfuture: ", s_future , " zonotope: ",z[iz],"-  patterns predictive safe controller: ",pattern)
#     #print("s future: ",s_future, "valve: ", mode.v , "pattern predicted: ", pattern)
#     print("zonotope in controller: ", obj["i"], " Te: {%d %d %d %d %d} "%(Te[it],Te[it+1],Te[it+2],Te[it+3],Te[it+4]),"pattern: ",pattern)
#     q.put(pattern)

def predictiveSafeController():
    return 1.0

def uppaalController():
    return 0.0
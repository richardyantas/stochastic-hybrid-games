import multiprocessing
import controllerss

# dataRead = pd.read_csv("../datasets/Solargis_min15_Almeria_Spain.csv")
# valveRead= pd.read_csv("../datasets/valve.csv")  # t1,t2,dur  
# User a few function with a short content 


# def run_experiment (controlName)
def simulation(controlName):     # maybe it should be called run_experiment 
    controllers_ = {"normal":controllerss.predictiveSafeController,"uppaal":controllerss.uppaalController}
    s        = si      
    dt       = dt
    num_tau  = tau/dt
    pat      = initialSafeController(s)   # Safe Pattern to start
    pattern_curr = list(pat)
    state_curr = s
    print("***********************************ONCE********")
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=controllers[controlName], args=(q,s))
    for i in range(0,num-H_uppaal):  # H_uppaal offset - Sending Predictions Pertirbuation 
        if i%(num_tau) == 0:
            if(len(pat) == 0):
                pat = q.get()
                print("*************************************************")                                     
                print(" zonotope in python: ", query(s)["i"] )
                d = pat.pop(0)
                mode = action(modes[d].p,modes[d].r,0,modes[d].f) 
            elif(len(pat) == 1):
                print("..................................................")             
                print("state sent to uppaal: ",s," valve: ",  )
                #time.sleep(1)
                d = pat.pop(0)           
                mode = action(modes[d].p,modes[d].r,0,modes[d].f) 
                print("mode python: ", mode)
                print("List of possible patterns to next state:", x[query(test(s))["i"]])   ## ??????????
                #p.join()               #??
                p = multiprocessing.Process(target=controllers[controlName], args=(q,s))
                p.start()
            elif(len(pat) > 1):
                d = pat.pop(0) 
                mode = action(modes[d].p,modes[d].r,0,modes[d].f) 
            mode.v = gValves[int(i/num_tau)]
            
            print("d: ",d)
        E = s.E + dt*mode.r*2
        V = s.V + dt*0.01000*( 0.1*mode.p - s.V ) 
        T = s.T + dt*(1/(0.1*mode.p))*( 
                    - factorTe*2.8811059759131854e-06*(s.T-Te[i])
                    - mode.v*9.34673995175876e-05*(s.T-Ti[i])
                    - mode.f*factorKe*0.001005026*(0.1*mode.p-s.V)*(s.T-Ti[i]) 
                    + factorI*0.7*0.7*8.403225763080125e-07*I[i]
                    + mode.r*0.008801843 )#0.00048018432931886426 #  0.1*mode.p-V  ->  T.T
        t = s.t + dt
        s = state(t,V,T,E)
        h = int( (s.t)/(60*60) ) 
        m = (s.t)/60-h*60
        it = i
        state_curr = s         
        #print("it: ",it,"time: %d h - %d min"%(h,m)," state: ",state_curr,"- Te: ",Te[i])
        actions.append(mode)
        states.append( s )
    return {"s": states, "a": actions, "H":H}
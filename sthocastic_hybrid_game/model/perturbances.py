import random

self.T_e = dataRead['Temperature'].values.tolist()[0:num_+1]
self.I_  = dataRead['GTI'].values.tolist()[0:num_+1]
v_  = valveRead['Flow'].values.tolist()[0:num_+1] 
self.dt  = 60.0
self.num = int(self.H/self.dt)+1
self.t   = np.linspace(0,self.H,self.num)
self.Te  = np.interp(self.t,t_,self.T_e)
self.I   = np.interp(self.t,t_,self.I_)
#
self.Ti  = np.ones(self.num+1)*TwaterIn  # In c++ 25
#self.si  = state(200*60 ,0.23,50,0) #state(0,0.23,50,0)   # start in the future



self.v   = trapezoideToRectangleInterpolation(np.interp(self.t,t_ ,v_),self.num)  
gValves = (np.zeros(24*12)).tolist()


def randomValve(self):
    value = random.randint(0,20)
    if value == 3:
        return 1 
    return 0


def randomValve():
        value = random.randint(0,20)
        if value == 3:
            return 1 
        return 0

def valvesGeneration():
    numValveActions = 5
    dvs = 1*3  # 1*60/5
    for i in range(0,numValveActions):
        # int(random.gauss(7*60/5,1*60/5) )
        gValves[ int(random.gauss(7*60/5, dvs) )  ] = 1
        gValves[ int(random.gauss(13*60/5,dvs) )  ] = 1
        gValves[ int(random.gauss(19*60/5,dvs) )  ] = 1
    print("Valves: ", gValves)
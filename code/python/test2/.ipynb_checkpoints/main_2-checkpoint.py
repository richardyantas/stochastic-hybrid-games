import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from fractions import Fraction

#cwater = 4177.6  # J/(Kg*K)
#density = 997   # kg/m3
#x1 = cwater*density/1000
#print ( "x1 = %d",x1) #  4165.0672


dataRead = pd.read_csv("../SolarEnergy/Solargis_min15_Almeria_Spain.csv")

class state:
    def __init__(self, time, volume, temperature, energyComsuption ):
        self.t = time
        self.V = volume 
        self.T = temperature
        self.E = energyComsuption


class action:
    def __init__(self, piston=0, resistor=0, valve=0):
        self.p = piston   #{-1,0,1}
        self.r = resistor #{0,1}
        self.v = valve   #{0,1}

class automaton:
    
    def __init__(self, data):
        self.H = data['Horizont']  
        self.tau = data['tau']
        self.num = self.H / self.tau
        self.si = data['stateInit']
        self.states = []
        self.states.append(self.si)


        self.d = data['Disturbance']
        self.actions = []
        self.target = data['Target']
        self.rate_volume_change = 0.0002

# 0.193

    def post(self,s,a,i):
        V = s.V + self.tau*(self.rate_volume_change*a.p)
        
        if a.p != -1:
            T = s.T + (1/(4165.0672*V))*self.tau*( -12*0.001*(s.T-self.d['Te'][i]) -
                                   a.v*4.186*0.093*(s.T-self.d['Ti'][i]) -
                                   a.p*4.186*0.093*(s.T-self.d['Ti'][i]) +
                                   0.001*3.5*self.d['I'][i]+a.r*2                                    
                                   )
        else:
            T = s.T + (1/(4165.0672*V))*self.tau*( -12*0.001*(s.T-self.d['Te'][i]) -
                                   a.v*4.186*0.093*(s.T-self.d['Ti'][i]) +
                                   0.001*3.5*self.d['I'][i]+a.r*2                                    
                                   )
        E = s.E + self.tau*a.r*2
        return state(s.t+tau,V,T,E)

    def controller(self,s):
        a = action()
        if s.T < self.target['Td']:
            a.r = 1
            if s.V <= 0.1:
                a.p = 0
            else:
                a.p = -1
        if s.T > self.target['Td']:
            a.r = 0
            if s.V >= 0.3:
                a.p = 0
            else:
                a.p = 1

        a.v = 0
        self.actions.append(a)  # Plot actions
        return a

    def simulation(self):
        s = self.si        
        for i in range(0,self.num-1):
            a = self.controller(s)

            r = float(Fraction(i*self.tau,3600))
            if (8 < r and r < 8.5) or (19 < r and r < 19.5):
                a.v = 1
            else:
                a.v = 0 

            #if a.p != -1:
            s = self.post(s,a,i)
            self.states.append(s)

            

tau = 15*60
Horizont = 2*24*60*60 
num = Horizont/tau

data = {
    'tau' : tau,
    'Horizont': Horizont, #2976*15*60
    'num': num,
    'Disturbance' : {
        'Te'  : dataRead['Temperature'].values.tolist()[0:num],
	    'Ti'  : [15]*(num),
	    'I'   : dataRead['GTI'].values.tolist()[0:num]
    },
    'Target':{
        'Td' : 25,   # 21 temperatura de comfort humano
        'Vd' : 100,
    },
    
    'stateInit': state(0,2*100*0.001,13,0)
}


A = automaton(data)
A.simulation()

T = []
V = []
E = []
time = []

for i in A.states:
    T.append(i.T)
    V.append(1000*i.V)
    E.append(i.E)
    time.append(i.t)

t = [] 
for i in time:
    t.append( float(Fraction(i,3600)) )

# print("time: %d, T: %d, Te: %d",len(t),len(T),len(Te))



taup = 5*60
Horizont = 2*24*60*60 
nump = Horizont/taup


t = t
Te = data['Disturbance']['Te']



tp = np.linspace(0,Horizont,nump)
print(tp)

Tep = np.interp(tp,t,Te)

print(Horizont)

print(len(t),len(Te), len(tp),len(Tep))

#plt.stem(Tep)
#plt.plot(t,Te)
#plt.plot(tp,Tep)
#plt.grid(True)
#plt.show()

print("ddd")



'''

grid = plt.GridSpec(4, 4, wspace=0.5, hspace=0.7)

#plt.figure(figsize=(9, 6))
# 2x3 
# 2x3x1   
# 2x3x2
plt.subplot(grid[0, 0])
#plt.bar(names, values)
plt.plot(t, data['Disturbance']['I'],label='I')
plt.ylabel('Irradiance(Kw/m2)')
plt.xlabel('time(hrs)')
plt.legend()
plt.grid(True)

plt.subplot( grid[0, 1:])
#plt.scatter(names, values)
plt.plot(t,data['Disturbance']['Te'],label='Te')
plt.ylabel('Te(Celsius)')
plt.xlabel('time(hrs)')
plt.legend()
plt.grid(True)

#plt.subplot(133)
plt.subplot( grid[1,:2] )
#plt.plot(names, values)
plt.plot(t,T,label='T')
plt.ylabel('T(Celsius)')
plt.xlabel('time(hrs)')
#plt.suptitle('Categorical Plotting')
plt.legend()
plt.grid(True)


plt.subplot( grid[2,:2] )
#plt.plot(names, values)
plt.plot(t,V,label='T')
plt.ylabel('V(L)')
plt.xlabel('time(hrs)')
#plt.suptitle('Categorical Plotting')
plt.legend()
plt.grid(True)

plt.subplot( grid[1:3,2:4] )
#plt.plot(names, values)
plt.plot(T,V,'black')
plt.ylabel('V(L)')
plt.xlabel('T(Celsius)')
#plt.suptitle('Categorical Plotting')
plt.legend()
plt.grid(True)


plt.subplot( grid[3,:2] )
#plt.plot(names, values)
plt.plot(t,E,'r')
plt.ylabel('E(kJ)')
plt.xlabel('time(Hrs)')
#plt.suptitle('Categorical Plotting')
plt.legend()
plt.grid(True)


plt.show()

'''
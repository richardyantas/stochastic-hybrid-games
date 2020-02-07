import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from fractions import Fraction

#cwater = 4177.6  # J/(Kg*K)
#density = 997   # kg/m3
#x1 = cwater*density/1000
#print ( "x1 = %d",x1) #  4165.0672


def sgn(a):
    if(a>0):
        return 1
    if(a<0 or a==0):
        return -1
    


class state:
    def __init__(self, time, volume, temperature, energyComsuption ):
        self.t = time
        self.V = volume 
        self.T = temperature
        self.E = energyComsuption

class action:
    def __init__(self, piston=0, resistor=0, valve=0):

        # There are 2 cases 
        # 1.- {-1,0,1}  means {D,S,I}
        # 2.- {-1,0,1}  means {Lower Position,K,Upper Position} If it exist.

        #self.pv  = pistonv   #{-1,0,1}
        self.p   = piston
        self.r   = resistor #{0,1}
        self.v   = valve    #{0,1}


class automaton:
    
    def __init__(self, data):

        self.H   = data['H']  
        self.tau = data['tau'] # Passing to seconds
        self.num = self.H / self.tau + 1
        
        self.v   = data['valve']

        self.si  = data['stateInit']
        self.ai  = action()

        self.states  = []
        self.actions = []
        self.actions.append(self.ai)
        
        self.states.append(self.si)

        self.d = data['D']        
        self.target = data['Target']
        self.rate_volume_change = 0.0002

# 0.193

    def post(self,s,a,i):

        if a.p == -1:
            is_expand = 0     # Drain
        if a.p == 0:    
            is_expand = 0     # Keep
        if a.p == 1:
            is_expand = 1     # Merge

        E = s.E + self.tau*a.r*2
        #V = s.V + self.tau*(self.rate_volume_change*a.p)
        V = s.V + self.tau*0.001*( 0.1*(a.p+2) -s.V )



        T = s.T + (1/V)*self.tau*( -2.8811059759131854e-06*(s.T-self.d['Te'][i]) -
                    
                    a.v*9.34673995175876e-05*(s.T-self.d['Ti'][i]) -
                    
                    is_expand*9.34673995175876e-05*(s.T-self.d['Ti'][i]) +
                    
                    8.403225763080125e-07*self.d['I'][i]+a.r*0.00048018432931886426                                    
                                   )

        '''
        T = s.T + (1/(4165.0672*V))*self.tau*( -12*0.001*(s.T-self.d['Te'][i]) -
                    
                    a.v*4.186*0.093*(s.T-self.d['Ti'][i]) -
                    
                    is_expand*4.186*0.093*(s.T-self.d['Ti'][i]) +
                    
                    0.001*3.5*self.d['I'][i]+a.r*2                                    
                                   )
        '''
        



        return state(s.t+tau,V,T,E)



    def controller(self,s):

        if s.T < self.target['Td']:
            r = 1
            if s.V <= 0.1:
                p = 0
            else:
                p = -1
        if s.T > self.target['Td']:
            r = 0
            if s.V >= 0.3:
                p = 0
            else:
                p = 1

        v = 0
        return action(p,r,v)


    def simulation(self):
        s = self.si        
        for i in range(0,self.num-1):
            a = action()
            
            if i%3 == 0:
                a = self.controller(s)

            # added  (I think it required to add self.) 
            a.v = v[i]

            #r = float(Fraction(i*self.tau,3600))
            #if (8 < r and r < 8.5) or (19 < r and r < 19.5):
            #    a.v = 1
            #else:
            #    a.v = 0 

            #if a.p != -1:

            

            s = self.post(s,a,i)

            self.actions.append(a)  # Plot actions
            self.states.append(s)
    
    def getT(self):
        T = []
        for i in A.states:
            T.append(i.T)
        return T

    def getV(self):
        V = [] 
        for i in A.states:
            V.append(i.V)            
        return V

    def getE(self):
        E = [] 
        for i in A.states:
            E.append(i.E)            
        return E

    def getTime(self):
        time = [] 
        for i in A.states:
            time.append(i.t)            
        return time

    def getr(self):
        r = []
        for i in A.actions:
            r.append(i.r)
        return r
    
    def getp(self):
        p = []
        for i in A.actions:
            p.append(i.p+6)
        return p

    def getv(self):
        v = []
        for i in A.actions:
            v.append(i.v+3)
        return v

'''
    Tree Strategy

    1. Data collected interpolate from 100 to 1000 points which a tau beetwen points to 1minute
        1.1 we have 10 points with tau = 15min if we changue tau tovalve 1 min then we have 100*15
        1.2 
    2. 
'''

            
dataRead = pd.read_csv("Solargis_min15_Almeria_Spain.csv")
valveRead= pd.read_csv("valve.csv")  # t1,t2,dur

tau_ = 15*60           # Real time of the data 
Horizont = 2*24*60*60      # Real time Interval from  [0-Horizont]
num_ = Horizont/tau_    # Num of intervals         [0 - num*tau]  , but there are num+1 points  t[0] - t[num]
t_  = np.linspace(0,Horizont,num_+1)
T_e = dataRead['Temperature'].values.tolist()[0:num_+1]
I_  = dataRead['GTI'].values.tolist()[0:num_+1]
v_  = valveRead['Flow'].values.tolist()[0:num_+1] 

print(len(t_))
print(len(I_))
print(len(v_))


tau = 60
num = Horizont/tau
t   = np.linspace(0,Horizont,num+1)
Te  = np.interp(t,t_,T_e)
I   = np.interp(t,t_,I_)
v   = np.interp(t,t_ ,v_)
Ti  = np.ones(num+1)*15


print(len(Ti))


data = {
    'tau' : tau,  # Passing to seconds from hours
    'H'   : Horizont,# Passing to seconds from hours  2976*15*60
    'num' : num,
    'D'   : {
                'Te'  : Te, #dataRead['Temperature'].values.tolist()[0:num],
                'Ti'  : Ti,
                'I'   : I,
            },
    
    'valve': v,
    'Target': {
                'Td' : 40,   # 21 temperatura de comfort humano
                'Vd' : 100,
              },
    
    'stateInit': state(0,2*100*0.001,13,0)
}


A = automaton(data)
A.simulation()
#t = [] 
#for i in A.getTime():
#    t.append( float(Fraction(i,3600)) )

# print("time: %d, T: %d, Te: %d",len(t),len(T),len(Te))


print( len(t) , len(data['D']['I']) , len(A.getT()) )


#plt.figure( figsize=(11, 9))



fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('time(s)')
ax1.set_ylabel('Enviornment Temperature', color = color)
ax1.plot(t,data['D']['Te'], color=color)
ax1.tick_params(axis='y', labelcolor = color)
plt.grid(True)
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Irradiance', color=color)
ax2.plot(t,data['D']['I'],color = color)
ax2.tick_params(axis='y',labelcolor=color)




#plt.plot(t, data['D']['Te'],label='Te')
#plt.ylabel('Te(Celsius)')
#plt.xlabel('time(hrs)')
#plt.legend()


plt.figure( figsize=(11, 11))

grid = plt.GridSpec(4, 4, wspace=0.8, hspace=0.7)


plt.subplot( grid[0,:2] )
plt.plot(t, A.getT() ,label='T')
plt.ylabel('T(Celsius)')
plt.xlabel('time(hrs)')
plt.legend()
plt.grid(True)

plt.subplot( grid[1,:2] )
plt.plot(t,A.getV(),label='T')
plt.ylabel('V(L)')
plt.xlabel('time(hrs)')
plt.legend()
plt.grid(True)

plt.subplot( grid[1:3,2:4] )
plt.plot(A.getT(),A.getV(),'black')
plt.ylabel('V(L)')
plt.xlabel('T(Celsius)')
plt.legend()
plt.grid(True)

plt.subplot( grid[2,:2] )
plt.plot(t,A.getE(),'r')
plt.ylabel('E(kJ)')
plt.xlabel('time(Hrs)')
plt.legend()
plt.grid(True)


# but have shapes (2881,) and (576,)

plt.subplot( grid[3,:2] )
plt.plot(t,A.getr(),'r')
plt.plot(t,A.getv(),'g')
plt.plot(t,A.getp(),'b')

plt.axis([0,Horizont,0,8])
plt.ylabel('{r,v,p}')
plt.xlabel('time(Hrs)')
plt.legend()
plt.grid(True)




plt.show()

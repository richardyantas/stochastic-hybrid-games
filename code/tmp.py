import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import os
import random
from patterns5 import *

def trapezoideToRectangleInterpolation(a, nnum):
    for i in range(0,len(a)):
        if a[i] != 1.0 and  a[i] != 0.0:
            a[i] = 0.0
    return a

class state:
    def __init__(self, time, volume, temperature, energyComsuption ):
        self.t = time
        self.V = volume 
        self.T = temperature
        self.E = energyComsuption
class action:
    def __init__(self, piston=0, resistor=0, valve=0, expand=0):
        self.p   = piston
        self.r   = resistor 
        self.v   = valve   
        self.f   = expand

class automaton:
    def __init__(self):
        dataRead = pd.read_csv("Solargis_min15_Almeria_Spain.csv")
        valveRead= pd.read_csv("valve.csv")  # t1,t2,dur  
        dt_      = 15*60                          # Real time of the data 
        self.H   = 1*24*60*60                # Real time Interval from  [0-Horizont]
        num_ = int(self.H/dt_)               # Num of intervals         [0 - num*tau]  , but there are num+1 points  t[0] - t[num]
        t_  = np.linspace(0,self.H,num_+1)
        T_e = dataRead['Temperature'].values.tolist()[0:num_+1]
        I_  = dataRead['GTI'].values.tolist()[0:num_+1]
        v_  = valveRead['Flow'].values.tolist()[0:num_+1] 
        self.dt  = 60
        self.num = int(self.H/self.dt)+1
        self.t   = np.linspace(0,self.H,self.num+1)
        self.Te  = np.interp(self.t,t_,T_e)
        self.I   = np.interp(self.t,t_,I_)
        self.v   = trapezoideToRectangleInterpolation(np.interp(self.t,t_ ,v_),self.num)  
        self.Ti  = np.ones(self.num+1)*TwaterIn  # In c++ 25
        self.si  = state(0,0.12,50,0)
        self.ai  = action()   #?
        self.actions = []
        self.states  = []
        self.actions.append(self.ai)        
        self.states.append(self.si)
        self.target = { 'Td' : 40, 'Vd' : 100,}, #data['Target'],   # 21 temperatura de comfort humano
        self.modes = [action(1,0,0,0), action(1,1,0,0), action(2,0,0,0), action(2,1,0,0), action(3,0,0,1), action(3,1,0,1), action(2,0,0,1),action(2,1,0,1)]
                        
    def plotBefore(self):
        #plt.subplot( grid[3:4,2:4] )
        plt.plot(self.t,self.Te,'g')
        plt.ylabel('Te')
        plt.xlabel('time(s)')
        plt.legend()
        plt.grid(True)        

    def controller(self,s):
        patterns = query(s)
        n  = len(patterns)             # check
        nu = random.randint(0,n-1)    # check
        print("time: ", s.t, "-  patterns controller: ",patterns[nu])
        return patterns[nu]  # random 

    def simulation(self):
        s    = self.si        
        dt   = self.dt 
        num_tau = tau/dt          
        pat  = self.controller(s)
        d    = pat.pop(0)
        print("size: ",len(self.v),"-", self.num)
        for i in range(0,self.num):     # (0,self.num-1)         
            if i%(num_tau) == 0 and i!=0: 
                if( len(pat) == 0 ):
                    pat = self.controller(s) # Tomara mas tiempo para el siguiente 
                    d = pat.pop(0)
                else:
                    d = pat.pop(0)              
            #mode = action(self.modes[d].p,self.modes[d].r, 0,self.modes[d].f)
            mode = action(self.modes[d].p,self.modes[d].r,self.v[i],self.modes[d].f)
            #print("mode v: ",mode.v," r: ",mode.r, " p: ",mode.p)
            E = s.E + dt*mode.r*2  # dt = 0.1
            V = s.V + dt*rate*( 0.1*mode.p - s.V ) # 0.5 = rate 0.01 = rate            self.rate_volume_change = 0.0002 # 0.193 
            T = s.T + dt*(1/(0.1*mode.p))*( 
                        - factorTe*2.8811059759131854e-06*(s.T-self.Te[i]) 
                        - mode.v*9.34673995175876e-05*(s.T-self.Ti[i])                 # valve
                        - mode.f*factorKe*0.001005026*(0.1*mode.p-V)*(s.T-self.Ti[i])
                        + factorI*0.7*0.7*8.403225763080125e-07*self.I[i]
                        + mode.r*0.00880184 )#0.00048018432931886426
            #print("T: ",T,"V: ",V,"E: ",E)
            t = s.t + dt
            s = state(t,V,T,E)
            self.actions.append(mode)  
            self.states.append( s )


    def plot(self):
        T = []
        V = []
        E = []
        r = []
        p = []
        v = []
        time = []
        for i in self.states:
            T.append(i.T)
            V.append(i.V)
            E.append(i.E)
            time.append(i.t)
        for i in self.actions:
            r.append(i.r)
            p.append(i.p+4)
            v.append(i.v+2)
        plt.figure( figsize=(11, 11))
        grid = plt.GridSpec(4, 4, wspace=0.8, hspace=0.7)
        plt.subplot( grid[0,:2] )
        #plt.plot(t, A.getT() ,label='T')
        plt.plot(time,T ,label='T',linewidth=0.8)                        # ?
        plt.ylabel('T(Celsius)')
        plt.xlabel('time(s)')
        plt.legend()
        plt.grid(True)
        plt.subplot( grid[1,:2] )
        plt.plot(time,V,label='T',linewidth=0.8)
        plt.ylabel('V(L)')
        plt.xlabel('time(s)')
        plt.legend()
        plt.grid(True)
        plt.subplot( grid[1:3,2:4] )
        plt.plot(T,V,'black',linewidth=0.5)
        plt.plot([R[1][0] , R[1][1], R[1][1], R[1][0],R[1][0]],
                 [R[0][0] , R[0][0], R[0][1], R[0][1],R[0][0] ],
                 'red',label="R region")
        plt.plot([S[1][0] , S[1][1], S[1][1], S[1][0],S[1][0]],
                 [S[0][0] , S[0][0], S[0][1], S[0][1],S[0][0]],
                 'purple',label="S region")
        plt.axis([10,100,0,0.4])
        plt.ylabel('V(L)')
        plt.xlabel('T(C)')
        plt.legend()
        plt.grid(True)
        plt.subplot( grid[2,:2] )
        plt.plot(time,E,'r',linewidth=0.8)
        plt.ylabel('E(kJ)')
        plt.xlabel('time(s)')
        plt.legend()
        plt.grid(True)
        # but have shapes (2881,) and (576,)
        plt.subplot( grid[3,:2] )
        plt.plot(time,r,'r',linewidth=0.8)
        plt.plot(time,v,'g',linewidth=0.8)
        plt.plot(time,p,'b',linewidth=0.8)
        plt.axis([0,self.H,0,8])
        plt.ylabel('{r,v,p}')
        plt.xlabel('time(s)')
        plt.legend()
        plt.grid(True)
        plt.subplot( grid[3:4,2:4] )
        plt.plot(time,v,'g')
        plt.ylabel('valve')
        plt.xlabel('time(s)')
        plt.legend()
        plt.grid(True)
        plt.show()

A = automaton()
#A.plotBefore()
A.simulation()
A.plot()

'''
 for i in range(0,4):
...     print(i)
... 
0
1
2
3


def trapezoideToRectangleInterpolation(a, nnum):
    
    la = len(a)
    b  = np.zeros(nnum+1)
    lb = len(b)
    r  = lb/la
    for i in range(0,la):
        for k in range(0,int(r)):
            if a[i] == 1:
                b[ int((r*i)+k) ] = 1
    
    #print("Original")
    #for i in range(0,len(a)):
    #    print(a[i],end =" ")

    for i in range(0,len(a)):
        if a[i] != 1.0 and  a[i] != 0.0:
            a[i] = 0.0
    return a

'''
import numpy as np 
import pandas as pd
#import matplotlib
import matplotlib.pyplot as plt
import subprocess
import os
import random
from patterns import *


def trapezoideToRectangleInterpolation(a, nnum):
    la = len(a)
    b  = np.zeros(nnum+1)
    lb = len(b)
    r  = lb/la
    for i in range(0,la):
        for k in range(0,int(r)):
            if a[i] == 1:
                b[ int((r*i)+k) ] = 1
    return b

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
        dt_ = 15*60                          # Real time of the data 
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
        self.Ti  = np.ones(self.num+1)*10
        self.si  = state(0,2*1300*0.001,50,0)
        self.ai  = action()   #?
        self.actions = []
        self.states = []
        self.actions.append(self.ai)        
        self.states.append(self.si)

        self.target = {
                'Td' : 40,   # 21 temperatura de comfort humano
                'Vd' : 100,
              }, #data['Target']
    
    def controller(self,s):
        patterns = query(s)
        lista = []
        n = len(patterns)             # check
        nu = random.randint(0,n-1)    # check
        for i in range(0,3): # check
            if patterns[nu].item(i) != -1:
                lista.append( patterns[nu].item(i) )
        print("n: ",n,",nu: ",nu,",lista: ",lista)
        return lista  # random 

    def simulation(self):
        #fe = 2.5
        fe = 1
        fi = 0.5
        
        ke = 10 
        s  = self.si        
        dt = self.dt
        mode = action()
        tau = 5*60
        num_tau = tau/dt
        modes = []
        modes.append( action(1,0,0,0) )
        modes.append( action(1,1,0,0) )
        modes.append( action(2,0,0,0) )
        modes.append( action(2,1,0,0) )
        modes.append( action(3,0,0,1) )
        modes.append( action(3,1,0,1) )
        modes.append( action(2,0,0,1) )
        modes.append( action(2,1,0,1) )          
        pat = self.controller(s)
        print("pat: ",pat)
        mode = modes[pat.pop()]
        for i in range(0,self.num-1):          
            #mode = modes[0]
            if i%(num_tau) == 0 and i!=0: 
                if( len(pat) == 0 ):
                    pat = self.controller(s) # Tomara mas tiempo para el siguiente 
                    #print("pat: ",pat)
                    mode = modes[pat.pop()]
                else:
                    mode = modes[pat.pop()]   #  ?? 
            #mode.v = self.v[i]
            #print(mode.v)
            E = s.E + dt*mode.r*2  # dt = 0.1
            V = s.V + dt*0.01*( 0.1*mode.p - s.V ) # 0.5 = rate            self.rate_volume_change = 0.0002 # 0.193 
            T = s.T + dt*(1/(0.1*mode.p))*( 
                        - fe*2.8811059759131854e-06*(s.T-self.Te[i]) 
                        - mode.v*9.34673995175876e-05*(s.T-self.Ti[i])
                        - mode.f*ke*0.001005026*(0.1*mode.p-V)*(s.T-self.Ti[i])
                        + fi*8.403225763080125e-07*self.I[i]
                        + mode.r*0.00048018432931886426 )
            t = s.t + dt
            s = state(t,V,T,E)
            #s = self.post(s,a,i)
            #Plot actions
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
            #print(i.v)
        
        plt.figure( figsize=(11, 11))
        grid = plt.GridSpec(4, 4, wspace=0.8, hspace=0.7)
        plt.subplot( grid[0,:2] )
        #plt.plot(t, A.getT() ,label='T')
        plt.plot(time,T ,label='T')                        # ?
        plt.ylabel('T(Celsius)')
        plt.xlabel('time(hrs)')
        plt.legend()
        plt.grid(True)

        plt.subplot( grid[1,:2] )
        plt.plot(time,V,label='T')
        plt.ylabel('V(L)')
        plt.xlabel('time(hrs)')
        plt.legend()
        plt.grid(True)

        plt.subplot( grid[1:3,2:4] )
        plt.plot(T,V,'black')
        plt.ylabel('V(L)')
        plt.xlabel('T(Celsius)')
        plt.legend()
        plt.grid(True)

        plt.subplot( grid[2,:2] )
        plt.plot(time,E,'r')
        plt.ylabel('E(kJ)')
        plt.xlabel('time(Hrs)')
        plt.legend()
        plt.grid(True)
        # but have shapes (2881,) and (576,)
        plt.subplot( grid[3,:2] )
        plt.plot(time,r,'r')
        plt.plot(time,v,'g')
        plt.plot(time,p,'b')
        plt.axis([0,self.H,0,8])
        plt.ylabel('{r,v,p}')
        plt.xlabel('time(Hrs)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def test(self):
        for i in range(0,len(self.v)):
            print(self.v[i])



A = automaton()
A.simulation()
A.plot()
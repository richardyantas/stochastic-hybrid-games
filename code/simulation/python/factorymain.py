import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.widgets import Slider, Button, RadioButtons
from   utils import *

T   = 1         # importan to gauss 0.1
dm  = 0.02
Mc  = 100
Kc  = 5         #16/4
Ce  = 4.186*1000
A_t = 2.5557
A_c = 2
dq  = 2000      # watts

tmax= 86400
num = int(tmax/T)
t   = np.arange(0, tmax, T)

Ieamp  = 1236*5000 
Tinamp = 40
Teamp  = 48

Ie  = Ieamp*gauss(86400/2,86400/8,T,num) 
Tin = Tinamp*gauss(86400/2,86400/8,T,num)
Te  = Teamp*gauss(86400/2,86400/8,T,num)

x = np.zeros((num,1))	
y = np.zeros((num,1))
A = np.zeros((num,1))
d = np.zeros((num,1))


x[0,0] = 40
y[0,0] = 130

va = valve(num)
va.setOneValues(getSec(7),getSec(7.2))
va.setOneValues(getSec(7.3),getSec(7.5))

re = resistance(num)
vo = piston(num)

vp = 0.1 # Piston velocity 


print(  str(-(Kc*A_t)/(Mc*Ce)) + ' ' +  str(A_c/(Mc*Ce)) + ' ' + str((dm/Mc)) + ' ' + str(dq/(Mc*Ce)) )


for i in range(0,num-1):
    if abs(y[i,0]-100*vo.g[i,0]) <= 0:
        y[i+1,0] = y[i,0]  
    else:
        y[i+1,0] = y[i,0] - vp*T*sign( y[i,0]-100*vo.g[i,0] )            

    Mc = y[i,0]
    
    x[i+1,0] = x[i,0] + ( ( -(Kc*A_t)/(Mc*Ce) )*(x[i,0]-Te[i,0]) + (Ie[i,0]*A_c)/(Mc*Ce) - va.g[i,0]*(dm/Mc)*(x[i,0]-Tin[i,0]) + re.g[i,0]*dq/(Mc*Ce))*T
    
    if x[i,0] < 60:
        re.g[i+1,0] = 1
        an = i
    if x[i,0] >= 60:
        if i - an <= 300:
            re.g[i+1,0] = 1
        else:
            re.g[i+1,0] = 0

    if x[i,0] >= 100:
        x[i,0] = 100

#solve(x,y,T,num,A,d,va,re,vo,Mc,Ce,A_t,A_c,dm,dq,Kc,vp,Tin,Ie,Te,Tinamp,Teamp,Ieamp)     

plotSimple(t,x,Ie,re,va)
plotWidget(t,x,y,T,num,A,d,va,re,vo,Mc,Ce,A_t,A_c,dm,dq,Kc,vp,Tin,Ie,Te,Tinamp,Teamp,Ieamp)

plt.show()



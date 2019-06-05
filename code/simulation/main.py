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
#re.setOneValues(getSec(1),getSec(2))
#re.setOneValues(getSec(17),getSec(18))

vo = piston(num)
#vo.setThreeValues(getSec(10),getSec(14))
#vo.setTwoValues(getSec(15),getSec(16))
vp = 0.1 # Piston velocity 

solve(x,y,T,num,A,d,va,re,vo,Mc,Ce,A_t,A_c,dm,dq,Kc,vp,Tin,Ie,Te,Tinamp,Teamp,Ieamp)     

plotSimple(t,x,Ie,re,va)
plotWidget(t,x,y,T,num,A,d,va,re,vo,Mc,Ce,A_t,A_c,dm,dq,Kc,vp,Tin,Ie,Te,Tinamp,Teamp,Ieamp)

plt.show()




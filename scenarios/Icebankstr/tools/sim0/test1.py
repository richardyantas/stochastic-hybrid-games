import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def greedyController(x0,xg):
    numVars = len(x0)
    u = np.ones(numVars)
    for i in range(0,numVars):
        if x0[i] > xg[i]:
            u[i] = 0.0
    return u


c=0.0001 #room transfer coef
cu=0.02  #heating on coef

A = [[-c,c],[c,-c]]
B = [[cu,0.0],[0.0,cu]]
C = A
D = B
x0=[50.0,10.0]
xg=[50.0,200.0]

sys1 = signal.StateSpace(A,B,C,D)
simTime = 60*60*1
controlStep = 15*60
c = greedyController(x0,xg)
tall = []
uall = np.array([]).reshape((0,len(x0)))
xall = np.array([]).reshape((0,len(x0)))


for ti in range(0,simTime,1):
    t=np.linspace(ti,ti+1,10)
    if ti%controlStep==0:
        c = greedyController(x0,xg)
    u=np.transpose([np.ones(len(t))*c[0],np.ones(len(t))*c[1]])
    t1,y1,x1 = signal.lsim(sys1,u,t,x0)
    x0 = x1[len(x1)-3]
    tall = np.concatenate((tall,t1),axis=0)
    uall = np.concatenate((uall,u),axis=0)
    xall = np.concatenate((xall,x1),axis=0)



plt.plot(tall,uall,'r-')
plt.plot(tall,xall,'b-')
plt.show()




import numpy as np
import math
from scipy import signal
import matplotlib.pyplot as plt

def ventilatorController(x,tset,tdelta,v,vcur):    
    troom = x(0)
    if troom > (tset+tdelta):
        return v
    elif troom < (tset-tdelta):
        return 0
    else:
        return vcur
    # if troom >= tset:
    #     return v
    # else:
    #     return 0

def cop(p):
    return (p*95)/100

def pumpBuiltInController(x,ip,P,llib,ulib):
    numSettings = len(P)
    if x[1] <= llib:
        return numSettings-1
    elif x[1] >= ulib:
        return 0
    else:
        return ip
    
def pumpNaiveController(x0,u0,P):
    # returns the index of the pump setting which minimizes the
    # difference between P and Isp
    isp = u0[1]
    dist = [abs(p - isp) for p in P]
    return dist.index(min(dist))

def generateInputs(x0,u0,ti,P,llib,ulib,v):
    numInputs = len(u0)
    controlStep = 15*60
    u1 = u0
    vcur = u0[3]
    tset = 18
    tdelta = 1
    v1 = ventilatorController(x0,tset,tdelta,v,vcur)
    u1[3] = v1
    p = u0[4]
    ip = P.index(p)
    if ti%controlStep==0:
        indexp1 = pumpNaiveController(x0,u0,P)
    indexp1 = pumpBuiltInController(x0,ip,P,llib,ulib)       
    p1 = P[indexp1]
    u1[4] = p1
    u1[5] = cop(p1)
    return u1
    
# initial state
troom = 18
lib = 30000
e = 0
es = 0
    
# constants
cr = 0.005
cjc = 0 # should be a negative constant
ci = 0
ulib = 1000000
llib = 1000

# inputs
ienv = 10.0
isp = ienv*100
tenv = 22.0
P = [0, 5000, 11000] #settings of the pump
v = 4000
vcur = 0
p = P[1] # the current setting
pe = cop(p)


# state space
A = np.array([[-cr,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
B1 = np.array([[ci,0,cr,cjc,0,0],[0,0,0,-1.0,0,1.0],[0,0,0,0,1.0,0],[0,1.0,0,0,0,0]])
B2 = np.array([[ci,0,cr,cjc,0,0],[0,0,0,-1.0,0,1.0],[0,0,0,0,1.0,0],[0,0,0,0,1.0,0]])
C = A
D = B1
x0=[troom,lib,e,es]
u0=[ienv,isp,tenv,vcur,p,pe]
sys1 = signal.StateSpace(A,B1,C,D)
sys2 = signal.StateSpace(A,B2,C,D)


# simulation time in seconds
simTime = 60*60*1

tall = []
uall = np.array([]).reshape((0,len(u0)))
xall = np.array([]).reshape((0,len(x0)))
xx = x0
xxall = np.array([]).reshape((0,len(xx)))
tau=1


for ti in range(0,simTime,1):
    t=np.linspace(ti,ti+1,10)            
    c = generateInputs(x0,u0,ti,P,llib,ulib,v)
    u=np.transpose([
        np.ones(len(t))*c[0],
        np.ones(len(t))*c[1],
        np.ones(len(t))*c[2],
        np.ones(len(t))*c[3],
        np.ones(len(t))*c[4],
        np.ones(len(t))*c[5]])
    # if c[4] < c[1]:
    #     t1,y1,x1 = signal.lsim(sys2,u,t,x0)
    #     xx = np.dot(np.dot(A,xx),ti+1-ti)/10+np.dot(B2,u)
    # else:
    t1,y1,x1 = signal.lsim(sys2,u,t,x0)

    # t1,y1,x1 = signal.lsim2((A, B1, C, D), T=t, U=u, X0=x0,
    #                           rtol=1e-9, atol=1e-11)
    
    xx = (np.dot(A,xx)+np.dot(B2,c))*tau + xx
    x0 = x1[len(x1)-1]
    u0 = u[len(u)-1]
    tall = np.concatenate((tall,t1),axis=0)
    uall = np.concatenate((uall,u),axis=0)
    xall = np.concatenate((xall,x1),axis=0)
    print(xx)
    
np.set_printoptions(threshold='nan')


plt.subplot(221)
plt.plot(tall,xall[:,0])
plt.yscale('linear')
plt.title('Troom')

plt.subplot(222)
plt.plot(tall,xall[:,1])
plt.yscale('linear')
plt.title('L-IB')


plt.subplot(223)
plt.plot(tall,xall[:,2], 'b-' )
plt.plot(tall,xall[:,3], 'r-' )
plt.yscale('linear')
plt.title('Energy')

# plt.subplot(224)
# plt.plot(tall,xall,'b-')
# plt.yscale('linear')
# plt.title('All')

plt.subplot(224)
plt.plot(tall,uall[:,[2,3,4]],'r-')
plt.yscale('linear')
plt.title('All-Inputs')

plt.show()






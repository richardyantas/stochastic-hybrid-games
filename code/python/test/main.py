import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Slider, Button, RadioButtons
from utils import *

from getSolarIncidentAngle import *


tmax= 10*24*60*60
tau = 15*60
num = int(tmax/tau)
t   = np.arange(0, tmax, tau)

#data = pd.read_csv("./SolarEnergy/meteotest_normal_year_87962.csv")
data = pd.read_csv("./SolarEnergy/Solargis_min15_Almeria_Spain.csv")

print( data[0:num] )
#irr = data['Irradiance']
irr =data['GTI'] #Irradiance -> Glocal Tilted Irradiance
Temp=data['Temperature'] # Enviornment Temperature


# Is Assumed, constant efficience indepent to time, for the moment 
# Is not computed the FR over Solar Collector.
# The irradiance got is considering tiled ans azimut angles even the sun around.


irr = irr.to_numpy()
Temp = Temp.to_numpy()
irr = irr[0:num]
Temp = Temp[0:num]


plt.figure(figsize=(9, 3))
plt.subplot(131)
#plt.bar(names, values)
plt.plot(t,Temp,label='Temperature')
plt.legend()
plt.grid(True)
plt.subplot(132)
#plt.scatter(names, values)
plt.plot(t,irr,label='Irradiance')
plt.legend()
plt.grid(True)
plt.show()


'''


tau   =  5*60         # importan to gauss 0.1
dm  =  0.293 # kg/s  #0.02
Mc  =  293.1 # kg
Kc  =  4.1  # w/(m*C)  #5         #16/4
Ce  =  4186 # kJ/(Kg*C)  #4.186*1000
A_t =  1.91 # m2  #2.5557
A_c =  1.91 # m2  #2
dq  =  2 #2000 # watts -> kw
#tmax= 48*60*60
tmax= 4*24*60*60
num = int(tmax/tau)
t   = np.arange(0, tmax, tau)
Ieamp  = 1000 #kg/m2 #1236*5000 
Tinamp = 15  # C
Teamp  = 18.3
vp = 0.1 # Piston velocity
#Ie  = Ieamp*gauss(86400,86400/8,T,num) 
#Tin = Tinamp*gauss(86400,86400/8,T,num)
#Te  = Teamp*gauss(86400,86400/8,T,num)

data = pd.read_csv("../SolarEnergy/SolarPrediction.csv")
irr  =data['Radiation']
Temp =data['Temperature']
irr  = irr.to_numpy()
Temp = Temp.to_numpy()

print("Irradation Total Size:",irr.size)  # 32686 ,  must be 600 samples for two days
print("Samples Num",num)       # 86400

I_env = irr[0:num]
T_env = Temp[0:num]
T_in = 0.5*Temp[0:num]  # Wrong


for i in range(0,num):
    T_env[i] = (T_env[i]-30)/2
T = np.zeros((num,1))	
V = np.zeros((num,1))

print("Irradiation Spliting Size ",I_env.size)
print("Temperature Spliting Size ",T_env.size, "Te[0] = ", T_env[0], "Te[num] = ", T_env[num-1])
print("Temperature state variables size", T.size)

va = valve(num,tau)
#va.setOneValues( getSec(7)   , getSec(7.2) )
#va.setOneValues( getSec(7.3) , getSec(7.5) )
re = resistance(num,tau)
vo = piston(num,tau)

print("Resistance signal size ",re.g.size)

#vo.setThreeValues(getSec(10),getSec(14))
#vo.setTwoValues(getSec(15),getSec(16))
#for i in range(0,num): #0 - 575  -> [0 - num>
#    print(i)

T[0,0] = 45
V[0,0] = 130

########################################

Body temperature 37 C

print("############ CONTROLLER ############")

#def controller(T,V,re,vo,va):
def controller(T,re,i):
    if T[i,0] < 80:
        re.g[i+1,0]=1
    if T[i,0] > 80:
        re.g[i+1,0]=0
    
    # Drain Mechanism
    if T[i,0] > 100:
        T[i,0]=100

print("####################################")

density_water = 997   # kg/m3 
specific_heat = 4.186 # kJ/(kgC)
A=1/(density_water*specific_heat)  #4173.4
#conduction_coef_collector = 4.1 # W/(m2K)
conduction_coef_collector = 4.1*0.001 # KW/(m2K) 
Area_collector = 1.91  # m2
B = conduction_coef_collector*Area_collector #0.00783   > Paper 12*0.001 kW/C replaced over paper.
flow_Rate_water_comsuption = 0.7/(60*60)  #  m3/s
C = specific_heat*flow_Rate_water_comsuption*density_water  #0.193
### Performance ###
efficiency_radiation_collector = 0.9
solar_absorptivity = 0.9
D = efficiency_radiation_collector*solar_absorptivity*Area_collector # 0.1547


print(A," ", B, " ", C, " ",D)



# We need a heat dump equation for 60C temperature start to deacrease the temperature.


for i in range(0,num-1):  # -> [0 - num-2]
    #y[i+1,0]=y[i,0]-vp*T*sign(y[i,0]-300*vo.g[i,0])
    #T[i+1,0]=T[i,0]+tau*(1/4173.4)*(7.83*(T[i,0]-T_env[i])-va.g[i,0]*0.193*(T[i,0]-T_in[i])+1.547*I_env[i]+re.g[i,0]*dq )

    #T[i+1,0]=T[i,0]+tau*(0.000239612785738247/V[0,0])*(7.83*(T[i,0]-T_env[i])-va.g[i,0]*0.193*(T[i,0]-T_in[i])+1.547*I_env[i]+re.g[i,0]*dq )
    #T[i+1,0]=T[i,0]+tau*(A/V[0,0])*(0.0012*(T[i,0]-T_env[i])-va.g[i,0]*C*(T[i,0]-T_in[i])+D*I_env[i]+re.g[i,0]*dq )
    T[i+1,0]=T[i,0]+tau*(A/V[0,0])*(0.0012*(T[i,0]-T_env[i])-va.g[i,0]*C*(T[i,0]-T_in[i])+D*I_env[i]+re.g[i,0]*dq )
    #controller(T,re,i)
    





for i in range(0,num):
    if abs(y[i,0]-300*vo.g[i,0]) <= 0:
        y[i+1,0] = y[i,0]  
    else:
        y[i+1,0] = y[i,0] - vp*T*sign( y[i,0]-300*vo.g[i,0] )            

    Mc = y[i,0]

    #A[i,0]  =  ( va.g[i,0]*(-dm/Mc) - Kc*A_t/(Mc*Ce) )
    #d[i,0]  =  A_c*Ie[i,0]/(Mc*Ce) + va.g[i,0]*Tin[i,0]*dm/Mc + Kc*A_t*Te[i,0]/(Mc*Ce)
    #x[i+1,0]=  x[i,0]/(1-A[i,0]*T) + re.g[i,0]*dq/(Mc*Ce)*T/(1-A[i,0]*T) + d[i,0]*T/(1-A[i,0]*T)
    
    x[i+1,0] = x[i,0] + 0.000006383*(x[i,0]-Te[i,0])
    # control
    if x[i,20] < 0:
        re.g[i+1,0] = 1
        an = i
    if x[i,0] >= 20:
        if i - an <= 300:
            re.g[i+1,0] = 1
        else:
            re.g[i+1,0] = 0

    if x[i,0] >= 100:
        x[i,0] = 100


plt.figure(1)
plt.plot(t,T, label = 'Temperature')
#plt.plot(t, Ie, label = 'Irradiance')
#plt.plot(t, re.g , '-r', label = 'Resistance')
#plt.plot(t, va.g, 'black', label ='Valve')
plt.legend()
plt.grid(True)
#plotSimple(t,x,Ie,re,va)
#plotWidget(t,x,y,T,num,A,d,va,re,vo,Mc,Ce,A_t,A_c,dm,dq,Kc,vp,Tin,Ie,Te,Tinamp,Teamp,Ieamp)
plt.show()





plt.figure(figsize=(9, 3))

plt.subplot(131)
#plt.bar(names, values)
plt.plot(t,T,label='Temperature')
plt.legend()
plt.grid(True)


plt.subplot(132)
#plt.scatter(names, values)
plt.plot(t,I_env,label='Irradiance')
plt.legend()
plt.grid(True)

plt.subplot(133)
#plt.plot(names, values)
plt.plot(t,T_env,label='Temp enviorment')
#plt.suptitle('Categorical Plotting')
plt.legend()
plt.grid(True)
plt.show()

'''

#from pandas import read_csv
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import animation
import time

# international-airline-passengers.csv
# create a differenced series

#             0 <j=i-d< l-d      d < i < l
#             x[i] - x[j]
def forecast(X,pivotWindow,predictionSize):
    days_in_year = pivotWindow
    differenced = list()
    print(X)   
    for i in range(days_in_year, len(X)):
        value = X[i] - X[i - days_in_year]
        differenced.append(value)
    # fit model
    model = ARIMA(differenced, order=(7,0,1))
    model_fit = model.fit(disp=0)
    # multi-step out-of-sample forecast
    start_index = len(differenced)
    end_index   = start_index + predictionSize
    #end_index   = start_index + 49#6
    forecast    = model_fit.predict(start=start_index, end=end_index)
    print(forecast)
    # invert the differenced forecast to something usable
    history = [x for x in X]
    day = 1
    pred = []
    for yhat in forecast:
        #inverted = inverse_difference(history, yhat, days_in_year)
        inverted = yhat + history[-days_in_year] 
        #print('Day %d: %f' % (day, inverted))
        pred.append(inverted)
        history.append(inverted)
        day += 1
    return pred


# https://www.kdnuggets.com/2019/05/animations-with-matplotlib.html
# load dataset
#series = read_csv('international-airline-passengers.csv', header=None)
#dataRead = pd.read_csv('Solargis_min15_Almeria_Spain.csv', header=None)
dataRead = pd.read_csv('Solargis_min15_Almeria_Spain.csv')
H   = 10*24*60*60
dt_ = 15*60
num_= int(H/dt_)
t_  = np.linspace(0,H,num_+1)
T_e = dataRead['Temperature'].values.tolist()[0:num_+1]
I_  = dataRead['GTI'].values.tolist()[0:num_+1]


dt  = 60.0
num = int(H/dt)+1
t   = np.linspace(0,H,num)
Te  = np.interp(t,t_,T_e)
# seasonal difference
#X = series.values[1:,1]
#X = [float(i) for i in X]

''' 
plt.style.use('seaborn-pastel')
fig = plt.figure()
#ax = plt.axes(xlim=(0, 4), ylim=(-50, 50))
ax = plt.axes(xlim=(0, 4), ylim=(0, 20))
line, = ax.plot([], [], lw=3)
def init():
    line.set_data([], [])
    return line,
def animate(i):
    num = 200
    xmax = 3
    u = 1*i
    print(u)
    x = np.linspace(0, xmax, num)
    y = np.array( Te[u:u+num] )
    line.set_data(x, y)
    ax.plot(Te[u:u+num],'o')
    #plt.plot(range(len(f),len(f)+len(pred)),pred,'red')    
    #ax.plot(x, y)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init,frames=1000, interval=100, blit=True)  # interval = 20
#anim.save('sine_wave.gif', writer='imagemagick')
plt.grid(True)
plt.show()
'''


#f = T_e[0:0+4*24+50]   # 200
f = I_[0:0+4*24+50]
#pred = forecast(f,24+11,3)
pred = forecast(f,24+11,3)

#pred2 = np.interp(t,t_,pred)

print("pred size: ",len(pred))
#plt.plot(f,marker='o', color = 'blue')
plt.plot(f,'o')
#plt.plot(range(len(Te),len(Te)+len(pred)),pred,'red')
plt.plot(range(len(f),len(f)+len(pred)),pred,'red')
plt.grid(True)
plt.show() 



### TASK ## 
# Start with 




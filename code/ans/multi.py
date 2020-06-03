
from pandas import read_csv
from statsmodels.tsa.arima_model import ARIMA
import numpy
import matplotlib.pyplot as plt 
# international-airline-passengers.csv
# create a differenced series
def forecast(X):
    days_in_year = 10
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
    end_index   = start_index + 40#6
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


# load dataset
series = read_csv('international-airline-passengers.csv', header=None)
# seasonal difference
X = series.values[1:,1]
X = [float(i) for i in X] 
pred = forecast(X)
plt.plot(X)
plt.plot( range(len(X),len(X)+len(pred)),pred,'red')
plt.show()



'''
import time
import random
import multiprocessing
import os


class A:
    def __init__(self):
        self.a = 3
    def controller(self,q):
        time.sleep(3)
        a = random.randint(0,4)
        b = random.randint(0,4)
        pattern = [a,b]
        q.put(pattern)
        print('Control finished - process id:', os.getpid())
    
    def simulation(self):
        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=self.controller, args=(q,))
        print("calling controller for next i = 0 ")
        p.start()
        pattern = q.get()
        print("Getting the pattern precalculated for it=0 and using in this status tp: ",pattern)
        p.join()
        p = multiprocessing.Process(target=self.controller, args=(q,))
        print("calling controller for next i = 1 ")
        p.start()
        for i in range(0,100):
            if(i%5 == 0 and i != 0):
                pattern = q.get()
                print("Getting the pattern precalculated for i=", i," and using in this status tp: ",pattern)
                p.join()
                p = multiprocessing.Process(target=self.controller, args=(q,))
                print("calling controller for next i=", i+5)
                p.start()
            print("Pattern t = ", i, " is: ", pattern) # tau = 5 min
            time.sleep(1)
            #print(i)
        
a = A()
a.simulation()
'''



'''
from pandas import read_csv
from statsmodels.tsa.arima_model import ARIMA
import numpy
import matplotlib.pyplot as plt 
# international-airline-passengers.csv
# create a differenced series
def difference(dataset, interval=1):
    diff = list()
    print(dataset)   
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return numpy.array(diff)
# invert differenced value
def inverse_difference(history, yhat, interval=1):
    return yhat + history[-interval]
# load dataset
series = read_csv('international-airline-passengers.csv', header=None)
# seasonal difference
X = series.values[1:,1]
X = [float(i) for i in X] 
#print(X)
days_in_year = 10
differenced = difference(X, days_in_year)
# fit model
model = ARIMA(differenced, order=(7,0,1))
model_fit = model.fit(disp=0)
# multi-step out-of-sample forecast
start_index = len(differenced)
end_index   = start_index + 40#6
forecast    = model_fit.predict(start=start_index, end=end_index)
print(forecast)
# invert the differenced forecast to something usable
history = [x for x in X]
day = 1
pred = []
for yhat in forecast:
    inverted = inverse_difference(history, yhat, days_in_year)
    #print('Day %d: %f' % (day, inverted))
    pred.append(inverted)
    history.append(inverted)
    day += 1
plt.plot(X)
#plt.plot( list( range( len(X),len(X)+len(inverted)) ),inverted, 'red')
plt.plot( range(len(X),len(X)+len(pred)),pred,'red')
#plt.plot( fore, 'green' )
#plt.plot( history, 'green')
plt.show()
'''
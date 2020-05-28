
# import libraries
# ARIMA example
# Import libraries
import warnings
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm


# Defaults
plt.rcParams['figure.figsize'] = (20.0, 10.0)
plt.rcParams.update({'font.size': 12})
plt.style.use('ggplot')

# Load the data
data = pd.read_csv('international-airline-passengers.csv', engine='python', skipfooter=3)
# A bit of pre-processing to make it nicer
data['Month']=pd.to_datetime(data['Month'], format='%Y-%m-%d')
data.set_index(['Month'], inplace=True)

# Plot the data
data.plot()
plt.ylabel('Monthly airline passengers (x1000)')
plt.xlabel('Date')
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
        q.put(random.randint(0,4))
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
        for i in range(0,5):
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
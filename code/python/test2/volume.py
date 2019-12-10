
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from fractions import Fraction


Horizont = 2*60*60;

tau = 15*60

num = Horizont/tau


t = np.linspace(0,2000,2000)
V = np.zeros(2000)


V[0]=500

for i in range(0,2000-1):
    V[i+1] = V[i] + tau*(-0.00001*V[i] + 0.001);

plt.plot(V)
plt.grid()
plt.show()
# Sun Diameter is 1.39*10e9 m  -> 1 390 000 km
# Earth Diameter is 1.27*10e7 m -> 12 700 km
# Angle 32
# Distance = 1.497 10e11 m
# This is just for hooby
# Reseach for Hobby

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Day[1-360]
# Location: SL,LL 
# LST: Local Time
# Latitude
# Til

N = 16  # The day of the year
B = (N-81)*360/364
ET = 9.87*np.sin(2*B) - 7.53*np.cos(B) - 1.5*np.sin(B)   # Equation Time

# Is needed to define the location point
SL = 30
LL = 33.3
DS = 0  # This value was invented
LST = 14*60

L = 35  # Latitude
Z = 10  # west
beta = 45  # tilt angle of the collector over horizontal

# If  east(right) of the standard meridian, the correction is added otherwise is subtraced.
 
AST = LST + ET - 4*(SL - LL) - DS
delta = 23.5*np.sin(360/365*(284+N))   
h = (AST-12*60)*15 #Hour angle  AST (min)  and 15(degrees)


j = np.sin(L)*np.sin(delta)*np.cos(beta) - np.cos(L)*np.sin(delta)*np.sin(beta)*np.cos(Z) + np.cos(L)*np.cos(delta)*np.cos(h)*np.cos(beta)+np.sin(L)*np.cos(delta)*np.cos(h)*np.sin(beta)*np.cos(Z)+np.cos(delta)*np.sin(h)*np.sin(beta)*np.sin(Z)

theta = np.arccos( j )

print(theta)















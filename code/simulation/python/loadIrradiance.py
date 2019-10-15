import numpy as np
import matplotlib.pyplot as plt
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

#import os
#for dirname, _, filenames in os.walk('/kaggle/input'):
#    for filename in filenames:
#        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


#data=pd.read_csv("../SolarEnergy/SolarPrediction.csv",delimiter=',',names=['UNIXTime','Data,Time','Radiation','Temperature','Pressure','Humidity','WindDirection(Degrees)','Speed','TimeSunRise','TimeSunSet'])
#data.head()
#data

#data = pd.read_csv("../SolarEnergy/SolarPrediction.csv")


tmax= 24*60*60
tau = 60*60
num = int(tmax/tau)
t   = np.arange(0, tmax, tau)

data = pd.read_csv("../SolarEnergy/meteotest_normal_year_87962.csv")

#print(data)
#print(data['Radiation'].unique())

print( data[0:num] )

irr=data['Irradiance']
Temp=data['Temperature']

irr = irr.to_numpy()
Temp = Temp.to_numpy()
irr = irr[0:num]
Temp = Temp[0:num]


#print(irr)
#print(Temp)

#print(type(irr))
#print(Temp)
#plt.plot(irr)

#plt.plot(Temp)
#plt.grid(True)
#plt.show()


#names = ['group_a', 'group_b', 'group_c']
#values = [1, 10, 100]

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

import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
import numpy as np
import json
import multiprocessing
from .utils import *
import sys

class DataProcessing:

    def __init__(self, filepath_csv="../datasets/Solargis_min15_Almeria_Spain.csv", filepath_valve="../datasets/valve.csv"):

        self.data = pd.read_csv(filepath_csv)
        self.valveData = pd.read_csv(filepath_valve)  # t1,t2,dur
        self.samplingTimeData = 900  # 15*60
        self.lifeTimeSimulation = 2*24*60*60
        self.numberSteps = 15

    def getRealPerturbations(self):
        numIntervalsTime = int(
            self.lifeTimeSimulation/self.samplingTimeData)
        t = np.linspace(0, self.lifeTimeSimulation, numIntervalsTime + 1)
        Te = self.data['Temperature'].values.tolist()[0:numIntervalsTime+1]
        I = self.data['GTI'].values.tolist()[0:numIntervalsTime+1]
        # v = self.valveData['Flow'].values.tolist()[0:numIntervalsTime+1]
        return {"t": t, "Te": Te, "I": I}
        

    def getDisturbanceSeries(self, dt=60, waterTemperatureInput=25):
        previousData = self.getRealPerturbations()
        newNumIntervalsTime = int(self.lifeTimeSimulation/dt) + 1
        t = np.linspace(0, self.lifeTimeSimulation, newNumIntervalsTime)
        Te = np.interp(t, previousData["t"], previousData["Te"])
        I = np.interp(t, previousData["t"], previousData["I"])
        # v = utils.binarizeInterpolation(
        #     np.interp(t, previousData["t"], previousData["v"]), newNumIntervalsTime)
        Ti = np.ones(newNumIntervalsTime + 1) * \
            waterTemperatureInput  # In c++ 25
        #return {"t": t, "Te": Te, "I": I, "Ti": Ti}
        return {"Te": Te, "I": I, "Ti": Ti}

        

# # num_states = 3
# # x = np.zeros(num_states)
# # x[0] = 0
# # x[1] = 1
# # x[2] = 2
# # modes  = [[1,0,0,0], [1,1,0,0], [2,0,0,0], [2,1,0,0], [3,0,0,1], [3,1,0,1], [2,0,0,1], [2,1,0,1]]  # p,r,v,f
# # #num_tau = 15
# # tau = 15*60
# # dt = 60
# # disturbances = [data["I"], data["Te"], data["Ti"]]
# # simulation(x, modes, disturbances, tau, dt)

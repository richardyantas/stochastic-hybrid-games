import numpy as np
import pandas as pd
import json
import random
import argparse
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from stochastic_hybrid_game.src.data.base_data_module import BaseDataModule

DATA_DIR = BaseDataModule.data_dirname()
WATER_TEMPERATURE_INPUT = 22.5


def plot_disturb(*args):
    time = [i for i in range(0, 3*24*60)]
    plt.plot(time, args[0], linewidth=1.8, color='r', drawstyle='steps')
    plt.plot(time, args[1], linewidth=0.8, color='b', drawstyle='steps')
    plt.plot(time, args[2], linewidth=1.8, color='g', drawstyle='steps')
    plt.grid(True, linewidth=0.6, linestyle='--')
    plt.show()


def select_interval_list(m_list, a, b):
    n_list = [0]*3*60*24
    for i in range(0, len(m_list)):
        if a <= i and i <= b:
            n_list[i] = m_list[i]
    return n_list


class signal:
    def __init__(self, _t=[], _y=[], _color="black"):
        list_t = _t
        list_y = _y
        color = _color


def predict_solar_data2(disturb, index=(13+1*24)*60, pivot=1*24*60, prediction_size=6*60):
    pred = []
    #data = SOLAR(args=None)
    #disturbs = data.loader_data()
    #Te = disturbs["Te"]
    #Te_taken = list(Te[0: index])
    # dif = []
    # for i in range(pivot, len(Te_taken)):
    #     dif.append(Te_taken[i]-Te_taken[i-pivot])
    # model = ARIMA(dif, order=(7, 1, 0))
    # model_fit = model.fit()
    # forecast = model_fit.predict(
    #     start=len(dif), end=(len(dif)+prediction_size))
    # history = list(Te_taken)
    # pred = []
    # for yhat in forecast:
    #     inverted = yhat + history[-pivot]
    #     pred.append(inverted)
    #     history.append(inverted)
    #Te = select_interval_list(Te[0:2*24*60], 0*60, 2*24*60)
    #Te_taken = select_interval_list(Te_taken, 0*60, 2*24*60)
    #history = select_interval_list(history, 0*60, len(Te_taken))
    #plot_disturb(history, Te, Te_taken)
    return pred


def predict_solar_data(data, pivot=1*24*60, prediction_size=6*60):
    dif = []  # index=(13+1*24)*60
    for i in range(pivot, len(data)):
        dif.append(data[i]-data[i-pivot])
    model = ARIMA(dif, order=(7, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.predict(
        start=len(dif), end=(len(dif)+prediction_size))
    history = list(data)
    pred = []
    for yhat in forecast:
        inverted = yhat + history[-pivot]
        pred.append(inverted)
        history.append(inverted)
    return pred


def test_predict():
    data = SOLAR(args=None)
    disturbs = data.loader_data()
    index = (24+8)*60
    Te = disturbs["Te"]
    Te_taken = list(Te[0: index])
    print("pre:", predict_solar_data(Te_taken, 24*60, 6*60))
    return


class SOLAR(BaseDataModule):
    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)
        self.data_dir = DATA_DIR
        self.data = pd.read_csv(f"{DATA_DIR}/Solargis_min15_Almeria_Spain.csv")

    def extraction_data(self):
        num_intervals = int(
            self.life_time/self.data_sample_time)
        t = np.linspace(0, self.life_time, num_intervals + 1)
        Te = self.data['Temperature'].values.tolist()[0:num_intervals+1]
        I = self.data['GTI'].values.tolist()[0:num_intervals+1]
        return {"t": t, "Te": Te, "I": I}

    def transform_data(self, *args, **kwargs) -> None:
        previous_data = self.extraction_data()
        new_num_intervals = int(self.life_time/self.dt) + 1  # each minute
        t = np.linspace(0, self.life_time, new_num_intervals)
        Te = np.interp(t, previous_data["t"], previous_data["Te"])
        I = np.interp(t, previous_data["t"], previous_data["I"])
        Ti = np.ones(new_num_intervals + 1) * WATER_TEMPERATURE_INPUT
        return {"Te": Te, "I": I, "Ti": Ti, "t": t}

    def loader_data(self):
        data = self.transform_data()
        return data


if __name__ == "__main__":
    test_predict()
    # predict_solar_data()

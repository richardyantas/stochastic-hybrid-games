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


<<<<<<< HEAD
def plot_disturb(*args):
    time = [i for i in range(0, 3*24*60)]
<<<<<<< HEAD
    plt.plot(time, args[0], linewidth=1.8, color='r', drawstyle='steps')
    plt.plot(time, args[1], linewidth=0.8, color='b', drawstyle='steps')
    plt.plot(time, args[2], linewidth=1.8, color='g', drawstyle='steps')
    plt.grid(True, linewidth=0.6, linestyle='--')
    plt.show()


def select_interval_list(m_list, a, b):
    n_list = [0]*3*60*24
=======
    with plt.style.context('dark_background'):
        plt.plot(time, args[0], linewidth=1.8, color='r', drawstyle='steps')
        plt.plot(time, args[1], linewidth=0.8, color='b', drawstyle='steps')
        plt.plot(time, args[2], linewidth=1.8, color='y', drawstyle='steps')
=======
def plot_solaris_data():
    # data = SOLAR(args=None)
    parser = argparse.ArgumentParser(add_help=False)
    # parser.add_argument("--data_class", type=str, default="SOLAR")
    parser.add_argument("--life_time", type=int, default=10*24*60)
    args = parser.parse_args()
    data = SOLAR(args)

    disturbs = data.loader_data()
    season_max = 10*24*60
    Te = disturbs["Te"][0:season_max]
    I = disturbs["I"][0:season_max]
    Ti = disturbs["Ti"][0:season_max]
    season = [float((i)/(24*60)) for i in range(0, season_max)]
    with plt.style.context('bmh'):
        fig, ax1 = plt.subplots(figsize=(10, 2))  # 15,4
        #plt.figure(figsize=(7, 3))
        ax2 = ax1.twinx()
        ax1.plot(season, Te, linewidth=0.8,
                 color='r', drawstyle='steps', label="Te")
        # ax1.plot(season, Ti, linewidth=0.8,
        #          color='b', drawstyle='steps', label="Ti")
        ax2.plot(season, I, linewidth=1.2,
                 color='purple', drawstyle='steps', label="I")
        ax1.set_xlabel('t[days]')
        ax1.set_ylabel('T[C]', color='r')
        ax2.set_ylabel('Irradiance[kW/m2]', color='purple')
        plt.legend()
>>>>>>> master
        plt.grid(True, linewidth=0.6, linestyle='--')
        plt.savefig(
            './doc/ucsp-mcs-thesis-english-2018/images/solaris2.png')
        plt.show()

<<<<<<< HEAD

def select_interval_list(m_list, a, b):
    n_list = [0]*2*60*24
>>>>>>> master
    for i in range(0, len(m_list)):
        if a <= i and i <= b:
            n_list[i] = m_list[i]
    return n_list
=======
    return
>>>>>>> master


<<<<<<< HEAD
class signal:
    def __init__(self, _t=[], _y=[], _color="black"):
        list_t = _t
        list_y = _y
        color = _color


def predict_solar_data():
    data = SOLAR(args=None)
    disturbs = data.loader_data()
    Te = disturbs["Te"]
    Te_taken = list(Te[0: (13+2*24)*60])
    pivot = 2*24*60
=======
def predict_solar_data2(index=(13+1*24)*60, pivot=1*24*60, prediction_size=6*60):
    pred = []
    data = SOLAR(args=None)
    disturbs = data.loader_data()
    Te = disturbs["Te"]
<<<<<<< HEAD
    Te_taken = list(Te[0: index])
>>>>>>> master
=======
    Te_integral = list(Te[0: index])
>>>>>>> master
    dif = []
    for i in range(pivot, len(Te_integral)):
        dif.append(Te_integral[i]-Te_integral[i-pivot])
    model = ARIMA(dif, order=(7, 1, 0))
    model_fit = model.fit()
<<<<<<< HEAD
    prediction_size = 6*60
=======
>>>>>>> master
    forecast = model_fit.predict(
        start=len(dif), end=(len(dif)+prediction_size))
    history = list(Te_integral)
    pred = []
    for yhat in forecast:
        inverted = yhat + history[-pivot]
        pred.append(inverted)
        history.append(inverted)
<<<<<<< HEAD
<<<<<<< HEAD
    Te = select_interval_list(Te[0:3*24*60], 0*60, 3*24*60)
    Te_taken = select_interval_list(Te_taken, 0*60, 3*24*60)
    history = select_interval_list(history, 0*60, len(Te_taken))
    plot_disturb(history, Te, Te_taken)
=======

    # Te = select_interval_list(Te[0:2*24*60], 0*60, 2*24*60)
    # Te_taken = select_interval_list(Te_taken, 0*60, 2*24*60)
    # history = select_interval_list(history, 0*60, len(Te_taken))
    # plot_disturb(history, Te, Te_taken)

    time = [i for i in range(0, 2*24*60)]
    with plt.style.context('dark_background'):
        plt.plot(history, linewidth=1.8, color='r', drawstyle='steps')
        plt.plot(Te, linewidth=0.8, color='w', drawstyle='steps')
        plt.plot(Te_taken, linewidth=1.8, color='y', drawstyle='steps')
=======
    # plot
    time_Te = [float((i)/60) for i in range(0, 2*24*60)]
    time_Te_integral = [float((i)/60) for i in range(0, len(Te_integral))]
    time_history = [float((i)/60) for i in range(0, len(history))]
    # with plt.style.context('dark_background'):
    with plt.style.context('bmh'):
        plt.plot(time_history, history, linewidth=1.8,
                 color='r', drawstyle='steps')
        plt.plot(time_Te, Te[0:-1], linewidth=0.8,
                 color='black', drawstyle='steps')
        plt.plot(time_Te_integral, Te_integral, linewidth=1.8,
                 color='cyan', drawstyle='steps')
        plt.ylabel('T[C]')
        plt.xlabel('t[hrs]')
        plt.legend()
>>>>>>> master
        plt.grid(True, linewidth=0.6, linestyle='--')
        plt.show()

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
>>>>>>> master
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
        Ti = np.ones(new_num_intervals + 1) * \
            WATER_TEMPERATURE_INPUT  # add noise here
        return {"Te": Te, "I": I, "Ti": Ti, "t": t}

    def loader_data(self):
        data = self.transform_data()
        return data


if __name__ == "__main__":
<<<<<<< HEAD
    # load_and_print_info(SOLAR)
    predict_solar_data()
=======
    # test_predict()
<<<<<<< HEAD
    predict_solar_data2()
>>>>>>> master
=======
    plot_solaris_data()
    # predict_solar_data2()
>>>>>>> master

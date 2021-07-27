from stochastic_hybrid_game.src.data.SOLAR import predict_solar_data
from typing import Any, Dict
import time
import os
import json
import jsbeautifier
import numpy as np
import argparse
import multiprocessing
from interval import interval
from stochastic_hybrid_game.src.data.base_data_module import BaseDataModule
from stochastic_hybrid_game.src.data.SOLAR import SOLAR
from stochastic_hybrid_game.src.models.SWH import SWH
from stochastic_hybrid_game.src.models.SWH import C_MODES
import matplotlib.pyplot as plt
# from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima.model import ARIMA
# import statsmodels as sm
# https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html
# import statsmodels.tsa.arima_model
# import statsmodels

# export PYTHONPATH=.
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./build/lib/   # desde el main - parece que no es necesario
# COMMAND = "python sthocastic_hybrid_game/tests/main.py lib/uppaal/bin-Linux/verifyta sthocastic_hybrid_game/tests/foo.xml sthocastic_hybrid_game/tests/foo.q"
# data = os.popen("lib/uppaal/bin-Linux/verifyta sthocastic_hybrid_game/tests/foo.xml sthocastic_hybrid_game/tests/foo.q").readlines()

COMMAND = "lib/uppaal/bin-Linux/verifyta sources/uppaal/swh.xml sources/uppaal/swh.q"
DATA_DIR = BaseDataModule.data_dirname()

SAFE_RES = json.load(open(f"{DATA_DIR}/pattern.json"))
PATTERNS = SAFE_RES["patterns"]
ZONOTOPES = SAFE_RES["zonotopes"]

SAFE_DATA = json.load(open(f"{DATA_DIR}/static_data.json"))
R = SAFE_DATA["R"]
S = SAFE_DATA["S"]
TAU = SAFE_DATA["tau"]  # 300 should be fixed by safe patterns


def query_safe_patterns(state):
    for i in range(0, len(ZONOTOPES)):
        z0_temperature = interval[ZONOTOPES[i][0],
                                  ZONOTOPES[i][1]]  # z0 = T interval
        z1_volume = interval[ZONOTOPES[i][2],
                             ZONOTOPES[i][3]]  # z1 = V interval
        if (state[1] in z1_volume and state[2] in z0_temperature):
            return PATTERNS[i]
    print("Not found patterns for this state: ", state)
    return [[-1, -1, -1]]


def plot_safe_behaviour():
    data = SOLAR(args=None)
    start_time = data.config()["start_time"]
    print(start_time)
    model = SWH(data_config=data.config(), disturbs=data.loader_data())
    safe_res = json.load(open(f"{DATA_DIR}/pattern.json"))
    static_data = json.load(open(f"{DATA_DIR}/static_data.json"))
    tau = static_data["tau"]
    state = [0.0, 0.13, 50.0]
    states = [list(state)]
    index = start_time
    set_pattern = []
    for i in range(0, 3):
        patterns = query_safe_patterns(state)
        pattern = patterns[int(len(patterns)/2)]
        plt.plot(state[1], state[2], "ro")
        for mode in pattern:
            for i in range(index, index+tau):
                state = model.post(mode, 0, state, i)
                states.append(list(state))
            index = index + tau
        print(pattern)
        print(state)
        set_pattern.append(list(pattern))
    colors = ["olive", "deepskyblue", "goldenrod", "cyan"]
    ind = 0
    for pat in set_pattern:
        print(pat)
        l = len(pat)*tau
        V = [float(states[i][1])
             for i in range(ind, ind + l+1)]  # para que cierre los puntos
        T = [float(states[i][2]) for i in range(ind, ind + l+1)]
        ind += l
        plt.plot(V, T, linewidth=1.0, color=colors.pop(0))
    # plt.axis([0.0, 0.4, 20.0, 90.0])
    plt.plot([R[1][0], R[1][0], R[1][1], R[1][1], R[1][0]], [
             R[0][0], R[0][1], R[0][1], R[0][0], R[0][0]], "gray", linewidth=1.2, linestyle='--', label="R")
    plt.plot([S[1][0], S[1][0], S[1][1], S[1][1], S[1][0]], [
             S[0][0], S[0][1], S[0][1], S[0][0], S[0][0]], "teal", linewidth=0.9, linestyle='--', label="S")
    plt.xlabel("Volume")
    plt.ylabel("Temperature")
    plt.grid(True, linewidth=0.6, linestyle='--')
    plt.savefig(
        './doc/ucsp-mcs-thesis-english-2018/images/safe_post_pattern.png')
    plt.show()

    # plot states with R, S

    return


class SOMPC_UPPAAL():
    def __init__(self, model: Any, data_config: Dict[str, Any], disturbs: Dict[str, Any], args: argparse.Namespace = None):
        # self.tau = self.args.get("tau", TAU)
        self.start_time = data_config["start_time"]
        self.disturbs = disturbs
        self.Te = disturbs["Te"]
        self.Ti = disturbs["Ti"]
        self.I = disturbs["I"]
        self.t = disturbs["t"]
        self.tau = TAU
        self.model = model
        self.u_actions = self.model.get_uncontrollable_actions()  # or load?
        self.initial_state = self.model.get_initial_state()
        self.nrSteps = self.model.get_number_steps()
        self.pat = list(query_safe_patterns(list(self.initial_state))[0])
        # self.controllable_mode = -1
        self.c_actions = []  # [C_MODES[self.controllable_mode]]
        self.queue = multiprocessing.Queue()
        self.prediction_size = 1*60  # prediction_size
        self.H = self.nrSteps*self.tau+self.tau
        self.list_params = []

    def send_save_data2uppaal(self, controllable_mode, state, index):
        pivot = 24*60
        Te = predict_solar_data(
            self.disturbs["Te"][0:index], pivot, self.prediction_size)
        Ti = predict_solar_data(
            self.disturbs["Ti"][0:index], pivot, self.prediction_size)
        I = predict_solar_data(
            self.disturbs["I"][0:index], pivot, self.prediction_size)

        # print("predicted: ", Te)
        # print("real: ", self.disturbs["Te"]
        #       [index:index+self.prediction_size])
        dynamic_data = {}
        dynamic_data["E"] = state[0]
        dynamic_data["V"] = state[1]
        dynamic_data["T"] = state[2]
        dynamic_data["mode"] = controllable_mode
        dynamic_data["valve"] = 0  # int(self.u_actions[index])  # OJO
        dynamic_data["t"] = index
        # list(self.Te[index:index+self.H])
        dynamic_data["Te"] = Te  # list(self.Te[index:index+self.H])
        dynamic_data["Ti"] = Ti  # list(self.Ti[index:index+self.H])
        dynamic_data["I"] = I  # list(self.I[index:index+self.H])
        file = open(f"{DATA_DIR}/dynamic_data.json", 'w', encoding='utf-8')
        file.write(json.dumps(dynamic_data, indent=4, sort_keys=True))
        return

    def pre_convert2array(self, points):
        for i in range(0, len(points)):
            points[i] = points[i][1:-1].split(",")
            points[i][0] = float(points[i][0])
            points[i][1] = float(points[i][1])
        return points

    def convert2array(self, points):  # HERE PROBLEM !!
        horizon_permitted = int(points[-1][0]/TAU)
        mlist = [None]*horizon_permitted
        for i in range(0, len(points)-1):
            if (points[i][0] == points[i+1][0] and points[i+1][0] != points[-1][0]):
                it = int(points[i][0]/self.tau)
                mlist[it] = points[i+1][1]  # int
        if mlist[0] == None:
            mlist[0] = 0
        for i in range(0, horizon_permitted-1):
            if mlist[i+1] == None:
                mlist[i+1] = mlist[i]
        return mlist

    def filter_pattern(self, mode, visitedPatterns):
        less = min(len(visitedPatterns), len(mode))
        patterns = []
        subgroup = [mode[0]]
        for i in range(0, less-1):
            if visitedPatterns[i] == visitedPatterns[i+1]:
                subgroup.append(mode[i+1])
            else:
                patterns.append(subgroup)
                subgroup = []
                subgroup.append(mode[i+1])
        patterns = patterns[0:-1]
        # new_patterns = []
        # for ps in patterns:
        #     for p in ps:
        #         new_patterns.append(p)
        # return new_patterns
        return patterns[0]

    def receive_strategy_from_uppaal(self):
        res = os.popen(COMMAND).readlines()
        params = {}
        params["visitedPatterns"] = 0
        params["mode"] = 0
        params["Tnext"] = 0
        for i in range(0, len(res)-1):
            key = res[i][:-2]
            if params.get(key) != None:
                points = res[i+1][:-1].split()[1:]
                points = self.pre_convert2array(points)
                params[key] = {"list": self.convert2array(
                    points), "points": points}
        # file = open(f"{DATA_DIR}/uppaal_response_data2.json",
        #             'a', encoding='utf-8')
        # file.write(json.dumps(params, indent=4, sort_keys=True)+",")
        # ---------------------#
        params["mode"] = [int(p) for p in params["mode"]["list"]]
        pattern = self.filter_pattern(
            params["mode"], params["visitedPatterns"]["list"])
        print("pattern: ", pattern, "size: ", len(pattern))
        return pattern

    def predict(self, controllable_mode, state, index):
        print("index: ", index)
        print("time(hr): ", index/60)
        print("mode to predict: ", controllable_mode)
        print("T: ", state[2])
        predicted_state = list(state)
        for i in range(index, index + self.tau):
            predicted_state = self.model.post(
                controllable_mode, self.u_actions[index], predicted_state, i)
        print("bbug", controllable_mode, state, index)
        print("T predicted on step: ", predicted_state[2])
        self.send_save_data2uppaal(controllable_mode, list(state), index)
        optimal_pattern = self.receive_strategy_from_uppaal()
        self.queue.put(optimal_pattern)
        return

    def control(self, state, index):
        if(len(self.pat) == 0):
            self.pat = self.queue.get()
            self.controllable_mode = self.pat.pop(0)
        elif(len(self.pat) == 1):
            self.controllable_mode = self.pat.pop(0)
            process = multiprocessing.Process(target=self.predict, args=(
                int(self.controllable_mode), state, index))
            process.start()
        elif(len(self.pat) > 1):
            self.controllable_mode = self.pat.pop(0)
        print("W")
        self.c_actions.append(C_MODES[self.controllable_mode])
        return self.controllable_mode

    def get_nrSteps(self):
        return self.nrSteps

    def get_tau(self):              # remove ?
        return self.tau

    def get_pat(self):               # remove ??
        return self.pat

    def get_controllable_actions(self):
        return self.c_actions

    @ staticmethod
    def add_to_argparse(parser):
        parser.add_argument("--tau", type=int, default=TAU)
        return parser


if __name__ == '__main__':
    plot_safe_behaviour()

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
from stochastic_hybrid_game.src.models.SWH import C_MODES
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

COMMAND = "lib/uppaal/bin-Linux/verifyta sources/uppaal/optimal.xml sources/uppaal/optimal.q"
DATA_DIR = BaseDataModule.data_dirname()
SAFE_DATA = json.load(open(f"{DATA_DIR}/static_data.json"))
TAU = SAFE_DATA["tau"]  # 300 should be fixed by safe patterns


class OMPC_UPPAAL():
    def __init__(self, model: Any, data_config: Dict[str, Any], disturbs: Dict[str, Any], args: argparse.Namespace = None):
        self.start_time = data_config["start_time"]
        self.disturbs = disturbs
        self.Te = disturbs["Te"]
        self.Ti = disturbs["Ti"]
        self.I = disturbs["I"]
        self.t = disturbs["t"]
        self.tau = TAU
        self.model = model
        self.u_actions = self.model.get_uncontrollable_actions()
        self.initial_state = self.model.get_initial_state()
        self.nrSteps = self.model.get_number_steps()
        # todavia no entiendo por que el problema siempre estuvo aqui !
        self.pat = [0, 2]
        #self.pat = list(query_safe_patterns(list(self.initial_state))[0])
        #self.controllable_mode = -1
        self.c_actions = []  # [C_MODES[self.controllable_mode]]
        self.queue = multiprocessing.Queue()
        self.prediction_size = 1*60  # prediction_size
        self.H = self.nrSteps*self.tau+self.tau
        self.list_params = []

    def send_save_data2uppaal(self, controllable_mode, state, index):
        pivot = 24*60
        Te = predict_solar_data(
            self.disturbs["Te"][0:index], pivot, self.prediction_size)  # [0:index ] good!
        Ti = predict_solar_data(
            self.disturbs["Ti"][0:index], pivot, self.prediction_size)
        I = predict_solar_data(
            self.disturbs["I"][0:index], pivot, self.prediction_size)
        dynamic_data = {}
        dynamic_data["E"] = state[0]
        dynamic_data["V"] = state[1]
        dynamic_data["T"] = state[2]
        dynamic_data["mode"] = controllable_mode
        dynamic_data["valve"] = 0  # int(self.u_actions[index])  # OJO
        dynamic_data["t"] = index
        dynamic_data["Te"] = Te
        dynamic_data["Ti"] = Ti
        dynamic_data["I"] = I
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

    def receive_strategy_from_uppaal(self):
        res = os.popen(COMMAND).readlines()
        params = {}
        params["mode"] = 0
        for i in range(0, len(res)-1):
            key = res[i][:-2]
            if params.get(key) != None:
                points = res[i+1][:-1].split()[1:]
                points = self.pre_convert2array(points)
                params[key] = {"list": self.convert2array(
                    points), "points": points}
        file = open(f"{DATA_DIR}/uppaal_response_data2.json",
                    'w', encoding='utf-8')
        file.write(json.dumps(params, indent=4, sort_keys=True)+",")
        # ---------------------
        params["mode"] = [int(p) for p in params["mode"]["list"]]
        print("bug: ", params["mode"])
        return params["mode"][0:3]

    def predict(self, controllable_mode, state, index):
        print("index: ", index)
        print("time(hr): ", index/60)
        print("mode to predict: ", controllable_mode)
        print("T: ", state[2])
        predicted_state = list(state)
        for i in range(index, index + self.tau):
            predicted_state = self.model.post(
                controllable_mode, self.u_actions[index], predicted_state, i)
        print("T predicted on step: ", predicted_state[2])
        print("bbug", controllable_mode, state, index)
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

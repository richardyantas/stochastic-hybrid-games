from typing import Any, Dict
import time
import os
import json
import jsbeautifier
import numpy as np
import argparse
import multiprocessing
from interval import interval
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from stochastic_hybrid_game.src.data.base_data_module import BaseDataModule
from stochastic_hybrid_game.src.data.SOLAR import SOLAR
from stochastic_hybrid_game.src.models.SWH import SWH
from stochastic_hybrid_game.src.models.SWH import C_MODES

DATA_DIR = BaseDataModule.data_dirname()
# SAFE_RES = json.load(open(f"{DATA_DIR}/pattern_perturbations_12.json"))
SAFE_RES = json.load(open(f"{DATA_DIR}/pattern.json"))
PATTERNS = SAFE_RES["patterns"]
ZONOTOPES = SAFE_RES["zonotopes"]
SAFE_DATA = json.load(open(f"{DATA_DIR}/static_data.json"))
R = SAFE_DATA["R"]
S = SAFE_DATA["S"]
TAU = SAFE_DATA["tau"]  # 300 should be fixed by safe patterns


class MPC():
    """_summary_
    """

    def __init__(self, model: Any, data_config: Dict[str, Any], disturbs: Dict[str, Any], args: argparse.Namespace = None):
        self.start_time = data_config["start_time"]
        self.disturbs = disturbs
        self.Te = disturbs["Te"]
        self.Ti = disturbs["Ti"]
        self.I = disturbs["I"]
        self.t = disturbs["t"]
        self.tau = TAU
        self.data_dir = DATA_DIR
        self.model = model
        self.u_actions = self.model.get_uncontrollable_actions()  # or load?
        self.initial_state = self.model.get_initial_state()
        self.nrSteps = self.model.get_number_steps()
        self.pat = list(self.query_safe_patterns(list(self.initial_state))[0])
        self.c_actions = []
        self.queue = multiprocessing.Queue()
        self.prediction_size = 1*60
        self.H = self.nrSteps*self.tau+self.tau
        self.list_params = []

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
        optimal_pattern = self.get_pattern(controllable_mode, state, index)
        self.queue.put(optimal_pattern)
        return

    def control(self, state, index):
        if (len(self.pat) == 0):
            self.pat = self.queue.get()
            self.controllable_mode = self.pat.pop(0)
        elif (len(self.pat) == 1):
            self.controllable_mode = self.pat.pop(0)
            process = multiprocessing.Process(target=self.predict, args=(
                int(self.controllable_mode), state, index))
            process.start()
        elif (len(self.pat) > 1):
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

    def query_safe_patterns(self, state):
        for i in range(0, len(ZONOTOPES)):
            z0_temperature = interval[ZONOTOPES[i][0],
                                      ZONOTOPES[i][1]]  # z0 = T interval
            z1_volume = interval[ZONOTOPES[i][2],
                                 ZONOTOPES[i][3]]  # z1 = V interval
            if (state[1] in z1_volume and state[2] in z0_temperature):
                return PATTERNS[i]
        print("Not found patterns for this state: ", state)
        return [[-1, -1, -1]]

    @ staticmethod
    def add_to_argparse(parser):
        parser.add_argument("--tau", type=int, default=TAU)
        return parser


# if __name__ == '__main__':

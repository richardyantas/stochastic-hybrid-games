from typing import Any, Dict
import json
import numpy as np
import argparse
import random
import time
import multiprocessing
from interval import interval
from stochastic_hybrid_game.src.data.base_data_module import BaseDataModule
from stochastic_hybrid_game.src.models.SWH import C_MODES

"""  
    Title: MPC predictive model controller
    Author: Richard Yantas A.
    References: https://locuslab.github.io/mpc.pytorch/
"""


DATA_DIR = BaseDataModule.data_dirname()
SAFE_RES = json.load(open(f"{DATA_DIR}/pattern.json"))
PATTERNS = SAFE_RES["patterns"]
ZONOTOPES = SAFE_RES["zonotopes"]
SAFE_DATA = json.load(open(f"{DATA_DIR}/static_data.json"))
TAU = SAFE_DATA["tau"]
TG = SAFE_DATA["Tg"]
ALPHA = SAFE_DATA["alpha"]


def query_safe_patterns(state):
    for i in range(0, len(ZONOTOPES)):
        z0_temperature = interval[ZONOTOPES[i][0],
                                  ZONOTOPES[i][1]]  # z0 = T interval
        z1_volume = interval[ZONOTOPES[i][2],
                             ZONOTOPES[i][3]]  # z1 = V interval
        if (state[1] in z1_volume and state[2] in z0_temperature):
            return PATTERNS[i]
    print("Not found patterns for this state: ", state)
    if state[2] < ZONOTOPES[0][0]:
        return PATTERNS[0]
    else:
        return PATTERNS[-1]
    # return [[-1, -1, -1]]


class OMPC_LOCAL():
    def __init__(self, model: Any, data_config: Dict[str, Any], disturbs: Dict[str, Any], args: argparse.Namespace = None):
        self.Te = disturbs["Te"]
        self.Ti = disturbs["Ti"]
        self.I = disturbs["I"]
        self.t = disturbs["t"]
        self.tau = TAU
        self.model = model
        self.u_actions = self.model.get_uncontrollable_actions()
        self.initial_state = self.model.get_initial_state()
        self.nrSteps = self.model.get_number_steps()
        #self.pat = list(query_safe_patterns(list(self.initial_state))[0])
        # self.controllable_mode = -1
        self.c_actions = []  # [C_MODES[self.controllable_mode]]
        self.queue = multiprocessing.Queue()
        self.H = self.nrSteps*self.tau

    def optimal_pattern_search(self, state, index, candidate_patterns):
        alpha = ALPHA
        Tg = TG
        Horizon = 9
        next_state = list(state)
        optimal_pattern = []
        min_costFunction = 100000.0
        for candidate_pattern in candidate_patterns:
            m_index = index
            temporal_state = list(next_state)
            for mode in candidate_pattern:
                for i in range(m_index, m_index+self.tau):
                    temporal_state = self.model.post(
                        mode, self.u_actions[i], temporal_state, i)
                m_index = m_index + self.tau
            costFunction = alpha * \
                temporal_state[0]+(1-alpha)*abs(Tg-temporal_state[2])
            if(costFunction < min_costFunction):
                min_costFunction = float(costFunction)
                optimal_pattern = list(candidate_pattern)
        print("optimal pattern: ", optimal_pattern)
        return optimal_pattern

#  ############################# CAMBIAR TAU sec -> min ###################

    def predict(self, controllable_mode, state, index):
        print("index: ", index)
        print("time(hr): ", index/60)
        print("mode to predict: ", controllable_mode)
        print("T: ", state[2])
        predicted_state = state
        for i in range(index, index + self.tau):
            predicted_state = self.model.post(
                controllable_mode, self.u_actions[i], predicted_state, i)  # antes era index creo que en u_actions[i] deberia de ser i ne vez de index
        patterns = query_safe_patterns(predicted_state)
        # optimal_pattern = self.optimal_pattern_search(patterns)
        # time.sleep(10)
        optimal_meta_pattern = self.optimal_pattern_search(
            predicted_state, index+self.tau, patterns)
        self.queue.put(optimal_meta_pattern)
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

    def get_tau(self):
        return self.tau

    def get_pat(self):
        return self.pat

    def get_controllable_actions(self):
        return self.c_actions

    @ staticmethod
    def add_to_argparse(parser):
        parser.add_argument("--tau", type=int, default=TAU)
        return parser

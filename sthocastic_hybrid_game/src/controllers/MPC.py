from typing import Any, Dict
import json
import numpy as np
import argparse
import random
import multiprocessing
from interval import interval
from sthocastic_hybrid_game.src.data.base_data_module import BaseDataModule
from sthocastic_hybrid_game.src.models.SWH import C_MODES
"""MPC predictive model controller"""

DATA_DIR = BaseDataModule.data_dirname()
SAFE_RES = json.load(open(f"{DATA_DIR}/pattern.json"))
PATTERNS = SAFE_RES["patterns"]
ZONOTOPES = SAFE_RES["zonotopes"]
# TAU = SAFE_RES["tau"]  # 300 should be fixed by safe patterns
SAFE_DATA = json.load(open(f"{DATA_DIR}/static_data.json"))
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


class MPC():
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
        self.pat = list(query_safe_patterns(list(self.initial_state))[0])
        #self.controllable_mode = -1
        self.c_actions = []  # [C_MODES[self.controllable_mode]]
        self.queue = multiprocessing.Queue()
        self.H = self.nrSteps*self.tau

    def optimal_pattern_search(self, patterns):
        # ANN controller
        #print("pattern choosen: ", patterns[1])
        pattern_size = len(patterns)
        pos = random.randrange(0, pattern_size)
        return patterns[0]  # for the moment

#  ############################# CAMBIAR TAU sec -> min ###################

    def predict(self, controllable_mode, state, index):
        predicted_state = state
        for i in range(index, index + self.tau):
            predicted_state = self.model.post(
                controllable_mode, self.u_actions[index], predicted_state, i)  # antes era index
        patterns = query_safe_patterns(predicted_state)
        optimal_pattern = self.optimal_pattern_search(patterns)
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

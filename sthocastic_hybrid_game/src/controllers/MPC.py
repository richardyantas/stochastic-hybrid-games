from typing import Any, Dict
import json
import numpy as np
import argparse
import multiprocessing
from interval import interval
from sthocastic_hybrid_game.src.data.base_data_module import BaseDataModule
from sthocastic_hybrid_game.src.models.SWH import C_MODES
"""MPC predictive model controller"""

DATA_DIR = BaseDataModule.data_dirname()
SAFE_RES = json.load(open(f"{DATA_DIR}/pattern.json"))
PATTERNS = SAFE_RES["patterns"]
ZONOTOPES = SAFE_RES["zonotopes"]
TAU = SAFE_RES["tau"]  # 300 should be fixed by safe patterns


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
        #self.tau = self.args.get("tau", TAU)
        self.tau = TAU
        self.model = model
        self.state = self.model.get_initial_state()
        self.pat = list(self.optimal_pattern_search(
            query_safe_patterns(self.state)))
        self.modes = self.model.get_controllable_modes()
        self.u_actions = self.model.get_uncontrollable_actions()
        self.queue = multiprocessing.Queue()
        self.process = multiprocessing.Process(
            target=self.predict, args=(self.pat.pop(0), self.state, 0))
        # states to plot
        self.c_actions = [self.modes[self.pat[-1]]]
        #self.u_actions = []
        self.states = [self.state]

    def optimal_pattern_search(self, patterns):
        # ANN controller
        #print("pattern choosen: ", patterns[1])
        return patterns[1]  # for the moment

#  ############################# CAMBIAR TAU sec -> min ###################

    def predict(self, mode, state, index):
        predicted_state = state
        taumin = int(self.tau/60)
        for i in range(index, index + taumin):
            predicted_state = self.model.post(mode, predicted_state, index)
        patterns = query_safe_patterns(predicted_state)
        optimal_pattern = self.optimal_pattern_search(patterns)
        self.queue.put(optimal_pattern)
        return

    def control(self, index):
        if(len(self.pat) == 0):
            self.pat = self.queue.get()
            controllable_mode = self.pat.pop(0)
        elif(len(self.pat) == 1):
            controllable_mode = self.pat.pop(0)
            process = multiprocessing.Process(target=self.predict, args=(
                controllable_mode, self.state, index))
            process.start()
        elif(len(self.pat) > 1):
            controllable_mode = self.pat.pop(0)

        self.state = self.model.update(controllable_mode, self.state, index)
        self.c_actions.append(list(self.modes[controllable_mode]))
        self.states.append(list(self.state))
        return self.pat

    def get_tau(self):
        return self.tau

    def get_pat(self):
        return self.pat

    def get_states(self):
        return self.states

    def get_controllable_actions(self):
        return self.c_actions

    def get_uncontrollable_actions(self):
        return self.u_actions

    @ staticmethod
    def add_to_argparse(parser):
        parser.add_argument("--tau", type=int, default=TAU)
        return parser

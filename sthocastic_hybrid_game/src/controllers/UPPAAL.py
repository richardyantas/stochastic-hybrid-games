from typing import Any, Dict
import time
import os
import json
import numpy as np
import argparse
import multiprocessing
from interval import interval
from sthocastic_hybrid_game.src.data.base_data_module import BaseDataModule
from sthocastic_hybrid_game.src.models.SWH import C_MODES
"""MPC predictive model controller"""

# export PYTHONPATH=.
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./build/lib/   # desde el main
#COMMAND = "python sthocastic_hybrid_game/tests/main.py lib/uppaal/bin-Linux/verifyta sthocastic_hybrid_game/tests/foo.xml sthocastic_hybrid_game/tests/foo.q"

DATA_DIR = BaseDataModule.data_dirname()
SAFE_RES = json.load(open(f"{DATA_DIR}/pattern.json"))
#STATIC_DATA = json.load(open(f"{DATA_DIR}/static_data.json"))
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


class UPPAAL():
    def __init__(self, model: Any, data_config: Dict[str, Any], args: argparse.Namespace = None):
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
        self.index = 0
        self.states = [self.state]

    def optimal_pattern_search(self, patterns):
        return patterns[1]

    def save_data2uppaal(self, patterns):
        dynamic_data = {}
        dynamic_data["T"] = self.state[2]
        dynamic_data["V"] = self.state[1]
        dynamic_data["E"] = self.state[0]
        dynamic_data["modeans"] = self.modes[0]  # self.controllable_mode
        dynamic_data["valve"] = self.u_actions[self.index]
        dynamic_data["t"] = self.index
        dynamic_data["pattern"] = self.pat
        # disturbance
        json.dump(dynamic_data, open(f"{DATA_DIR}/dynamic_data.json", 'w'))
        return

    def co2array(self, points):  # it only affect2list
        signal = []
        coord = {}
        for i in range(0, len(points)):
            point = points[i][1:-1].split(',')
            coord[point[0]] = point[1]
        # for i in range(0, len(points)-1):
        #    if coord4[0]
        return signal

    def parse2array(self, res):  # parse2dict
        params = {}
        params["value"] = 0
        params["X"] = 0
        params["NUM_PATTERNS"] = 0
        for i in range(0, len(res)):
            if params.get(res[i][:-2]) != None:  # removing :\n with -3
                params[res[i][:-2]] = self.co2array(res[i+1][:-1].split()[1:])
        time.sleep(1)
        # for key in params:
        #    params[key] = params[key].split()
        # mvalve = self.readUppaalValues(mvalve)
        # ppos = self.readUppaalValues(ppos)
        # mode = self.readUppaalValues(mode)
        # flag = self.readUppaalValues(flag)
        # visitedPatterns = self.readUppaalValues(visitedPatterns)
        #pattern = [0]
        # res[10] : title
        # res[11] : data
        return params

    # **************** Taks **************
    # modified libconfig to pass
    # patterns

    def predict(self, mode, state, index):
        predicted_state = state
        taumin = int(self.tau/60)
        for i in range(index, index + taumin):
            predicted_state = self.model.post(mode, predicted_state, index)
        patterns = query_safe_patterns(predicted_state)
        # save pattern and disturbances to json
        self.save_data2uppaal(patterns)
        # call uppaal executing a command
        # data = os.popen("lib/uppaal/bin-Linux/verifyta sources/uppaal/random.xml sources/uppaal/foo.q").readlines()
        data = os.popen(
            "lib/uppaal/bin-Linux/verifyta sthocastic_hybrid_game/tests/foo.xml sthocastic_hybrid_game/tests/foo.q").readlines()
        print(self.parse2array(data))
        optimal_pattern = self.optimal_pattern_search(patterns)
        # read terminal response or even better a json from upppaal
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
        self.index = index
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

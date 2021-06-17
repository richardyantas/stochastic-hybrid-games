from typing import Any, Dict
import time
import os
import json
import jsbeautifier
import numpy as np
import argparse
import multiprocessing
from interval import interval
from sthocastic_hybrid_game.src.data.base_data_module import BaseDataModule
from sthocastic_hybrid_game.src.models.SWH import C_MODES
import matplotlib.pyplot as plt
"""MPC predictive model controller"""

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


class UPPAAL():
    def __init__(self, model: Any, data_config: Dict[str, Any], disturbs: Dict[str, Any], args: argparse.Namespace = None):
        # self.tau = self.args.get("tau", TAU)
        self.Te = disturbs["Te"]
        self.Ti = disturbs["Ti"]
        self.I = disturbs["I"]
        self.t = disturbs["t"]
        self.tau = TAU
        self.model = model
        self.initial_state = self.model.get_initial_state()
        self.u_actions = self.model.get_uncontrollable_actions()
        self.nrSteps = self.model.get_number_steps()

        self.pat = list(query_safe_patterns(list(self.initial_state))[0])
        self.controllable_mode = -1
        self.c_actions = []  # [C_MODES[self.controllable_mode]]
        self.queue = multiprocessing.Queue()
        self.H = self.nrSteps*self.tau

    # this method would be better on model SWH python instead or generalize!!!!

    def send_save_data2uppaal(self, controllable_mode, state, index):
        dynamic_data = {}
        dynamic_data["E"] = state[0]
        dynamic_data["V"] = state[1]
        dynamic_data["T"] = state[2]
        dynamic_data["mode"] = controllable_mode
        dynamic_data["valve"] = 0  # self.u_actions[index]
        dynamic_data["t"] = index
        dynamic_data["Te"] = list(self.Te[index:index+self.H])
        dynamic_data["Ti"] = list(self.Ti[index:index+self.H])
        dynamic_data["I"] = list(self.I[index:index+self.H])
        file = open(f"{DATA_DIR}/dynamic_data.json", 'w', encoding='utf-8')
        file.write(json.dumps(dynamic_data, indent=4, sort_keys=True))
        return

    def p2array(self, points, key):
        for i in range(0, len(points)):
            points[i] = points[i][1:-1].split(",")
            points[i][0] = float(points[i][0])
            points[i][1] = float(points[i][1])
        mlist = [None]*self.nrSteps
        for i in range(0, len(points)-1):
            if (points[i][0] == points[i+1][0] and points[i+1][0] != self.nrSteps*self.tau):
                it = int(points[i][0]/self.tau)
                mlist[it] = points[i+1][1]  # int
        for i in range(0, self.nrSteps):
            if mlist[i] == None:
                # estoy en duda pero parece que funciona xd
                mlist[i] = mlist[i-1]
        maxl = int(points[-1][0]/5)
        if key == "visitedPatterns":
            print("visitedpatterns: ", points,
                  "  we can also plot this in real time")
            # for p in points:
            #     plt.plot(p[0], p[1], '-ok', linewidth=0.8)
            #     plt.ylabel('visited pat')
            #     plt.xlabel('t(hr)')
            #     plt.grid(True, linewidth=0.6, linestyle='--')
            #     plt.pause(0.05)
            # plt.pause(5.0)
            return maxl
        return mlist

    def receive_strategy_from_uppaal(self):
        res = os.popen(COMMAND).readlines()
        # print("Res: ", res)
        params = {}
        # params["ppos"] = 0
        params["visitedPatterns"] = 0
        params["mode"] = 0
        # params["flag"] = 0
        # params["value"] = 0
        params["Tnext"] = 0
        # params["zi"] = 0
        # params["mvalve"] = 0
        # params["X"] = 0
        # params["NUM_PATTERNS"] = 0
        for i in range(0, len(res)-1):
            if params.get(res[i][:-2]) != None:  # removing :\n with -3
                key = res[i][:-2]
                params[key] = self.p2array(res[i+1][:-1].split()[1:], key)

        # time.sleep(2)
        params["Tnext"] = params["Tnext"][0]
        max = params["visitedPatterns"]
        params["mode"] = [int(v) for v in params["mode"][0:max]]
        print("T predicted uppaal: ", params["Tnext"])
        print("pattern:", params["mode"], "size:", len(params["mode"]))
        return params["mode"]

    #   **************** Tasks **************
    '''
        cost_function -> paretoFunc
        cost -> pareto
        forecasting of T, Te, Ti
        add sthocasticity on uppaal template for valve 0.5 and 0.5
        intrerval??
        dynamic_data["Te"] = list(self.Te[index:index+self.H])
        extras:
        ******
        move  send_save_parameters on SWH model
    '''

    def predict(self, controllable_mode, state, index):
        # hay un error en el index 765 previo a 695,  luego en otra iteracion error en index 480 previo a 405
        print("index: ", index)
        print("mode to predict: ", controllable_mode)
        print("T: ", state[2])
        predicted_state = list(state)
        for i in range(index, index + self.tau):
            predicted_state = self.model.post(
                controllable_mode, predicted_state, i)  # antes era index
        print("T predicted on step: ", predicted_state[2])
        time.sleep(3)
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

    def get_tau(self):
        return self.tau

    def get_pat(self):
        return self.pat

    def get_controllable_actions(self):
        return self.c_actions

    def get_uncontrollable_actions(self):
        return self.u_actions

    @ staticmethod
    def add_to_argparse(parser):
        parser.add_argument("--tau", type=int, default=TAU)
        return parser

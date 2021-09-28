from typing import Any, Dict
import argparse
import numpy as np
import json
import random
from stochastic_hybrid_game.src.data.base_data_module import BaseDataModule
from stochastic_hybrid_game.src.data.SOLAR import SOLAR
# OBS: Dynamical neuroscience -> Biological neural network https://en.wikipedia.org/wiki/Dynamical_neuroscience
# Time series and panel data econometrics, Econometrics in Theory and Practice: Analysis of Cross Section, Time Series and Panel Data with Stata 15.1
# parameters.json ---> Safe c++ IBex ---> patterns, zonotopes
#            |                                |---------------> python
#            |------------------------------------------------>  API

DATA_DIR = BaseDataModule.data_dirname()

SAFE_DATA = json.load(open(f"{DATA_DIR}/static_data.json"))
# -> [E,V,T] # [0.13, 50.0, 0.0]  # pattern [0, 7]
INITIAL_STATE = [0.0, 0.13, 50.0]
TAU = SAFE_DATA["tau"]
FACTOR_TE = SAFE_DATA["factorTe"]
FACTOR_I = SAFE_DATA["factorI"]
FACTOR_KE = SAFE_DATA["factorKe"]
RATE = SAFE_DATA["rate"]
TWATER_IN = SAFE_DATA["TwaterIn"]
R_BOUNDARY = SAFE_DATA["R"]
S_BOUNDARY = SAFE_DATA["S"]
NUMBER_STEPS = SAFE_DATA["nrSteps"]

NUM_ACTIONS = SAFE_DATA["num_actions"]
STANDARD_DEVIATION = SAFE_DATA["standard_deviation"]


#           p, r, f    -> this c_mode order is copied from c++ code model.cpp
C_MODES = [[1, 0, 0],
           [1, 1, 0],
           [2, 0, 0],
           [2, 1, 0],
           [3, 0, 1],
           [3, 1, 1],
           [2, 0, 1],
           [2, 1, 1]]


class SWH():
    def __init__(self, data_config: Dict[str, Any], disturbs: Dict[str, Any], args: argparse.Namespace = None) -> None:
        self.args = vars(args) if args is not None else {}
        self.life_time = data_config["life_time"]
        self.data_sample_time = data_config["data_sample_time"]
        self.start_time = data_config["start_time"]
        self.dt = data_config["dt"]
        self.Te = disturbs["Te"]
        self.Ti = disturbs["Ti"]
        self.I = disturbs["I"]
        self.t = disturbs["t"]
        self.factorTe = FACTOR_TE
        self.factorI = FACTOR_I
        self.factorKe = FACTOR_KE
        self.x = INITIAL_STATE
        R = R_BOUNDARY
        S = S_BOUNDARY
        #self.u_modes = (np.zeros(int(self.life_time))).tolist()

    def post(self, mode: int, u_action: int, x: list, index: int) -> list:  # u_action: int
        c_actions = C_MODES[mode]
        # u_action = 0
        dt_sec = self.dt*60
        E = x[0] + dt_sec*c_actions[1]*2
        V = x[1] + dt_sec*0.01000*(0.1*c_actions[0] - x[1])
        T = x[2] + dt_sec*(1/(0.1*c_actions[0]))*(
            - self.factorTe*2.8811059759131854e-06*(x[2]-self.Te[index])
            - u_action*9.34673995175876e-05*(x[2]-self.Ti[index])
            - c_actions[2]*self.factorKe*0.001005026 *
            (0.1*c_actions[0]-x[1])*(x[2]-self.Ti[index])
            + self.factorI*0.7*0.7*8.403225763080125e-07*self.I[index]
            + c_actions[1]*0.008801843)
        x[0] = E
        x[1] = V
        x[2] = T
        return x

    def get_uncontrollable_actions(self):
        with open(f"{DATA_DIR}/uncontrollable_data_{STANDARD_DEVIATION}_{NUM_ACTIONS}.txt", 'r', newline='') as file:
            lines = file.readlines()
        lines = [float(line[0:-1]) for line in lines]
        return list(lines)

    def update(self, mode, u_action, state, index):
        state = self.post(mode, u_action, state, index)
        return state

    def get_initial_state(self):
        return INITIAL_STATE

    def get_controllable_modes(self):
        return C_MODES

    def get_number_steps(self):
        return NUMBER_STEPS

    @ staticmethod
    def add_to_argparse(parser):
        parser.add_argument("--fc1", type=int, default=1024)
        parser.add_argument("--fc2", type=int, default=128)
        return parser

    @ classmethod
    def generate_uncontrollable_data(cls):
        data = BaseDataModule()
        data_config = data.config()
        life_time = data_config["life_time"]
        start_time = data_config["start_time"]
        u_modes = (np.zeros(int(life_time))).tolist()
        #num_actions = random.randrange(100, 200)
        num_actions = NUM_ACTIONS
        standard_deviation = STANDARD_DEVIATION  # 1*12  # 2
        for i in range(0, num_actions):
            u_modes[int(random.gauss(start_time +
                                     7*60, standard_deviation))] += 1
            u_modes[int(random.gauss(start_time +
                                     13*60, standard_deviation))] += 1
            u_modes[int(random.gauss(start_time +
                                     19*60, standard_deviation))] += 1
        num_actions2 = 10  # random.randrange(10, 20)
        for i in range(0, num_actions2):
            u_modes[int(random.uniform(start_time, life_time))] += 1
        # write on file
        with open(f"{DATA_DIR}/uncontrollable_data_{standard_deviation}_{num_actions}.txt", 'w', newline='') as file:
            for e in u_modes:
                file.write(str(e)+"\n")
        return


if __name__ == '__main__':

    SWH.generate_uncontrollable_data()

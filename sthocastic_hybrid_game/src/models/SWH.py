
from typing import Any, Dict
import argparse
import numpy as np
import json
import random
from sthocastic_hybrid_game.src.data.base_data_module import BaseDataModule
# OBS: Dynamical neuroscience -> Biological neural network https://en.wikipedia.org/wiki/Dynamical_neuroscience
# Time series and panel data econometrics, Econometrics in Theory and Practice: Analysis of Cross Section, Time Series and Panel Data with Stata 15.1

# parameters.json ---> Safe c++ IBex ---> patterns, zonotopes
#            |                                |---------------> python
#            |------------------------------------------------>  API

DATA_DIR = BaseDataModule.data_dirname()
SAFE_DATA = json.load(open(f"{DATA_DIR}/parameters.json"))
INITIAL_STATE = [0.0, 0.13, 50.0]  # -> [E,V,T] # [0.13, 50.0, 0.0]
FACTOR_TE = SAFE_DATA["factorTe"]
FACTOR_I = SAFE_DATA["factorI"]
FACTOR_KE = SAFE_DATA["factorKe"]
RATE = SAFE_DATA["rate"]
TWATER_IN = SAFE_DATA["TwaterIn"]

C_MODES = [[1, 0, 0],
           [1, 1, 0],
           [2, 0, 0],
           [2, 1, 0],
           [3, 0, 1],
           [3, 1, 1],
           [2, 0, 1],
           [2, 1, 1]]

U_MODES = np.zeros(24*12).tolist()


def uncontrollable_action_generation():
    U_MODES = (np.zeros(24*12)).tolist()
    num_actions = random.randrange(5, 8)
    standard_deviation = 1*3  # 1*60/5
    for i in range(0, num_actions):
        U_MODES[int(random.gauss(7*60/5, standard_deviation))] = 1
        U_MODES[int(random.gauss(13*60/5, standard_deviation))] = 1
        U_MODES[int(random.gauss(19*60/5, standard_deviation))] = 1
    return U_MODES


class SWH():
    def __init__(self, data_config: Dict[str, Any], disturbs: Dict[str, Any], args: argparse.Namespace = None) -> None:
        self.args = vars(args) if args is not None else {}
        self.life_time = data_config["life_time"]
        self.data_sample_time = data_config["data_sample_time"]
        self.dt = data_config["dt"]
        self.Te = disturbs["Te"]
        self.Ti = disturbs["Ti"]
        self.I = disturbs["I"]
        self.factorTe = FACTOR_TE
        self.factorI = FACTOR_I
        self.factorKe = FACTOR_KE
        self.x = INITIAL_STATE
        uncontrollable_action_generation()

    # @classmethod
    def post(self, mode: int, x: list, index: int) -> list:
        c_actions = C_MODES[mode]
        u_action = 0  # U_MODES[index]
        x[0] = x[0] + self.dt*c_actions[1]*2
        x[1] = x[1] + self.dt*0.01000*(0.1*c_actions[0] - x[1])
        x[2] = x[2] + self.dt*(1/(0.1*c_actions[0]))*(
            - self.factorTe*2.8811059759131854e-06*(x[2]-self.Te[index])
            - u_action*9.34673995175876e-05*(x[2]-self.Ti[index])
            - c_actions[2]*self.factorKe*0.001005026 *
            (0.1*c_actions[0]-x[1])*(x[2]-self.Ti[index])
            + self.factorI*0.7*0.7*8.403225763080125e-07*self.I[index]
            + c_actions[1]*0.008801843)
        return x

    def get_initial_state(self):
        return INITIAL_STATE

    def get_controllable_modes(self):
        return C_MODES

    def update(self, mode, x, index):
        self.x = self.post(mode, x, index)
        return self.x

    @ staticmethod
    def add_to_argparse(parser):
        parser.add_argument("--fc1", type=int, default=1024)
        parser.add_argument("--fc2", type=int, default=128)
        return parser

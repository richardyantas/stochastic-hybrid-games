'''
    This code is to optimize the strategy search through a stochastic approach using Uppaal
    run: python stochastic_hybrid_game/src/run_experiment.py --controller=MPC.Uppaal
    Author: Richard Yantas
'''

from typing import Any, Dict
import json
import os
import argparse
from stochastic_hybrid_game.src.data.base_data_module import BaseDataModule
from stochastic_hybrid_game.src.controllers.MPC import MPC
from stochastic_hybrid_game.src.data.SOLAR import predict_solar_data

DATA_DIR = BaseDataModule.data_dirname()
SAFE_DATA = json.load(open(f"{DATA_DIR}/static_data.json"))
COMMAND = "lib/uppaal/bin-Linux/verifyta sources/uppaal/swh3.xml sources/uppaal/swh.q"
TAU = SAFE_DATA["tau"]


class Uppaal(MPC):
    def __init__(self, model: Any, data_config: Dict[str, Any], disturbs: Dict[str, Any], args: argparse.Namespace = None):
        MPC.__init__(self, model, data_config, disturbs, args)
        self.command = COMMAND
        self.tau = TAU

    def get_pattern(self, controllable_mode, state, index):
        self.send_save_data2uppaal(controllable_mode, list(state), index)
        optimal_pattern = self.receive_strategy_from_uppaal()
        return optimal_pattern

    def send_save_data2uppaal(self, controllable_mode, state, index):
        pivot = 24*60
        Te = predict_solar_data(
            self.disturbs["Te"][0:index], pivot, self.prediction_size)
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
        file = open(f"{self.data_dir}/dynamic_data.json",
                    'w', encoding='utf-8')
        file.write(json.dumps(dynamic_data, indent=4, sort_keys=True))
        return

    def pre_convert2array(self, points):
        for i in range(0, len(points)):
            points[i] = points[i][1:-1].split(",")
            points[i][0] = float(points[i][0])
            points[i][1] = float(points[i][1])
        return points

    def convert2array(self, points):  # HERE PROBLEM !!
        horizon_permitted = int(points[-1][0]/self.tau)
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
        params["mode"] = [int(p) for p in params["mode"]["list"]]
        pattern = self.filter_pattern(
            params["mode"], params["visitedPatterns"]["list"])
        print("pattern: ", pattern, "size: ", len(pattern))
        return pattern

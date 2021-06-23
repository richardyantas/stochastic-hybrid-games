# pytest -v sthocastic_hybrid_game/tests/test_UPPAAL.py
# To also see the output ass -s
# pytest -v sthocastic_hybrid_game/tests/test_UPPAAL.py -s
from types import DynamicClassAttribute
from stochastic_hybrid_game.src.controllers.UPPAAL import UPPAAL
from stochastic_hybrid_game.src.models.SWH import SWH
from stochastic_hybrid_game.src.data.SOLAR import SOLAR
from stochastic_hybrid_game.src.data.base_data_module import BaseDataModule
import matplotlib.pyplot as plt
import numpy as np
import argparse
import pytest
import json
import time
from interval import interval

data = SOLAR(args=None)
model = SWH(data_config=data.config(), disturbs=data.loader_data())
controller = UPPAAL(model, data_config=data.config(),
                    disturbs=data.loader_data(), args=None)

DATA_DIR = BaseDataModule.data_dirname()
SAFE_RES = json.load(open(f"{DATA_DIR}/pattern.json"))
DYNAMIC_DATA = json.load(open(f"{DATA_DIR}/dynamic_data.json"))
STATIC_DATA = json.load(open(f"{DATA_DIR}/static_data.json"))
POINTS_DATA = json.load(open(f"{DATA_DIR}/uppaal_response_data.json"))

R = STATIC_DATA["R"]
PATTERNS = SAFE_RES["patterns"]
ZONOTOPES = SAFE_RES["zonotopes"]
TAU = STATIC_DATA["tau"]
disturbs = data.loader_data()


def plot_points(points1, points2):
    p1x = []
    p1y = []
    p2x = []
    p2y = []
    # yy = []
    for v in points1:
        p1x.append(v[0])
        p1y.append(v[1])
        # yy.append(v[1]/2)
    for v in points2:
        p2x.append(v[0])
        p2y.append(v[1])

    # plt.axis([0, 20, 0, 10])
    plt.plot(p1x, p1y, drawstyle='steps', linewidth=0.8, color='r')
    plt.plot(p2x, p2y, drawstyle='steps', linewidth=0.8)
    plt.grid(True, linewidth=0.6, linestyle='--')
    plt.show()


def test_forecasting():
    Te = disturbs["Te"]
    index = 3*60
    predicted = controller.forecast_disturbances(
        list(Te[index-1*60:index]), 5*60, 60)
    print(predicted)
    # #pTe = self.forecast(list(self.Te[t_min-60*24:t_min]), 5*60, 59)
    assert 1 == 1


def test_points_recevied():
    print("")
    # for response in POINTS_DATA:
    #     print("visitedPatterns: ", response["visitedPatterns"]["list"])
    #     print("mode: ", response["mode"]["list"])
    #     new_pattern = controller.filter_pattern(
    #         response["mode"]["list"], response["visitedPatterns"]["list"])

    #     print("new pattern: ", new_pattern)
    # plot_points(response["visitedPatterns"]["points"],
    #            response["mode"]["points"])

    assert 1 == 1


def test_disturbances():
    Te = disturbs["Te"]
    Ti = disturbs["Ti"]
    I = disturbs["I"]
    index = DYNAMIC_DATA["t"]
    Te_dynamic = DYNAMIC_DATA["Te"]
    Ti_dynamic = DYNAMIC_DATA["Ti"]
    I_dynamic = DYNAMIC_DATA["I"]
    tau = STATIC_DATA["tau"]
    nrSteps = STATIC_DATA["nrSteps"]
    H_tau = (nrSteps+1)*tau
    assert all([a == b for a, b in zip(Te[index:index+H_tau], Te_dynamic)])
    assert all([a == b for a, b in zip(Ti[index:index+H_tau], Ti_dynamic)])
    assert all([a == b for a, b in zip(I[index:index+H_tau], I_dynamic)])


def test_zonotope_hist():
    assert 3 == 3


def test_pattern_post():
    state = [0.0, 0.0, 0.0]
    state[0] = DYNAMIC_DATA["E"]
    state[1] = DYNAMIC_DATA["V"]
    state[2] = DYNAMIC_DATA["T"]
    t = DYNAMIC_DATA["t"]
    mode = DYNAMIC_DATA["mode"]
    for i in range(t, t+TAU):  # prediction
        state = model.post(mode, 0, state, i)
    t = t + TAU
    D = [0, 6]
    U = [0, 7]
    # patterns = [U, D, D, U, D, D, D, D]
    patterns = []
    # patterns = [D, D, D, D, D, D, D]
    for pattern in patterns:
        for mod in pattern:
            for i in range(t, t+TAU):
                state = model.post(mod, 0, state, i)
            t = t + TAU
    r1 = interval[R[0][0], R[0][1]]
    r2 = interval[R[1][0], R[1][1]]
    assert state[2] in r1 and state[1] in r2


def test_uppaal_p2array():
    # read data from run_experiment in json format
    visited_patterns_points = [[0.0, 0.0], [0.0, 1.0], [10.0, 1.0], [10.0, 2.0], [20.0, 2.0], [20.0, 3.0], [30.0, 3.0], [30.0, 4.0], [
        40.0, 4.0], [40.0, 5.0], [50.0, 5.0], [50.0, 6.0], [60.0, 6.0], [60.0, 7.0], [70.0, 7.0], [70.0, 8.0]]
    # one by one convert it
    # visited_patterns = controller.convert2array(visited_patterns_points)
    assert 2 == 2


def test_uppaal_read_response():
    visited_patterns = [[0.0, 0.0], [0.0, 1.0], [15.0, 1.0], [15.0, 2.0], [25.0, 2.0], [25.0, 3.0], [
        35.0, 3.0], [35.0, 4.0], [45.0, 4.0], [45.0, 5.0], [55.0, 5.0], [55.0, 6.0], [65.0, 6.0], [65.0, 7.0]]
    assert 1 == 1


# if key == "visitedPatterns":
#     print("visitedpatterns: ", points)
#     # for p in points:
#     #     plt.plot(p[0], p[1], '-ok', linewidth=0.8)
#     #     plt.ylabel('visited pat')
#     #     plt.xlabel('t(hr)')
#     #     plt.grid(True, linewidth=0.6, linestyle='--')
#     #     plt.pause(0.05)
#     # plt.pause(5.0)
#     return maxl

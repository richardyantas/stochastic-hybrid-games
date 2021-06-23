# pytest -v sthocastic_hybrid_game/tests/test_SWH.py
from stochastic_hybrid_game.src.models.SWH import SWH
from stochastic_hybrid_game.src.data.SOLAR import SOLAR
import matplotlib.pyplot as plt
import numpy as np
import argparse
import pytest

data = SOLAR(args=None)
model = SWH(data_config=data.config(), disturbs=data.loader_data())


def test_swh_post():
    assert 3 == 3


def test_uncontrollable_actions():
    times = np.linspace(0, model.life_time, model.life_time)
    times_hr = [float(t/60) for t in times]
    u_actions = model.get_uncontrollable_actions()
    plt.axis([0, 1440/(60), 0, 10])
    plt.plot(times_hr, u_actions, drawstyle='steps', linewidth=0.8)
    plt.grid(True, linewidth=0.6, linestyle='--')
    plt.show()
    assert len(u_actions) == len(times)
    assert len(u_actions) == model.life_time


# def test_predict_model_state_is_inside_of_boundary():
#   # [0.1, 0.15, 40.1] -> pat [1, 6] -> mode 1
#   new_state = predict_model_state([0.1, 0.15, 40.1], 8.7, 25.0, 0.0, [1,1,0,0])
#   print(new_state[0])
#   isInside = new_state[1] in interval[R[0][0],R[0][1]], new_state[2] in interval[R[1][0],R[1][1]]
#   assert  isInside == (True, True)

# # @pytest.mark.skip(reason="Uppal methods is not done yet")
# def test_predictiveSafeController_state_after_tube_process():
#   queue = multiprocessing.Queue()
#   data = DataProcessing(filepath1, filepath2)
#   new_state = predictiveSafeController(queue, [0.1, 0.15, 40.1], [1,1,0,0], data.getDisturbanceSeries(), 0)
#   isInside = new_state[1] in interval[R[0][0],R[0][1]], new_state[2] in interval[R[1][0],R[1][1]]
#   assert isInside == (True, True)

# @pytest.mark.skip(reason="Uppal methods is not done yet")
# def test_uppaalController():
#   assert uppaalController()

# if __name__ == '__main__':
# test()

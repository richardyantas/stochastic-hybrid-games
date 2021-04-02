# pytest -q sthocastic_hybrid_game/src/controllers_test.py
# pytest -v sthocastic_hybrid_game/src/controllers_test.py
import pytest
from interval import interval
import multiprocessing
from .dataProcessing import DataProcessing
from .controllers import query, initialSafeController, predict_model_state, predictiveSafeController, uppaalController
from .config import *

def test_query():  
  assert query([0.0, 0.15, 40.1]) == {"pat":[1,6],"i":0}
  assert query([1.1, 220.0, 0.0]) == {"pat":[-1,-1,-1],"i":-1}

def test_initialSafeController():
  
  assert initialSafeController([0.0, 0.15, 40.1]) == [1,6]
  assert initialSafeController([1.1, 220.0, 0.0]) == [-1,-1,-1]

def test_predict_model_state_is_inside_of_boundary():
  # [0.1, 0.15, 40.1] -> pat [1, 6] -> mode 1  
  new_state = predict_model_state([0.1, 0.15, 40.1], 8.7, 25.0, 0.0, [1,1,0,0])
  print(new_state[0])
  isInside = new_state[1] in interval[R[0][0],R[0][1]], new_state[2] in interval[R[1][0],R[1][1]]
  assert  isInside == (True, True)

# @pytest.mark.skip(reason="Uppal methods is not done yet")
def test_predictiveSafeController_state_after_tube_process():
  queue = multiprocessing.Queue()
  data = DataProcessing(filepath1, filepath2)
  new_state = predictiveSafeController(queue, [0.1, 0.15, 40.1], [1,1,0,0], data.getDisturbanceSeries(), 0) 
  isInside = new_state[1] in interval[R[0][0],R[0][1]], new_state[2] in interval[R[1][0],R[1][1]]
  assert isInside == (True, True)

@pytest.mark.skip(reason="Uppal methods is not done yet")
def test_uppaalController():
  assert uppaalController()
  

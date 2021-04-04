
import pytest
from interval import interval
import multiprocessing
from .dataProcessing import DataProcessing
from .simulation import simulation, supervisor
from .config import *

def test_supervisor():
  queue = multiprocessing.Queue()
  data = DataProcessing(filepath1, filepath2)
  mode, pat = supervisor(queue, [1,6], [0.1, 0.15, 40.1], data.getDisturbanceSeries(), 0)
  assert [mode, pat] == [[1, 1, 0, 0], [6]]

@pytest.mark.skip(reason="update model state method is not done yet")
def test_update_model_state():
  assert 0 == 0

# @pytest.mark.skip(reason="simulation method is not done yet")
def test_simulation():
  data = DataProcessing(filepath1, filepath2)
  new_state = simulation("normal", [0.1, 0.15, 40.1], data.getDisturbanceSeries() )
  isInside = new_state[1] in interval[R[0][0],R[0][1]], new_state[2] in interval[R[1][0],R[1][1]]
  assert isInside == (True, True)


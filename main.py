
from sthocastic_hybrid_game.src.dataProcessing import DataProcessing
from sthocastic_hybrid_game.src.simulation import simulation
from sthocastic_hybrid_game.src.config import *

data = DataProcessing(filepath1, filepath2)
simulation("normal", [0.0, 0.11, 42.0], data.getDisturbanceSeries())


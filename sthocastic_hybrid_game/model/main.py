import controllerss
import pandas as pd

from   statsmodels.tsa.arima_model import ARIMA

from   statsmodels.tsa.arima_model import ARIMA

dataRead = pd.read_csv("./sthocastic_hybrid_game/datasets/Solargis_min15_Almeria_Spain.csv")
valveRead= pd.read_csv("./sthocastic_hybrid_game/datasets/valve.csv")  # t1,t2,dur 

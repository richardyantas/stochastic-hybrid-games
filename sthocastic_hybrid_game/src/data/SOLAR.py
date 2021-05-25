import numpy as np
import pandas as pd
import argparse
from sthocastic_hybrid_game.src.data.base_data_module import BaseDataModule

DATA_DIR = BaseDataModule.data_dirname()
WATER_TEMPERATURE_INPUT = 25


class SOLAR(BaseDataModule):
    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)
        self.data_dir = DATA_DIR
        self.data = pd.read_csv(
            f"{DATA_DIR}/Solargis_min15_Almeria_Spain.csv")

    def extraction_data(self):
        num_intervals = int(
            self.life_time/self.data_sample_time)
        t = np.linspace(0, self.life_time, num_intervals + 1)
        Te = self.data['Temperature'].values.tolist()[0:num_intervals+1]
        I = self.data['GTI'].values.tolist()[0:num_intervals+1]
        return {"t": t, "Te": Te, "I": I}

    def transform_data(self, *args, **kwargs) -> None:
        previous_data = self.extraction_data()
        new_num_intervals = int(self.life_time/self.dt) + 1
        t = np.linspace(0, self.life_time, new_num_intervals)
        Te = np.interp(t, previous_data["t"], previous_data["Te"])
        I = np.interp(t, previous_data["t"], previous_data["I"])
        Ti = np.ones(new_num_intervals + 1) * WATER_TEMPERATURE_INPUT
        return {"Te": Te, "I": I, "Ti": Ti}

    def loader_data(self):
        data = self.transform_data()
        return data


if __name__ == "__main__":
    load_and_print_info(SOLAR)

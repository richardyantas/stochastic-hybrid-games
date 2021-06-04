import numpy as np
import pandas as pd
import random
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
        return {"Te": Te, "I": I, "Ti": Ti, "t": t}

    def uncontrollable_action_generation(self):
        # valves for water consumption on buildings , tau = 5 !!! IMPORTANT to link with the general tau from controller in some way
        print("dt:", self.dt)
        U_MODES = (np.zeros(int(self.life_time/(5*60)))).tolist()
        num_actions = random.randrange(5, 8)
        standard_deviation = 1*3  # 1*60/5
        for i in range(0, num_actions):
            U_MODES[int(random.gauss(7*60/5, standard_deviation))] = 1
            U_MODES[int(random.gauss(13*60/5, standard_deviation))] = 1
            U_MODES[int(random.gauss(19*60/5, standard_deviation))] = 1
        print("umodes:", len(U_MODES))
        return U_MODES

    def loader_data(self):
        data = self.transform_data()
        return data


if __name__ == "__main__":
    load_and_print_info(SOLAR)

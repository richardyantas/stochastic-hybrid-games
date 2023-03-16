from pathlib import Path
import argparse
import json

DATA_DIR = Path(__file__).resolve().parents[2]/"data/solar-water-heating/"
STATIC_DATA = json.load(open(f"{DATA_DIR}/static_data.json"))
# 2*24*60  # 3*24*60 # (in min) two days  BATCH_SIZE
LIFE_TIME = STATIC_DATA["life_time"]
START_TIME = STATIC_DATA["start_time"]  # 1*24*60
DATA_SAMPLE_TIME = STATIC_DATA["data_sample_time"]  # (in min)
DT = STATIC_DATA["dt"]  # 1  # data_resample_time (in min)

# NUMBER_STEPS = 15
# OBS: we can use pandas propeties to process data or numpy, an also create an API
# vars returns the __dict__ attribute of the given project


class BaseDataModule():
    def __init__(self, args: argparse.Namespace = None) -> None:
        self.args = vars(args) if args is not None else {}
        self.start_time = int(self.args.get(
            "start_time", START_TIME))
        self.life_time = int(self.args.get(
            "life_time", LIFE_TIME))
        self.data_sample_time = self.args.get(
            "data_sample_time", DATA_SAMPLE_TIME)
        self.dt = self.args.get("dt", DT)

    @classmethod
    def data_dirname(cls):
        return Path(__file__).resolve().parents[2]/"data/solar-water-heating/"

    def config(self):
        return {"start_time": self.start_time, "life_time": self.life_time, "data_sample_time": self.data_sample_time, "dt": self.dt}

    @staticmethod
    def add_to_argparse(parser):
        parser.add_argument("--start_time", type=int, default=START_TIME)
        parser.add_argument("--life_time", type=int, default=LIFE_TIME)
        parser.add_argument("--data_sample_time", type=int,
                            default=DATA_SAMPLE_TIME)
        parser.add_argument("--dt", type=int, default=DT)
        return parser


if __name__ == "__main__":
    DATA_DIR = Path(__file__).resolve().parents[2]/"data/solar-water-heating/"
    print(DATA_DIR)

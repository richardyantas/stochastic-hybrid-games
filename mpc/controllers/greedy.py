'''
This code is to optimize the strategy search
run: python stochastic_hybrid_game/src/run_experiment.py --controller=MPC.Greedy
References: https://locuslab.github.io/mpc.pytorch/
Author: Richard Yantas
'''

from typing import Any, Dict
import argparse
import json
from mpc.data.base_data_module import BaseDataModule
from mpc.controllers import MPC

DATA_DIR = BaseDataModule.data_dirname()
SAFE_DATA = json.load(open(f"{DATA_DIR}/static_data.json"))
TG = SAFE_DATA["Tg"]
ALPHA = SAFE_DATA["alpha"]


class Greedy(MPC):
    def __init__(self, model: Any, data_config: Dict[str, Any], disturbs: Dict[str, Any], args: argparse.Namespace = None):
        MPC.__init__(self, model, data_config, disturbs, args)
        self.Tg = TG
        self.alpha = ALPHA

    def get_pattern(self, controllable_mode, state, index):
        predicted_state = state
        for i in range(index, index + self.tau):
            predicted_state = self.model.post(
                controllable_mode, self.u_actions[i], predicted_state, i)  # antes era index creo que en u_actions[i] deberia de ser i ne vez de index
        patterns = self.query_safe_patterns(predicted_state)
        optimal_meta_pattern = self.optimal_pattern_search(
            predicted_state, index+self.tau, patterns)
        return optimal_meta_pattern

    def optimal_pattern_search(self, state, index, candidate_patterns):
        next_state = list(state)
        optimal_pattern = []
        min_costFunction = 100000.0
        for candidate_pattern in candidate_patterns:
            m_index = index
            temporal_state = list(next_state)
            for mode in candidate_pattern:
                for i in range(m_index, m_index+self.tau):
                    temporal_state = self.model.post(
                        mode, self.u_actions[i], temporal_state, i)
                m_index = m_index + self.tau
            costFunction = self.alpha * \
                temporal_state[0]+(1-self.alpha)*abs(self.Tg-temporal_state[2])
            if (costFunction < min_costFunction):
                min_costFunction = float(costFunction)
                optimal_pattern = list(candidate_pattern)
        print("optimal pattern: ", optimal_pattern)
        return optimal_pattern

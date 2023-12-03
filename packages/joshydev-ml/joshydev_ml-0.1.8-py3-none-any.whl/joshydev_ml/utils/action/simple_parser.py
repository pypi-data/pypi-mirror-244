import numpy as np
import joshydev_ml.gym.spaces


class SimpleParser():
    def __init__(self, n_bins=3):
        super().__init__()
        assert n_bins % 2 == 1, "n_bins must be an odd number"
        self._n_bins = n_bins

    def get_action_space(self) -> joshydev_ml.gym.spaces.Space:
        return joshydev_ml.gym.spaces.MultiDiscrete([self._n_bins] * 5 + [2] * 3)

    def parse_actions(self, actions: np.ndarray, state) -> np.ndarray:
        actions = actions.reshape((-1, 8))
        actions[..., :5] = actions[..., :5] / (self._n_bins // 2) - 1
        return actions

import joshydev_ml.gym.spaces as spaces
from joshydev_ml.gym import ObservationWrapper


class FlattenObservation(ObservationWrapper):
    r"""Observation wrapper that flattens the observation."""

    def __init__(self, env):
        super(FlattenObservation, self).__init__(env)
        self.observation_space = spaces.flatten_space(env.observation_space)

    def observation(self, observation):
        return spaces.flatten(self.env.observation_space, observation)

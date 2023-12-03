from joshydev_ml.gym.envs.mujoco.mujoco_env import MujocoEnv

# ^^^^^ so that user gets the correct error
# message if mujoco is not installed correctly
from joshydev_ml.gym.envs.mujoco.ant import AntEnv
from joshydev_ml.gym.envs.mujoco.half_cheetah import HalfCheetahEnv
from joshydev_ml.gym.envs.mujoco.hopper import HopperEnv
from joshydev_ml.gym.envs.mujoco.walker2d import Walker2dEnv
from joshydev_ml.gym.envs.mujoco.humanoid import HumanoidEnv
from joshydev_ml.gym.envs.mujoco.inverted_pendulum import InvertedPendulumEnv
from joshydev_ml.gym.envs.mujoco.inverted_double_pendulum import InvertedDoublePendulumEnv
from joshydev_ml.gym.envs.mujoco.reacher import ReacherEnv
from joshydev_ml.gym.envs.mujoco.swimmer import SwimmerEnv
from joshydev_ml.gym.envs.mujoco.humanoidstandup import HumanoidStandupEnv
from joshydev_ml.gym.envs.mujoco.pusher import PusherEnv
from joshydev_ml.gym.envs.mujoco.thrower import ThrowerEnv
from joshydev_ml.gym.envs.mujoco.striker import StrikerEnv

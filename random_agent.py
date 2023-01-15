from random import randint

from ray.rllib.algorithms.algorithm import Algorithm
from environment import GridWorldEnv
from ray_env_wrapper import AntiJamEnv


class RandomAgent:
    def compute_actions(self, env: GridWorldEnv):
        # return: {"light_{i}": 0 or 1}
        return {f"light_{i}":  randint(0, 1) for i in range(len(env.junctions))}

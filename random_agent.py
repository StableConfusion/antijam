from random import randint

from ray.rllib.algorithms.algorithm import Algorithm
from environment import GridWorldEnv
from ray_env_wrapper import AntiJamEnv


class RandomAgent:
    def compute_actions(self, env: GridWorldEnv):
        # return: {"light_{i}": 0 or 1}
        if env.day % 10 != 0:
            return {f"light_{i}": env.junctions[i].state for i in range(len(env.junctions))}
        else:
            return {f"light_{i}":  1 - env.junctions[i].state for i in range(len(env.junctions))}

from ray.rllib.algorithms.algorithm import Algorithm
from environment import GridWorldEnv
from ray_env_wrapper import AntiJamEnv


class TrainedAgent:
    def __init__(self, checkpoint_path):
        self.algo = Algorithm.from_checkpoint(checkpoint_path)
        self.env = AntiJamEnv({})

    def compute_actions(self, env: GridWorldEnv):
        # return: {"light_{i}": 0 or 1}
        self.env.env = env
        obs = {
            f'light_{i}': self.env.get_light_observation(i)
            for i in range(self.env.num_lights)
        }
        return self.algo.compute_single_action(obs)

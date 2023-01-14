from gym.spaces import Discrete, Box
from ray.rllib.env import MultiAgentEnv, EnvContext


class AntiJamEnv(MultiAgentEnv):
    def __init__(self, config: EnvContext):
        self.num_lights: int = config["num_lights"]
        self.grid_size: tuple[int, int] = config["grid_size"]
        self.action_space = {
            f"light_{i}": Discrete(2) for i in range(self.num_lights)
        }
        self.observation_space = {
            f"light_{i}": Box(
                low=0,
                high=1,
                shape=(self.grid_size[0], self.grid_size[1], 5),
                dtype="uint8",
            ) for i in range(self.num_lights)
        }

    def reset(self):
        pass

    def step(self, action_dict):
        # action_dict: {"light_{i}": 0 or 1}
        # return:
        #     obs_dict: {"light_{i}": NxMx5 tensor}
        #     reward_dict: {"light_{i}": mean car speed}
        #     done_dict: {"light_{i}": False, "__all__": False}
        #     info_dict: {"light_{i}": {}}
        pass

    def render(self, mode='human'):
        pass

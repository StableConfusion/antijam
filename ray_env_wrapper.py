'''
Implements action/observation spaces and rewards for the environment.
'''

import numpy as np
from gym.spaces import Discrete, Box
from ray.rllib.env import MultiAgentEnv, EnvContext
from environment import GridWorldEnv


class AntiJamEnv(MultiAgentEnv):
    def __init__(self, config: EnvContext):
        super().__init__()

        self.env = GridWorldEnv()

        self._agent_ids = [
            f"light_{i}" for i in range(len(self.env.junctions))]

        self.num_lights: int = len(self.env.junctions)
        self.num_cars: int = len(self.env.vehicles)
        self.grid_size: tuple[int, int] = self.env.map.shape

        self.action_space = Discrete(2)

        self.observation_space = Box(
            low=0,
            high=1,
            # shape=(5, self.grid_size[0], self.grid_size[1]),
            shape=(5 * self.grid_size[0] * self.grid_size[1],),
            dtype=np.uint8,
        )

    def reset(self):
        self.env = GridWorldEnv()
        obs_dict = {}
        for i in range(self.num_lights):
            obs_dict[f"light_{i}"] = self.get_light_observation(i)
        return obs_dict

    def step(self, action_dict):
        # action_dict: {"light_{i}": 0 or 1}
        # return:
        #     obs_dict: {"light_{i}": NxMx5 tensor}
        #     reward_dict: {"light_{i}": mean car speed}
        #     done_dict: {"light_{i}": False, "__all__": False}
        #     info_dict: {"light_{i}": {}}
        obs_dict = {}
        reward_dict = {}
        done_dict = {}
        info_dict = {}

        for i in range(self.num_lights):
            self.env.junctions[i].set_state(action_dict[f"light_{i}"])

        num_moved = self.env.step()
        reward = num_moved / self.num_cars

        for i in range(self.num_lights):
            obs_dict[f"light_{i}"] = self.get_light_observation(i)
            reward_dict[f"light_{i}"] = reward
            done_dict[f"light_{i}"] = False
            info_dict[f"light_{i}"] = {}

        done_dict["__all__"] = False

        return obs_dict, reward_dict, done_dict, info_dict

    def get_light_observation(self, light_id):
        # observation contains:
        # - available junctions
        # - car positions
        # - position of this agent's junction
        # - position of traffic lights in state 0
        # - position of traffic lights in state 1
        # - optionally a map (was removed to speed up training)

        obs = np.zeros(
            (self.grid_size[0], self.grid_size[1], 6), dtype=np.uint8)

        # obs[:, :, 0] = np.where(self.env.map == 0, 0, 1)

        for junction in self.env.junctions:
            if junction.cooldown == 0:
                obs[junction.i: junction.i + 2,
                    junction.j: junction.j + 2, 1] = 1

            if junction.state == 0:
                obs[junction.i: junction.i + 2,
                    junction.j: junction.j + 2, 4] = 1

            elif junction.state == 1:
                obs[junction.i: junction.i + 2,
                    junction.j: junction.j + 2, 5] = 1

        for vehicle in self.env.vehicles:
            obs[vehicle.i, vehicle.j, 2] = 1

        this_junction = self.env.junctions[light_id]

        obs[this_junction.i: this_junction.i + 2,
            this_junction.j: this_junction.j + 2, 3] = 1

        return np.stack((
            # obs[:, :, 0],
            obs[:, :, 1],
            obs[:, :, 2],
            obs[:, :, 3],
            obs[:, :, 4],
            obs[:, :, 5],
        )).flatten()

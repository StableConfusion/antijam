import numpy as np
import pygame

from environment import GridWorldEnv
from gui.main_screen import MainScreen, Town
from random_agent import RandomAgent
from trained_agent import TrainedAgent


class ReplayBuffer:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.buffer = []

    def add(self, new_record: float):
        self.buffer.append(new_record)
        if len(self.buffer) >= self.max_size:
            self.buffer.pop(0)

    def get_mean_reward(self):
        return sum(self.buffer) / len(self.buffer)


if __name__ == '__main__':
    env_1 = GridWorldEnv()
    env_2 = GridWorldEnv()

    # env.animate(500)
    ms = MainScreen(env_1.map, verbose=1)
    town_1 = Town(ms, False)
    town_2 = Town(ms, True)
    clock = pygame.time.Clock()

    agent_1 = RandomAgent()
    agent_2 = RandomAgent()
    # agent_2 = TrainedAgent('ray_results/PPO/PPO_antijam_0db8c_00000_0_2023-01-14_22-18-56/checkpoint_000005')

    buffer_size = 100
    r_buffer_1 = ReplayBuffer(buffer_size)
    r_buffer_2 = ReplayBuffer(buffer_size)

    max_step = np.inf
    current_step = 0
    running = True

    while running:
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if current_step <= max_step:

            actions_1 = agent_1.compute_actions(env_1)
            actions_2 = agent_2.compute_actions(env_2)

            for i in range(len(env_1.junctions)):
                env_1.junctions[i].set_state(actions_1[f"light_{i}"])
            for i in range(len(env_2.junctions)):
                env_2.junctions[i].set_state(actions_2[f"light_{i}"])

            r_1 = env_1.step() / len(env_1.vehicles)
            r_2 = env_2.step() / len(env_2.vehicles)

            r_buffer_1.add(r_1)
            r_buffer_2.add(r_2)

            town_1.step(env_1.vehicles, env_1.junctions, r_buffer_1.get_mean_reward())
            town_2.step(env_2.vehicles, env_2.junctions, r_buffer_2.get_mean_reward())

            town_1.update_state()
            town_2.update_state()

            town_1.render_map()
            town_2.render_map()

            ms.render_prompts()

            pygame.display.flip()
            current_step += 1

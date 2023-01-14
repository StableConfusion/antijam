import pygame

from environment import GridWorldEnv
from gui.main_screen import MainScreen, Town
from random_agent import RandomAgent


if __name__ == '__main__':
    env_1 = GridWorldEnv()
    env_2 = GridWorldEnv()

    # env.animate(500)
    ms = MainScreen(env_1.map)
    town_1 = Town(ms, False)
    town_2 = Town(ms, True)
    clock = pygame.time.Clock()

    agent_1 = RandomAgent()
    agent_2 = RandomAgent()

    max_step = 500
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

            env_1.step()
            env_2.step()

            town_1.step(env_1.vehicles, env_1.junctions)
            town_2.step(env_2.vehicles, env_2.junctions)

            town_1.update_state()
            town_2.update_state()

            town_1.render_map()
            town_2.render_map()

            current_step += 1

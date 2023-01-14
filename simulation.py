import pygame

from environment import GridWorldEnv
from gui.main_screen import MainScreen


if __name__ == '__main__':
    env = GridWorldEnv()

    # env.animate(500)
    ms = MainScreen(env.map)
    clock = pygame.time.Clock()

    max_step = 10
    current_step = 0
    running = True

    while running:
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if current_step <= max_step:

            env.step()
            ms.step(env.vehicles, env.junctions)
            ms.update_state()
            ms.render_map()

            if current_step % 10 == 9:
                env.change_random_lights()

        # if current_step == max_step:
        #     running = False
            current_step += 1

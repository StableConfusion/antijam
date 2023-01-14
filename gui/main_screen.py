import numpy as np
import pygame
import display_settings

from typing import List, Tuple

from gui.resource_manager import ResourceManager


class MainScreen:
    def __init__(self, town_map: np.ndarray, width: int, height: int):
        pygame.init()
        self.town_map = town_map
        self.map_height, self.map_width = self.town_map.shape
        self.width = width
        self.height = height
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))
        self.resource_manager = ResourceManager()
        self.clock = pygame.time.Clock()
        self.running = True

    def render_map(
            self,
            vehicles_state: List[Tuple],
            junctions_state: List[Tuple]
    ):
        for y in range(self.map_height):
            for x in range(self.map_width):
                if not self.town_map[y, x]:
                    self.screen.blit(self.resource_manager.grass_tile, (x * display_settings.DEFAULT_TILE_SIZE, y * display_settings.DEFAULT_TILE_SIZE))
                else:
                    self.screen.blit(self.resource_manager.soil_tile, (x * display_settings.DEFAULT_TILE_SIZE, y * display_settings.DEFAULT_TILE_SIZE))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.render_map(None, None)


if __name__ == '__main__':

    town_map = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    screen_height = town_map.shape[0] * display_settings.DEFAULT_TILE_SIZE
    screen_width = town_map.shape[1] * display_settings.DEFAULT_TILE_SIZE

    main_screen = MainScreen(
        town_map=town_map,
        width=screen_width,
        height=screen_height
    )

    main_screen.run()

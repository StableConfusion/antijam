import numpy as np
import pygame

from typing import List, Tuple

from gui.resource_manager import ResourceManager


class MainScreen:
    def __init__(self, map: np.ndarray, width: int, height: int):
        pygame.init()
        self.map = map
        self.map_height, self.map_width = map.shape
        self.width = width
        self.height = height
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))
        self.resource_manager = ResourceManager()
        self.running = True

    def render_map(
            self,
            vehicles_state: List[Tuple],
            junctions_state: List[Tuple]
    ):
        for y in range(self.map_height):
            for x in range(self.map_width):
                image = None

                if not self.map[y, x]:
                    image = self.resource_manager.grass_tile




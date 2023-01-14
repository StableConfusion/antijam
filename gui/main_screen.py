import numpy as np
import pygame
import display_settings

from typing import List, Tuple, Optional

from gui.resource_manager import ResourceManager, rotate_resize_car, rotate_road
from environment import Vehicle, Junction, Direction


class MainScreen:
    def __init__(self, town_map: np.ndarray, width: int, height: int):
        pygame.init()
        self.parse_town_map(town_map)
        self.map_height, self.map_width = town_map.shape
        self.width = width
        self.height = height

        self.screen: pygame.Surface = pygame.display.set_mode((width, height))
        self.resource_manager = ResourceManager()

        self.vehicle_state: Optional[List[Vehicle]] = None
        self.junction_state: Optional[List[Junction]] = None
        self.vehicle_state_tmp: Optional[List[Junction]] = None
        self.junction_state_tmp: Optional[List[Junction]] = None
        self.should_update = False

        self.clock = pygame.time.Clock()
        self.running = True

    def render_map(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.town_map[y][x] == "grass":
                    self.screen.blit(self.resource_manager.grass_tile, (x * display_settings.DEFAULT_TILE_SIZE, y * display_settings.DEFAULT_TILE_SIZE))
                else:
                    self.screen.blit(self.resource_manager.soil_tile, (x * display_settings.DEFAULT_TILE_SIZE, y * display_settings.DEFAULT_TILE_SIZE))
                    self.screen.blit(rotate_road(self.town_map[y][x], self.resource_manager),
                                     (x * display_settings.DEFAULT_TILE_SIZE, y * display_settings.DEFAULT_TILE_SIZE))
        if self.vehicle_state is not None:
            for vehicle in self.vehicle_state:
                y = vehicle.i
                x = vehicle.j

                self.screen.blit(rotate_resize_car(self.resource_manager.car_tiles[1], vehicle.direction),
                                 (x * display_settings.DEFAULT_TILE_SIZE, y * display_settings.DEFAULT_TILE_SIZE))

        if self.junction_state is not None:
            pass

        pygame.display.flip()

    def step(self, vehicle_state: List[Vehicle], junction_state: List[Junction]):
        self.vehicle_state_tmp = vehicle_state
        self.junction_state_tmp = junction_state
        self.should_update = True

    def update_state(self):
        if self.should_update:
            self.vehicle_state = self.vehicle_state_tmp.copy()
            self.junction_state = self.junction_state_tmp.copy()
            self.should_update = False

    def run(self):
        self.vehicle_state = [Vehicle(None, 1, 2, Direction.LEFT), Vehicle(None, 4, 7, Direction.UP)]

        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update_state()
            self.render_map()

    def parse_town_map(self, town_map: np.ndarray):
        self.town_map = [[None for _ in range(town_map.shape[1])] for _ in range(town_map.shape[0])]

        for y in range(town_map.shape[0]):
            for x in range(town_map.shape[1]):
                if not town_map[y, x]:
                    self.town_map[y][x] = "grass"
                else:
                    if not town_map[y-1][x] and not town_map[y-1][x-1] and not town_map[y][x-1]:
                        self.town_map[y][x] = "road_corner_right_down"
                    elif not town_map[y][x+1] and not town_map[y-1][x+1] and not town_map[y-1][x]:
                        self.town_map[y][x] = "road_corner_left_down"
                    elif not town_map[y+1][x] and not town_map[y+1][x+1] and not town_map[y][x+1]:
                        self.town_map[y][x] = "road_corner_left_up"
                    elif not town_map[y][x-1] and not town_map[y+1][x-1] and not town_map[y+1][x]:
                        self.town_map[y][x] = "road_corner_right_up"
                    elif (not town_map[y-1][x-1] and not town_map[y-1][x]) or (not town_map[y-1][x] and not town_map[y-1][x+1]):
                        self.town_map[y][x] = "road_corner_straight_right"
                    elif (not town_map[y-1][x+1] and not town_map[y][x+1]) or (not town_map[y][x+1] and not town_map[y+1][x+1]):
                        self.town_map[y][x] = "road_corner_straight_down"
                    elif (not town_map[y+1][x-1] and not town_map[y+1][x]) or (not town_map[y+1][x] and not town_map[y+1][x+1]):
                        self.town_map[y][x] = "road_corner_straight_left"
                    elif (not town_map[y-1][x-1] and not town_map[y][x-1]) or (not town_map[y][x-1] and not town_map[y+1][x-1]):
                        self.town_map[y][x] = "road_corner_straight_up"
                    elif not town_map[y+1][x+1]:
                        self.town_map[y][x] = "road_corner_right_down"
                    elif not town_map[y+1][x-1]:
                        self.town_map[y][x] = "road_corner_left_down"
                    elif not town_map[y-1][x-1]:
                        self.town_map[y][x] = "road_corner_left_up"
                    elif not town_map[y-1][x+1]:
                        self.town_map[y][x] = "road_corner_right_up"
                    else:
                        print(f"Error in parsing map! x = {x}, y = {y}")
                        exit(-1)
        print(self.town_map[2][6])


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

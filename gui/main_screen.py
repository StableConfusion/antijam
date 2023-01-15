import numpy as np
import pygame
from typing import List, Tuple, Optional

import gui.display_settings as display_settings
from gui.display_settings import set_tile_size, set_car_size
from gui.resource_manager import ResourceManager, rotate_resize_car, rotate_road
from commentary import Commentator


class MainScreen:
    def __init__(self, town_map: np.ndarray, verbose=0, is_commentator=False):
        pygame.init()
        pygame.display.set_caption('BITEhack Anti Jam')
        self.font = pygame.font.Font('freesansbold.ttf', 48)
        self.font_comment = pygame.font.Font('freesansbold.ttf', 25)

        set_tile_size(town_map.shape[0])
        set_car_size()

        screen_height = display_settings.DEFAULT_SCREEN_SIZE + 2 * display_settings.TILE_SIZE
        screen_width = display_settings.DEFAULT_SCREEN_SIZE + display_settings.TILE_SIZE

        self.parse_town_map(town_map)
        self.map_height, self.map_width = town_map.shape
        self.width = screen_width
        self.height = screen_height

        self.screen: pygame.Surface = pygame.display.set_mode((self.width * 2 + display_settings.TILE_SIZE, self.height))
        self.resource_manager = ResourceManager()

        self.is_commentator = is_commentator
        self.commentator = Commentator()
        self.commentator_cooldown = 50
        self.commentator_side = 0
        self.current_comment = ""

        self.verbose = verbose

    def render_prompts(self):
        if self.verbose:
            if self.commentator_cooldown > 0:
                if self.commentator_cooldown < 15:
                    if self.commentator_side == 0:
                        self.screen.blit(self.resource_manager.speech_bubble[2], (2 * display_settings.DEFAULT_SCREEN_SIZE - 64, display_settings.DEFAULT_SCREEN_SIZE - 300))
                    else:
                        self.screen.blit(self.resource_manager.speech_bubble[3], (64, display_settings.DEFAULT_SCREEN_SIZE - 300))

                if len(self.current_comment) > 0:
                    if self.commentator_side == 0:
                        self.screen.blit(self.resource_manager.speech_bubble[1], (40, display_settings.DEFAULT_SCREEN_SIZE - 330))
                        self.screen.blit(self.font_comment.render(self.current_comment, False, (0, 0, 0)), (100, display_settings.DEFAULT_SCREEN_SIZE - 265))
                    else:
                        self.screen.blit(self.resource_manager.speech_bubble[0], (2 * display_settings.DEFAULT_SCREEN_SIZE - 380, display_settings.DEFAULT_SCREEN_SIZE - 330))
                        self.screen.blit(self.font_comment.render(self.current_comment, False, (0, 0, 0)), (2 * display_settings.DEFAULT_SCREEN_SIZE - 335, display_settings.DEFAULT_SCREEN_SIZE - 265))

                self.commentator_cooldown -= 1
                return

            if self.is_commentator:
                speech = self.commentator.speak()
                if "Commentator1" in speech and "Commentator2" in speech:
                    speech = self.commentator.cut_commentator(speech)

                comment = ' '.join(speech.split(' ')[1:])
                self.current_comment = comment
                self.commentator_cooldown = 75
                self.commentator_side = not self.commentator_side
            else:
                speech = self.commentator.random_generated_comment(not self.commentator_side)
                self.current_comment = speech
                self.commentator_cooldown = 75
                self.commentator_side = not self.commentator_side

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


class Town:
    def __init__(self, screen: MainScreen, has_offset: bool):
        self.screen = screen
        self.screen_offset = 0
        if has_offset:
            self.screen_offset = display_settings.DEFAULT_SCREEN_SIZE + display_settings.TILE_SIZE

        self.vehicle_state: Optional[List] = None
        self.junction_state: Optional[List] = None
        self.vehicle_state_tmp: Optional[List] = None
        self.junction_state_tmp: Optional[List] = None
        self.mean_reward = 0.0
        self.mean_reward_tmp = 0.0
        self.should_update = False

    def render_map(self):
        for y in range(self.screen.map_height):
            for x in range(self.screen.map_width):
                self.screen.screen.blit(self.screen.resource_manager.grass_tile, (x * display_settings.TILE_SIZE + self.screen_offset, y * display_settings.TILE_SIZE))
                if self.screen.town_map[y][x] != "grass":
                    self.screen.screen.blit(rotate_road(self.screen.town_map[y][x], self.screen.resource_manager),
                                     (x * display_settings.TILE_SIZE + self.screen_offset, y * display_settings.TILE_SIZE))

        if self.junction_state is not None:
            for junction in self.junction_state:
                y = junction.i
                x = junction.j

                self.screen.screen.blit(self.screen.resource_manager.road_1_tiles[4],
                                 (x * display_settings.TILE_SIZE + self.screen_offset, y * display_settings.TILE_SIZE))

                offset = np.ceil(display_settings.TILE_SIZE * 0.05)
                line_width = np.ceil(display_settings.TILE_SIZE * 0.25)

                # state: 0 - horizontal, 1 - vertical
                if junction.state == 0:
                    pygame.draw.rect(self.screen.screen, (0, 200, 0),
                                     pygame.Rect(x * display_settings.TILE_SIZE + offset + self.screen_offset,
                                                 np.ceil((y + 0.75) * display_settings.TILE_SIZE), 2 * (display_settings.TILE_SIZE - offset), line_width))
                else:
                    pygame.draw.rect(self.screen.screen, (0, 200, 0),
                                     pygame.Rect(np.ceil((x + 0.75) * display_settings.TILE_SIZE) + self.screen_offset,
                                                 y * display_settings.TILE_SIZE + offset, line_width, 2 * (display_settings.TILE_SIZE - offset)))

        if self.vehicle_state is not None:
            for vehicle in self.vehicle_state:
                y = vehicle.i
                x = vehicle.j

                self.screen.screen.blit(rotate_resize_car(self.screen.resource_manager.car_tiles[1], vehicle.direction),
                                 (x * display_settings.TILE_SIZE + self.screen_offset, y * display_settings.TILE_SIZE))

        self.screen.screen.blit(self.screen.font.render("Mean reward {:.2f}".format(self.mean_reward), False, (255, 255, 255)), (250 + self.screen_offset, 50))

    def step(self, vehicle_state: List, junction_state: List, mean_reward: float):
        self.vehicle_state_tmp = vehicle_state
        self.junction_state_tmp = junction_state
        self.mean_reward_tmp = mean_reward
        self.should_update = True

    def update_state(self):
        if self.should_update:
            self.vehicle_state = self.vehicle_state_tmp
            self.junction_state = self.junction_state_tmp
            self.mean_reward = self.mean_reward_tmp
            self.should_update = False





from os import listdir, walk
from os.path import isfile, join

import numpy as np
import pygame

import display_settings
from environment import Direction


class TileSet:
    def __init__(self, file, size=(32, 32), margin=1, spacing=1):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'


class TileMap:
    def __init__(self, tile_set, size=(10, 20), rect=None):
        self.size = size
        self.tile_set = tile_set
        self.map = np.zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface((32*w, 32*h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tile_set.tiles[self.map[i, j]]
                self.image.blit(tile, (j*32, i*32))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        print(self.map)
        print(self.map.shape)
        self.render()

    def set_random(self):
        n = len(self.tile_set.tiles)
        self.map = np.random.randint(n, size=self.size)
        print(self.map)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'


def scale_2_tile_size(image):
    return pygame.transform.scale(image, (display_settings.DEFAULT_TILE_SIZE, display_settings.DEFAULT_TILE_SIZE))


def scale_2_car_size(image):
    return pygame.transform.scale(image, (display_settings.DEFAULT_CAR_WIDTH, display_settings.DEFAULT_TILE_SIZE))


def rotate_resize_car(image, direction: Direction):
    if direction == Direction.RIGHT:
        return pygame.transform.scale(pygame.transform.rotate(image, 270),
                                      (display_settings.DEFAULT_TILE_SIZE, display_settings.DEFAULT_CAR_WIDTH))
    elif direction == Direction.DOWN:
        return pygame.transform.rotate(image, 180)
    elif direction == Direction.LEFT:
        return pygame.transform.scale(pygame.transform.rotate(image, 90),
                                      (display_settings.DEFAULT_TILE_SIZE, display_settings.DEFAULT_CAR_WIDTH))
    else:
        return image


class ResourceManager:
    """
    Image set author: craftpix (Free Game Assets (GUI, Sprite, Tilesets)
    Site: https://free-game-assets.itch.io/free-race-track-tile-set?download
    """
    def __init__(self):
        resource_path_road_1 = r"../resource/road_1"
        resource_path_road_2 = r"../resource/road_2"
        resource_path_background = r"../resource/background_tiles"
        resource_path_car = r"../resource/car"

        # Road_1 Tiles
        self.road_1_tiles = []
        for tile_image in [f for f in listdir(resource_path_road_1) if isfile(join(resource_path_road_1, f))]:
            self.road_1_tiles.append(scale_2_tile_size(pygame.image.load(join(resource_path_road_1, tile_image))))

        self.road_1_tiles[0] = pygame.transform.scale(self.road_1_tiles[0], (display_settings.DEFAULT_TILE_SIZE + 5, display_settings.DEFAULT_TILE_SIZE + 5))
        self.road_1_tiles[1] = pygame.transform.scale(self.road_1_tiles[1], (display_settings.DEFAULT_TILE_SIZE + 5, display_settings.DEFAULT_TILE_SIZE + 5))

        # Road 2 Tiles
        self.road_2_tiles = []
        for tile_image in [f for f in listdir(resource_path_road_2) if isfile(join(resource_path_road_2, f))]:
            self.road_2_tiles.append(scale_2_tile_size(pygame.image.load(join(resource_path_road_2, tile_image))))

        self.road_2_tiles[0] = pygame.transform.scale(self.road_2_tiles[0], (display_settings.DEFAULT_TILE_SIZE + 5, display_settings.DEFAULT_TILE_SIZE + 5))
        self.road_2_tiles[1] = pygame.transform.scale(self.road_2_tiles[1], (display_settings.DEFAULT_TILE_SIZE + 5, display_settings.DEFAULT_TILE_SIZE + 5))

        # Background Tiles
        self.grass_tile = scale_2_tile_size(pygame.image.load(join(resource_path_background, "grass.png")))
        self.soil_tile = scale_2_tile_size(pygame.image.load(join(resource_path_background, "soil.png")))
        self.water_tile = scale_2_tile_size(pygame.image.load(join(resource_path_background, "water.png")))

        # Car Tiles
        self.car_tiles = []
        for tile_image in [f for f in listdir(resource_path_car) if isfile(join(resource_path_car, f))]:
            self.car_tiles.append(scale_2_car_size(pygame.image.load(join(resource_path_car, tile_image))))


def rotate_road(road_type, resource_manager: ResourceManager):
    """
    :param image: image to rotate
    :param road_type: type of road tile
    :param resource_manager: instance of ResourceManager
    :return: rotated image
    """

    if road_type == "road_corner_right_down":
        return resource_manager.road_1_tiles[1]
    elif road_type == "road_corner_left_down":
        return pygame.transform.rotate(resource_manager.road_1_tiles[1], -90)
    elif road_type == "road_corner_left_up":
        return pygame.transform.rotate(resource_manager.road_1_tiles[0], -270)
    elif road_type == "road_corner_right_up":
        return resource_manager.road_1_tiles[0]
    elif road_type == "road_corner_straight_right":
        return resource_manager.road_1_tiles[2]
    elif road_type == "road_corner_straight_down":
        return pygame.transform.rotate(resource_manager.road_1_tiles[2], 90)
    elif road_type == "road_corner_straight_left":
        return resource_manager.road_1_tiles[2]
    elif road_type == "road_corner_straight_up":
        return pygame.transform.rotate(resource_manager.road_1_tiles[2], 90)
    else:
        raise ValueError

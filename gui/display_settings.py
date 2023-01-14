from numpy import ceil

DEFAULT_TILE_SIZE = 64
DEFAULT_CAR_WIDTH = 48

DEFAULT_SCREEN_SIZE = 800

TILE_SIZE = DEFAULT_TILE_SIZE
CAR_WIDTH = DEFAULT_CAR_WIDTH


def set_tile_size(town_size: int):
    global TILE_SIZE
    TILE_SIZE = ceil(DEFAULT_SCREEN_SIZE / town_size)


def set_car_size():
    global CAR_WIDTH
    CAR_WIDTH = ceil(CAR_WIDTH * (TILE_SIZE / DEFAULT_TILE_SIZE))

import gym
from gym import spaces
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from enum import Enum


class Direction(Enum):
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP = (-1, 0)


class GridWorldEnv:
    def __init__(self, render_mode=None):
        self.map = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])

        n, m = self.map.shape

        self.map_obs = self.map[self.map >= 1]

        self.vehicles = [
            Vehicle(self, 1, 1, Direction.DOWN),
            Vehicle(self, 5, 1, Direction.DOWN),
        ]

        # Top left corner of junction
        self.junctions = [
            Junction(1, 8),
            Junction(9, 8)
        ]

        # Pseudjunctions
        self.corner_roads = {
            (1, 1): Direction.DOWN,
            (2, 2): Direction.RIGHT,
            (n-2, 1): Direction.RIGHT,
            (n-3, 2): Direction.UP,
            (n-2, m-2): Direction.UP,
            (n-3, m-3): Direction.LEFT,
            (1, m-2): Direction.LEFT,
            (2, m-3): Direction.DOWN
        }

        self.render()
        for i in range(20):
            self.step()
            self.render()

    def step(self):
        for vehicle in self.vehicles:
            vehicle.move()

    def render(self):
        temp = deepcopy(self.map)

        for vehicle in self.vehicles:
            temp[vehicle.i, vehicle.j] = 3

        plt.matshow(temp)
        plt.show()


class Junction:
    def __init__(self, top_i, top_j, state=0):
        self.i = top_i
        self.j = top_j
        # 0 - left / right, 1 - up / down
        self.state = state

    def is_in_junction(self, i, j):
        return self.i <= i <= self.i + 1 and self.j <= j <= self.j + 1


class Vehicle:
    def __init__(self, world: GridWorldEnv, i: int, j: int, start_direction: Direction) -> None:
        self.i = i
        self.j = j
        self.world = world

        self.direction = start_direction

    def move(self):
        self.find_direction()
        next_i, next_j = self.i + self.direction.value[0], self.j + self.direction.value[1]

        # Other vehicles
        for vehicle in self.world.vehicles:
            if vehicle.i == next_i and vehicle.j == next_j:
                return

        # Junctions
        for junction in self.world.junctions:
            if not junction.is_in_junction(next_i, next_j): continue

            if junction.state == 0:
                if self.direction not in [Direction.LEFT, Direction.RIGHT]:
                    return
            else:
                if self.direction not in [Direction.DOWN, Direction.UP]:
                    return
        # Road
        if self.world.map[next_i, next_j] == 1:
            self.i, self.j = next_i, next_j

    def find_direction(self):
        for i1, j1 in self.world.corner_roads:
            if self.i == i1 and self.j == j1:
                self.direction = self.world.corner_roads[(i1, j1)]


if __name__ == '__main__':
    env = GridWorldEnv()
    env.step()


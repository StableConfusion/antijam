from __future__ import annotations
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from enum import Enum

from matplotlib import animation
from matplotlib.animation import FuncAnimation


class Direction(Enum):
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP = (-1, 0)

    def is_left_turn(self, other: Direction):
        return [self, other] in [
            [Direction.UP, Direction.LEFT],
            [Direction.LEFT, Direction.DOWN],
            [Direction.DOWN, Direction.RIGHT],
            [Direction.RIGHT, Direction.UP]
        ]


def opposite(direction: Direction):
    return {
        Direction.RIGHT: Direction.LEFT,
        Direction.DOWN: Direction.UP,
        Direction.LEFT: Direction.RIGHT,
        Direction.UP: Direction.DOWN
    }[direction]

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
        self.day = 0

        self.map_obs = self.map[self.map >= 1]

        self.vehicles = [
            Vehicle(self, 10, 5, Direction.RIGHT),
            Vehicle(self, 9, 15, Direction.LEFT),
            Vehicle(self, 9, 14, Direction.LEFT),
            Vehicle(self, 9, 13, Direction.LEFT),
            Vehicle(self, 9, 12, Direction.LEFT),
            Vehicle(self, 1, 14, Direction.LEFT),
            Vehicle(self, 10, 7, Direction.RIGHT),
            Vehicle(self, 4, 8, Direction.DOWN),
            Vehicle(self, 4, 9, Direction.UP),
            Vehicle(self, 5, 9, Direction.UP),
            Vehicle(self, 6, 9, Direction.UP),
            Vehicle(self, 7, 9, Direction.UP),
        ]

        # Top left corner of junction
        self.junctions = [
            Junction(1, 8, [(1, Direction.LEFT), (1, Direction.RIGHT), (1, Direction.DOWN)], 1),
            Junction(9, 8, [(1, Direction.LEFT), (1, Direction.RIGHT), (1, Direction.UP)]),
            # Junction(9, 8, [(1, Direction.LEFT), (1, Direction.UP)]),
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

    def step(self) -> int:
        """
        Makes simulation and returns how many vehicles were moved
        :return: reward
        """
        self.day += 1
        vehicles_moved = 0
        for vehicle in self.vehicles:
            if vehicle.move():
                vehicles_moved += 1
        return vehicles_moved

    def change_random_lights(self):
        for junction in self.junctions:
            junction.state = np.random.randint(0, 2)

    def render(self):
        temp = deepcopy(self.map)
        self.render_junctions(temp)
        for vehicle in self.vehicles:
            temp[vehicle.i, vehicle.j] = 5

        plt.matshow(temp)
        plt.show()

    def render_junctions(self, map_to_edit):
        for junction in self.junctions:
            map_to_edit[junction.i:junction.i+2, junction.j:junction.j+2] = 3 + junction.state

    def animate(self, n=1000):
        fig, ax = plt.subplots()

        ims = []
        for i in range(n):
            self.step()
            temp = deepcopy(self.map)
            self.render_junctions(temp)
            for vehicle in self.vehicles:
                temp[vehicle.i, vehicle.j] = 5
            im = ax.imshow(temp, animated=True)
            if i == 0:
                ax.imshow(temp)
            if self.day % 10 == 0:
                self.change_random_lights()
            ims.append([im])

        ani = animation.ArtistAnimation(fig, ims, interval=200, blit=True,
                                        repeat_delay=1000)

        plt.show()


class Junction:
    def __init__(self, top_i, top_j, valid_turns, state=0):
        self.i = top_i
        self.j = top_j
        # 0 - left / right, 1 - up / down
        self.valid_turns = valid_turns
        self.state = state

    def is_in_junction(self, i, j):
        return self.i <= i <= self.i + 1 and self.j <= j <= self.j + 1

    def get_random_turn(self, from_direction):
        valid_turns = [turn for turn in self.valid_turns if turn[1] != opposite(from_direction)]
        total = sum([turn[0] for turn in valid_turns])
        return np.random.choice(list(map(lambda x: x[1], valid_turns)), p=[turn[0]/total for turn in valid_turns])


class Vehicle:
    def __init__(self, world: GridWorldEnv, i: int, j: int, start_direction: Direction) -> None:
        self.world = world
        self.i = i
        self.j = j

        self.direction = start_direction
        self.temp_direction = None

    def move(self):
        self.find_direction()
        temp_direction = self.direction.value

        if self.temp_direction is not None:
            if self.direction.is_left_turn(self.temp_direction):
                temp_direction = self.direction.value[0] + self.temp_direction.value[0], self.direction.value[1] + self.temp_direction.value[1]
            else:
                temp_direction = self.temp_direction.value

        next_i, next_j = self.i + temp_direction[0], self.j + temp_direction[1]

        # Other vehicles
        for vehicle in self.world.vehicles:
            if vehicle.i == next_i and vehicle.j == next_j:
                return False

        # On the junction
        is_in_junction = False
        for junction in self.world.junctions:
            if junction.is_in_junction(self.i, self.j):
                is_in_junction = True

        # Want to entry junctions
        if not is_in_junction:
            for junction in self.world.junctions:
                if not junction.is_in_junction(next_i, next_j): continue

                if junction.state == 0:
                    if self.direction not in [Direction.LEFT, Direction.RIGHT]:
                        return False
                else:
                    if self.direction not in [Direction.DOWN, Direction.UP]:
                        return False

                if self.temp_direction is None:
                    self.temp_direction = junction.get_random_turn(self.direction)
        else:
            if self.temp_direction is not None:
                self.direction = self.temp_direction
                self.temp_direction = None

        # Road
        assert self.world.map[next_i, next_j] >= 1

        self.i, self.j = next_i, next_j
        return True

    def find_direction(self):
        for i1, j1 in self.world.corner_roads:
            if self.i == i1 and self.j == j1:
                self.direction = self.world.corner_roads[(i1, j1)]

    def __repr__(self):
        return f"Vehicle({self.i}, {self.j}, {self.direction})"


if __name__ == '__main__':
    env = GridWorldEnv()
    # for i in range(30):
    #     print(env.step())
    #     env.render()
    #     if i % 10 == 9:
    #         env.change_random_lights()
    # env.animate(500)


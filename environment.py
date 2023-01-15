from __future__ import annotations
import numpy as np
from copy import deepcopy
from typing import List
import matplotlib.pyplot as plt
from enum import Enum
from gui.main_screen import MainScreen

from matplotlib import animation
from matplotlib.animation import FuncAnimation
from utils import Direction, opposite


JUNCTION_COOLDOWN = 5


class GridWorldEnv:
    def __init__(self, render_mode=None, map_size=42, num_of_vehicles=80):
        self.map, self.junctions = self.generate_map(map_size, map_size, 3, 3)

        n, m = self.map.shape
        self.day = 0

        # self.map_obs = self.map[self.map >= 1]

        self.vehicles = self.generate_vehicles(num_of_vehicles)
        # self.vehicles = [
        #     Vehicle(self, 1, 10, Direction.LEFT),
        # ]

        # Pseudjunctions
        self.corner_roads = {
            (1, 1): Direction.DOWN,
            (2, 2): Direction.RIGHT,
            (n - 2, 1): Direction.RIGHT,
            (n - 3, 2): Direction.UP,

            (n - 2, m - 2): Direction.UP,
            (n - 3, m - 3): Direction.LEFT,
            (1, m - 2): Direction.LEFT,
            (2, m - 3): Direction.DOWN
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
        for junction in self.junctions:
            junction.unblock()
        for vehicle in self.vehicles:
            vehicle.unswap()
        return vehicles_moved

    def change_random_lights(self):
        for junction in self.junctions:
            junction.set_state(np.random.randint(0, 2))

    def render(self):
        temp = deepcopy(self.map)
        self.render_junctions(temp)
        for vehicle in self.vehicles:
            temp[vehicle.i, vehicle.j] = 5

        plt.matshow(temp)
        plt.show()

    @staticmethod
    def generate_map(i: int, j: int, hor_jun: int, ver_jun: int) -> tuple[np.ndarray, np.ndarray]:
        new_map = np.zeros((i, j))
        junctions = []

        # Edge roads
        new_map[1:3, 1:-1] = 1
        new_map[-3:-1, 1:-1] = 1
        new_map[1:-1, 1:3] = 1
        new_map[1:-1, -3:-1] = 1

        hor_jun_loc = list(np.linspace(1, i - 3, hor_jun + 2, dtype=int)[1:-1])
        ver_jun_loc = list(np.linspace(1, j - 3, ver_jun + 2, dtype=int)[1:-1])

        # 3 prio roads
        new_map[hor_jun_loc[len(hor_jun_loc) // 2]:hor_jun_loc[len(hor_jun_loc) // 2] + 2, 1:-1] = 3
        new_map[1:-1, ver_jun_loc[len(ver_jun_loc) // 2]:ver_jun_loc[len(ver_jun_loc) // 2] + 2] = 3

        # 2-prio roads
        new_map[hor_jun_loc[len(hor_jun_loc) // 4]:hor_jun_loc[len(hor_jun_loc) // 4] + 2, 1:-1] = 2
        new_map[hor_jun_loc[3 * len(hor_jun_loc) // 4]:hor_jun_loc[3 * len(hor_jun_loc) // 4] + 2, 1:-1] = 2
        new_map[1:-1, ver_jun_loc[len(ver_jun_loc) // 4]:ver_jun_loc[len(ver_jun_loc) // 4] + 2] = 2
        new_map[1:-1, ver_jun_loc[3 * len(ver_jun_loc) // 4]:ver_jun_loc[3 * len(ver_jun_loc) // 4] + 2] = 2

        # 1-prio roads
        for hor_loc in hor_jun_loc:
            if hor_loc not in [hor_jun_loc[len(hor_jun_loc) // 2], hor_jun_loc[len(hor_jun_loc) // 4],
                               hor_jun_loc[3 * len(hor_jun_loc) // 4]]:
                new_map[hor_loc:hor_loc + 2, 1:-1] = 1
        for ver_loc in ver_jun_loc:
            if ver_loc not in [ver_jun_loc[len(ver_jun_loc) // 2], ver_jun_loc[len(ver_jun_loc) // 4],
                               ver_jun_loc[3 * len(ver_jun_loc) // 4]]:
                new_map[1:-1, ver_loc:ver_loc + 2] = 1

        hor_jun_loc = list(np.linspace(1, i - 3, hor_jun + 2, dtype=int))
        ver_jun_loc = list(np.linspace(1, j - 3, ver_jun + 2, dtype=int))

        for hor_loc in hor_jun_loc:
            for ver_loc in ver_jun_loc:
                up_prio = -1
                down_prio = -1
                left_prio = -1
                right_prio = -1
                if not hor_loc == 1:
                    up_prio = new_map[hor_loc - 1, ver_loc]
                if not hor_loc == i - 3:
                    down_prio = new_map[hor_loc + 2, ver_loc]
                if not ver_loc == 1:
                    left_prio = new_map[hor_loc, ver_loc - 1]
                if not ver_loc == j - 3:
                    right_prio = new_map[hor_loc, ver_loc + 2]

                negative = [up_prio, down_prio, left_prio, right_prio].count(-1)
                if negative == 2:
                    continue

                prios = []
                if up_prio != -1:
                    prios.append((up_prio, Direction.UP))
                if down_prio != -1:
                    prios.append((down_prio, Direction.DOWN))
                if left_prio != -1:
                    prios.append((left_prio, Direction.LEFT))
                if right_prio != -1:
                    prios.append((right_prio, Direction.RIGHT))
                junctions.append(Junction(hor_loc, ver_loc, prios))

        return new_map, junctions

    def generate_vehicles(self, n: int) -> List[Vehicle]:
        veh_list = []
        road_tiles = list(zip(*np.nonzero(self.map)))
        indices = np.random.choice(len(road_tiles), n, replace=False)
        road_tiles = [road_tiles[k] for k in indices]

        for i in range(n):
            direction = None
            if self.map[road_tiles[i][0], road_tiles[i][1] - 1] == 0:
                direction = Direction.DOWN
            elif self.map[road_tiles[i][0], road_tiles[i][1] + 1] == 0:
                direction = Direction.UP
            elif self.map[road_tiles[i][0] - 1, road_tiles[i][1]] == 0:
                direction = Direction.LEFT
            elif self.map[road_tiles[i][0] + 1, road_tiles[i][1]] == 0:
                direction = Direction.RIGHT
            # if it's on junction
            elif road_tiles[i][0] == 2:
                direction = Direction.RIGHT
            elif road_tiles[i][0] == self.map.shape[0] - 3:
                direction = Direction.LEFT
            elif self.map[
                road_tiles[i][0] + 1, road_tiles[i][1] + 1] == 0 or self.map[
                road_tiles[i][0] - 1, road_tiles[i][1] + 1] == 0:
                direction = Direction.UP
            elif self.map[
                road_tiles[i][0] - 1, road_tiles[i][1] - 1] == 0 or self.map[
                road_tiles[i][0] + 1, road_tiles[i][1] - 1] == 0:
                direction = Direction.DOWN
            assert direction is not None
            veh_list.append(Vehicle(self, road_tiles[i][0], road_tiles[i][1], direction))
        return veh_list

    def render_junctions(self, map_to_edit):
        for junction in self.junctions:
            map_to_edit[junction.i:junction.i + 2, junction.j:junction.j + 2] = -2 + junction.state

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

        ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                        repeat_delay=1000)

        plt.show()


class Junction:
    def __init__(self, top_i, top_j, valid_turns, state=0):
        self.i = top_i
        self.j = top_j
        # 0 - left / right, 1 - up / down
        self.valid_turns = valid_turns
        self.state = state
        # yellow light
        self.is_blocked = False
        self.cooldown = 0

    def is_in_junction(self, i, j):
        return self.i <= i <= self.i + 1 and self.j <= j <= self.j + 1

    def get_random_turn(self, from_direction):
        valid_turns = [turn for turn in self.valid_turns if turn[1] != opposite(from_direction)]
        total = sum([turn[0] for turn in valid_turns])
        return np.random.choice(list(map(lambda x: x[1], valid_turns)), p=[turn[0] / total for turn in valid_turns])

    def set_state(self, new_state):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        if new_state ^ self.state == 0:
            return
        self.is_blocked = True
        self.state = new_state
        self.cooldown = JUNCTION_COOLDOWN

    def unblock(self):
        self.is_blocked = False


class Vehicle:
    def __init__(self, world: GridWorldEnv, i: int, j: int, start_direction: Direction) -> None:
        self.world = world
        self.i = i
        self.j = j

        self.direction = start_direction
        self.temp_direction = None
        self.swapped = False

    def move(self):
        self.find_direction()

        if self.swapped: return True

        temp_direction = self.direction.value

        if self.temp_direction is not None:
            temp_direction = self.direction.value[0] + self.temp_direction.value[0], \
                             self.direction.value[1] + self.temp_direction.value[1]

        next_i, next_j = self.i + temp_direction[0], self.j + temp_direction[1]

        # Other vehicles
        for vehicle in self.world.vehicles:
            if vehicle.i == next_i and vehicle.j == next_j:
                if self.temp_direction is not None and vehicle.temp_direction is not None:
                    self.i, self.j, vehicle.i, vehicle.j = vehicle.i, vehicle.j, self.i, self.j
                    vehicle.swapped = True
                    self.swapped = True
                    self.direction = self.temp_direction
                    vehicle.direction = vehicle.temp_direction
                    self.temp_direction = None
                    vehicle.temp_direction = None
                    return True
                else:
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

                if junction.is_blocked: return False

                if junction.state == 0:
                    if self.direction not in [Direction.LEFT, Direction.RIGHT]:
                        return False
                else:
                    if self.direction not in [Direction.DOWN, Direction.UP]:
                        return False

                if self.temp_direction is None:
                    temp_direction = junction.get_random_turn(self.direction)
                    if self.direction.is_left_turn(temp_direction):
                        self.temp_direction = temp_direction
                    else:
                        self.direction = temp_direction
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

    def unswap(self):
        self.swapped = False

    def __repr__(self):
        return f"Vehicle({self.i}, {self.j}, {self.direction})"



if __name__ == '__main__':
    env = GridWorldEnv()

    env.animate(500)
    # ms = MainScreen(env.map)
    # for i in range(3):
    #     env.step()
    #     env.render()
    #     # ms.step(env.vehicles, env.junctions)
    #     if i % 10 == 9:
    #         env.change_random_lights()

    # env.map > 0
    # env.render()


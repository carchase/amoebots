'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Oct 11, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

import math

class Grid:
    """
    The world model representation of the webots arena. The purpose of the world model
    is to represent the world in a way the AI level can understand and process.
    """

    def __init__(self, arena_size, arena_size_cm):
        self.width = arena_size
        self.height = arena_size
        self.tiles_per_cm = arena_size / arena_size_cm
        self.grid = [[]]
        self.robots = []

        for i in range(self.width):
            self.grid.append([])
            for j in range(self.height):
                self.grid[i].append(Tile(i, j, self.tiles_per_cm))

    def in_bounds(self, position):
        return 0 <= position[0] < self.width and 0 <= position[1] < self.height

    def occupied(self, tile):
        return tile.occupied

    def neighbors(self, tile):
        (x, y) = tile.position
        coords = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        coords = filter(self.in_bounds, coords)
        coords = filter(self.occupied, coords)
        results = []
        for coord in coords:
            results.append(self.grid[coord[0]][coord[1]])
        return results

    def get_tile(self, position):
        if self.in_bounds(position):
            return self.grid[int(position[0] * self.tiles_per_cm)][int(position[1] * self.tiles_per_cm)]
        else:
            return None

class Robot:
    """
    Representation of a robot in the world model. Each robot has a real position and heading,
    and a tile it is occupying on the world space grid.
    """
    def __init__(self, robot_id):
        self.robot_id = robot_id
        self.position = None
        self.heading = None
    #     self.grid = grid
    #     self.tile = grid.get_tile(x, y)

    # def move(self, new_position):
    #     self.tile.occupied = None
    #     self.position = new_position
    #     self.tile = self.grid[int(self.position.x * 100),
    #                           int(self.position.y * 100)]
    #                           # convert meters to centimeters then align to grid
    #     self.tile.occupied = self

    def get_distance(self, old_position, new_position):
        return math.sqrt((new_position[0] - old_position[0]) ** 2 +
                         (new_position[1] - old_position[1]) ** 2)

    def get_angle(self, old_position, new_position):
        # calculate slope of line between old and new positions
        rise = (new_position[0] - old_position[0])
        run = (new_position[1] - old_position[1])

        # calculate angle between line and robot heading
        return math.atan2(rise, run)

class Tile:
    def __init__(self, x, y, tiles_per_cm):
        self.occupied = None   # is a Robot if tile is occupied by that robot
        self.goal = False
        self.position = (x, y)
        self.center = (self.position[0] / tiles_per_cm, self.position[1] / tiles_per_cm)

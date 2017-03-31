'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Oct 11, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

import math

ARENA_SIZE = 7
TILES_PER_CM = 0.12337143

class Grid:
    """
    The world model representation of the webots arena. The purpose of the world model
    is to represent the world in a way the AI level can understand and process.
    """

    def __init__(self):
        self.width = ARENA_SIZE
        self.height = ARENA_SIZE
        self.grid = [[]]
        self.robots = []

        for i in range(self.width):
            for j in range(self.height):
                self.grid[i][j] = Tile(i, j)

    def in_bounds(self, position):
        return 0 <= position.x < self.width and 0 <= position.y < self.height

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
            return self.grid[int(position.x * TILES_PER_CM)][int(position.y * TILES_PER_CM)]
        else:
            return None

class Robot:
    """
    Representation of a robot in the world model. Each robot has a real position and heading,
    and a tile it is occupying on the world space grid.
    """
    def __init__(self, grid, x, y):
        self.position = None
        self.heading = None
        self.grid = grid
        self.tile = grid.get_tile(x, y)

    def move(self, new_position):
        self.tile.occupied = False
        self.position = new_position
        self.tile = self.grid[int(self.position.x * 100),
                              int(self.position.y * 100)]
                              # convert meters to centimeters then align to grid
        self.tile.occupied = True

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
    def __init__(self, x, y):
        self.occupied = False
        self.goal = False
        self.position = (x, y)
        self.center = (self.position[0] / TILES_PER_CM, self.position[1] / TILES_PER_CM)

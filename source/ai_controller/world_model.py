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

    arena_size = 7
    cmPerTile = 0.12337143

    def __init__(self):
        self.width = arena_size
        self.height = arena_size
        self.grid = [[]]
        self.robots = []

        for i in range(self.width):
            for j in range(self.height):
                grid[i][j] = Tile(i, j)
    
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
            results.append(grid[coord[0]][coord[1]])
        return results

    def get_tile(self, position):
        if in_bounds(position):
            return grid[int(position.x / cmPerTile)][int(position.y / cmPerTile)]
        else:
            return None

class Robot:
    def __init__(self, tile):
        self.position = None
        self.heading = None
        self.tile = tile

    def move(new_position):
        self.tile.occupied = False
        self.position = new_position
        self.tile = grid[int(position.x * 100), int(position.y * 100)] # convert meters to centimeters then align to grid
        self.tile.occupied = True

    def calc(old_position, new_position):
        # calcualte distance between old and new positions
        distance = math.sqrt( (new_position[0] - old_position[0]) ** 2 + (new_position[1] - old_position[1]) ** 2 )

        # calculate slope of line between old and new positions

        # calculate angle between line and robot heading

class Tile:
    def __init__(self, x, y):
        self.occupied = False
        self.goal = False
        self.position = (x, y)
        self.center = (self.position.x * cmPerTile, self.position.y * cmPerTile)

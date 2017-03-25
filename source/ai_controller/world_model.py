'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Oct 11, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

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

        for i in range(0 to self.width):
            for j in range(0 to self.height):
                grid[i][j] = Tile(i, j)
    
    def in_bounds(self, tile):
        (x, y) = tile
        return 0 <= x < self.width and 0 <= y < self.height
    
    def neighbors(self, tile):
        (x, y) = tile.position
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        results = filter(self.in_bounds, results)
        return results

class Robot:
    self.position = None
    self.heading = None

    def move(new_position):
        self.position = new_position
        grid[position.x, position.y].occupied = True

class Tile:
    __init__(self, x, y):
        self.occupied = False
        self.position = (x, y)

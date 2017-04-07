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

    def __init__(self, arena_size, arena_size_cm):
        self.width = arena_size
        self.height = arena_size
        self.width_cm = arena_size_cm
        self.height_cm = arena_size_cm
        self.cm_per_tile = float(arena_size_cm) / float(arena_size)
        self.grid = []
        self.robots = []

        for i in range(self.height):
            self.grid.append([])
            for j in range(self.width):
                self.grid[i].append(Tile(i, j, self.cm_per_tile))

    def in_bounds(self, position):
        """
        Determine if a position is in or out of bounds
        """
        print( position)
        return 0 <= position[0] < self.width and 0 <= position[1] < self.height

    def in_bounds_real_coords(self, coordinates):
        """
        Determine if the cm coordinates are in in_bounds
        """
        return 0 <= coordinates[0] < self.width_cm and 0 <= coordinates[1] < self.height_cm

    def neighbors(self, tile):
        """
        Get all neighbors of a given tile
        """
        (x_cor, y_cor) = tile.position
        coords = [(x_cor+1, y_cor), (x_cor, y_cor-1), (x_cor-1, y_cor), (x_cor, y_cor+1)]
        coords = filter(self.in_bounds, coords)
        results = []
        for coord in coords:
            results.append(self.grid[coord[0]][coord[1]])
        return results

    def get_tile_real_coords(self, coordinates):
        """
        Get the tile that contains the real world position cm coordinates.
        """
        if self.in_bounds_real_coords(coordinates):
            return self.grid[
                round(coordinates[0] / self.cm_per_tile)][
                    round(coordinates[1] / self.cm_per_tile)]
        else:
            return None

    def find_tile(self, robot):
        for row in self.grid:
            for tile in row:
                if tile.occupied is robot:
                    return tile
        return None

class Robot:
    """
    Representation of a robot in the world model. Each robot has a real position and heading,
    and a tile it is occupying on the world space grid.
    """
    def __init__(self, robot_id, port_id, robot_type):
        self.robot_id = robot_id
        self.port_id = port_id
        self.robot_type = robot_type
        self.position = (0, 0)
        self.heading = 0

class Sensor:
    def __init__(self, sensor_id, port_id, sensor_type):
        self.sensor_id = sensor_id
        self.port_id = port_id
        self.sensor_type = sensor_type
        self.asked = False
        self.received = False

class Tile:
    """
    The world model representation of an individual tile in the world model grid.
    Each tile can contain up to one robot and one goal.
    """
    def __init__(self, x, y, cm_per_tile):
        self.occupied = None   # is a Robot if tile is occupied by that robot
        self.goal = False
        self.robot_goal = None
        self.position = (x, y)
        self.center = ((x + 0.5) * cm_per_tile, (y + 0.5) * cm_per_tile)

'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Oct 11, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

class Arena:
    """
    The world model representation of the webots arena. The purpose of the world model
    is to represent the world in a way the AI level can understand and process.

    Args:
        arena_size (int): The size of the arena in tiles (ex: 5 for a 5x5 grid arena)
        arena_size_cm (double): The actual physical size of the arena in cm
        goal_positions (list): A list of the goal position tuples

    Attributes:
        width (int): The width of the arena in tiles
        height (int): The height of the arena in tiles
        width (float): The width of the arena in cm
        height (float): The width of the arena in cm
        cm_per_tile (float): The conversion factor between the size of a tile and cm
        grid (Tile[]): The world model grid, a self.width x self.height array of Tiles
    """

    def __init__(self, arena_size, arena_size_cm, goal_positions):
        self.width = arena_size
        self.height = arena_size
        self.width_cm = arena_size_cm
        self.height_cm = arena_size_cm
        self.cm_per_tile = float(arena_size_cm) / float(arena_size)
        self.grid = []

        for row in range(self.height):
            self.grid.append([])
            for col in range(self.width):
                self.grid[row].append(Tile(col, row, self.cm_per_tile))

        # Set the goals
        for goal in goal_positions:
            self.grid[goal[1]][goal[0]].goal = True

    def in_bounds(self, position):
        """
        Determine if a position is in or out of bounds

        Args:
            position (Tuple): The grid position to check against the world model grid
        """
        return 0 <= position[0] < self.width and 0 <= position[1] < self.height

    def in_bounds_real_coords(self, coordinates):
        """
        Determine if the cm coordinates are in in_bounds

        Args:
            coordinates (Tuple): The real coordinates to check against the world model grid
        """
        return 0 <= coordinates[0] < self.width_cm and 0 <= coordinates[1] < self.height_cm

    def neighbors(self, tile):
        """
        Get all neighbors of a given tile

        Args:
            tile (Tile): The tile whose neighbors to find
        """
        (x_cor, y_cor) = tile.position
        coords = [(x_cor+1, y_cor), (x_cor, y_cor-1), (x_cor-1, y_cor), (x_cor, y_cor+1)]
        coords = filter(self.in_bounds, coords)
        results = []
        for coord in coords:
            results.append(self.grid[coord[1]][coord[0]])
        return results

    def get_tile_real_coords(self, coordinates):
        """
        Get the tile that contains the real world position cm coordinates.

        Args:
            coordinates (Tuple): The real coordinates to check against the world model grid
        """
        if self.in_bounds_real_coords(coordinates):
            return self.grid[
                int(coordinates[1] / self.cm_per_tile)][
                    int(coordinates[0] / self.cm_per_tile)]
        else:
            return None

    def find_tile(self, robot):
        """
        Finds the tile containing the given robot. Returns None if the robot
        does not have a tile (can happen if multiple robots are trying to
        occupy the same tile).

        Args:
            robot (Robot): The robot to search the grid for.
        """
        for row in self.grid:
            for tile in row:
                if tile.occupied is robot:
                    return tile
        return None

    def find_robot_goal(self, robot):
        """
        Finds the goal for a given robot.

        Args:
            robot (Robot): The robot whose goal to search for
        """

        for row in self.grid:
            for tile in row:
                if tile.robot_goal is robot:
                    return tile
        return None

    def to_string(self):
        """
        Generates the state of the world as a string. "o" tiles are open, "g" tiles are goals,
        "r" tiles are robots, and "R" tiles are robots that are on goals.
        """
        line = ""
        for row in self.grid:
            for tile in row:
                if tile.occupied != None and tile.goal:
                    line += "R "
                elif tile.occupied != None:
                    line += "r "
                elif tile.goal:
                    line += "g "
                else:
                    line += "o "
            line += "\n"

        return line

class Robot:
    """
    Representation of a robot in the world model. Each robot has a real position and heading,
    and can be either simulator or real robots.

    Args:
        robot_id (int): The number used to identify the robot
        port_id (int): The COM port used to communicate with the robot
        robot_type (string): The type of robot, either a simulator SMORES or a real SMORES

    Attributes:
        robot_id (int): The number used to identify the robot
        port_id (int): The COM port used to communicate with the robot
        robot_type (string): The type of robot, either a simulator SMORES or a real SMORES
        position (Tuple): The position of the robot in the arena (in cm)
        heading (float): The direction the robot is facing, in degrees CCW from North
        queued_commands (int): The number of commands given to the robot that are waiting to execute
        robot_number (int): The number used to identify the robot
    """
    number = 0
    def __init__(self, robot_id, port_id, robot_type):
        self.robot_id = robot_id
        self.port_id = port_id
        self.robot_type = robot_type
        self.position = (0, 0)
        self.heading = 0
        self.queued_commands = 0
        self.robot_number = Robot.number
        Robot.number += 1

class Sensor:
    """
    Representation of a sensor in the world model. Sensors record the position and heading
    of the robots. In the case of the simulator, sensors are the robots themselves.

    Args:
        port_id (int): The COM port used to communicate with the sensor
        sensor_type (string): The type of sensor, either a simulator SMORES or a real camera

    Attributes:
        port_id (int): The COM port used to communicate with the sensor
        sensor_type (string): The type of sensor, either a simulator SMORES or a real camera
        asked (bool): Boolean that tracks whether the sensor has been polled for an update
        recieved (bool): Boolean that tracks whether the sensor has responded to an update request
    """
    def __init__(self, port_id, sensor_type):
        self.port_id = port_id
        self.sensor_type = sensor_type
        self.asked = False
        self.received = False

class Tile:
    """
    The world model representation of an individual tile in the world model grid.
    Each tile can contain up to one robot and one goal.

    Args:
        x (int): The tile's horizontal position in the world model grid
        y (int): The tile's vertical position in the world model grid
        cm_per_tile (float): The conversion factor between the size of a tile and cm

    Attributes:
        occupied (Robot): The robot occupying the tile (None if the tile is open)
        goal (bool): Whether or not the tile is a goal
        robot_goal (Robot): The Robot assigned to this goal tile (None if this tile is not a goal)
        position (Tuple): The tile's position in the world model grid
        center (Tuple): The real coordinates of the tile's center, in cm
    """
    def __init__(self, x, y, cm_per_tile):
        self.occupied = None
        self.goal = False
        self.position = (x, y)
        self.center = ((x + 0.5) * cm_per_tile, (y + 0.5) * cm_per_tile)

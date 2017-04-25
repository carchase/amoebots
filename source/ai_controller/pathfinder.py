'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on April 15, 2017

View the full repository here https://github.com/car-chase/amoebots
'''

from __future__ import print_function
from pyddl import Domain, Problem, Action, neg, planner

class Pathfinder:
    """
    The PDDL processor that generates the moves necessary to get robots from their initial states
    to their goal states.  This level performs the pathfinding on the world and generates the
    commands for the robot to execute.

    Args:
        options (dict): The dictionary containing the program settings.
        world_grid (Tile[][]) The 2D array containing the current state of the world.
        robot_goal_positions (tuple[]) An array of tuples mapping robots to their goal positions.

    Attributes:
        options (dict): The dictionary containing the program settings.
        init_row (list): The list containing all the row numbers.
        init_col (list): The list containing all the column numbers.
        init_state (list): The list containing the current state of the world in PDDL.
        init_robots (list): The list containing all the robot ID numbers.
        init_goals (list): The list containing the goal state.
    """
    def __init__(self, options, world_grid, robot_goal_positions):
        self.init_row = []
        self.init_col = []
        self.init_state = []
        self.init_robots = []
        self.init_goals = []
        self.options = options

        # Determine which robots_numbers are active
        active_robots = []
        for robot in robot_goal_positions:
            active_robots.append(robot[0])

        # Parse the world to generate the initial state
        self.generate_init_state(self.options["ARENA_SIZE"], world_grid, active_robots)

        # Parse the goal positions to generate a goal state
        self.generate_goal_state(robot_goal_positions)

    def generate_init_state(self, world_size, world_grid, active_robots):
        """
        Generates the initial PDDL state of the world

        Args:
            world_size (int): The dictionary containing the program settings.
            world_grid (Tile[][]) The 2D array containing the current state of the world.
            active_robots (tuple[]) An array of the robot numbers to consider when solving.
        """
        self.init_state = []
        self.init_row = []
        self.init_col = []
        self.init_robots = []

        for row in range(world_size):
            for col in range(world_size):
                if world_grid[row][col].occupied is None:
                    self.init_state.append(('notOccupied', col, row))
                elif world_grid[row][col].occupied.robot_number in active_robots:
                    self.init_state.append(('at', world_grid[row][col].occupied.robot_number,
                                            col, row))
                    self.init_robots.append(world_grid[row][col].occupied.robot_number)
                else:
                    self.init_robots.append(world_grid[row][col].occupied.robot_number)
            self.init_row.append(row)
            self.init_col.append(row)

        for inc in range(world_size):
            self.init_state.append(('isLeftOf', inc, inc + 1))
            self.init_state.append(('isAbove', inc, inc + 1))

    def generate_goal_state(self, robots):
        """
        Generates the initial PDDL state of the world

        Args:
            world_size (int): The dictionary containing the program settings.
            world_grid (Tile[][]) The 2D array containing the current state of the world.
            active_robots (tuple[]) An array of the robot numbers to consider when solving.
        """
        self.init_goal = []
        for robot in robots:
            self.init_goal.append(('at', robot[0], robot[1][0], robot[1][1]))

    def start_algorithm(self):
        """
        Initiates the PDDL processing.  Returns the moves with the robot numbers.
        """
        domain = Domain((
            Action(
                'moveLeft',
                parameters=(
                    ('robot', 'r'),
                    ('row', 'x_old'),
                    ('row', 'x_new'),
                    ('col', 'y'),
                ),
                preconditions=(
                    ('at', 'r', 'x_old', 'y'),
                    ('notOccupied', 'x_new', 'y'),
                    ('isLeftOf', 'x_new', 'x_old'),
                ),
                effects=(
                    ('at', 'r', 'x_new', 'y'),
                    neg(('at', 'r', 'x_old', 'y')),
                    neg(('notOccupied', 'x_new', 'y')),
                    ('notOccupied', 'x_old', 'y'),
                ),
            ),
            Action(
                'moveRight',
                parameters=(
                    ('robot', 'r'),
                    ('row', 'x_old'),
                    ('row', 'x_new'),
                    ('col', 'y'),
                ),
                preconditions=(
                    ('at', 'r', 'x_old', 'y'),
                    ('notOccupied', 'x_new', 'y'),
                    ('isLeftOf', 'x_old', 'x_new'),
                ),
                effects=(
                    ('at', 'r', 'x_new', 'y'),
                    neg(('at', 'r', 'x_old', 'y')),
                    neg(('notOccupied', 'x_new', 'y')),
                    ('notOccupied', 'x_old', 'y'),
                ),
            ),
            Action(
                'moveUp',
                parameters=(
                    ('robot', 'r'),
                    ('row', 'x'),
                    ('row', 'y_old'),
                    ('col', 'y_new'),
                ),
                preconditions=(
                    ('at', 'r', 'x', 'y_old'),
                    ('notOccupied', 'x', 'y_new'),
                    ('isAbove', 'y_new', 'y_old'),
                ),
                effects=(
                    ('at', 'r', 'x', 'y_new'),
                    neg(('at', 'r', 'x', 'y_old')),
                    neg(('notOccupied', 'x', 'y_new')),
                    ('notOccupied', 'x', 'y_old'),
                ),
            ),
            Action(
                'moveDown',
                parameters=(
                    ('robot', 'r'),
                    ('row', 'x'),
                    ('row', 'y_old'),
                    ('col', 'y_new'),
                ),
                preconditions=(
                    ('at', 'r', 'x', 'y_old'),
                    ('notOccupied', 'x', 'y_new'),
                    ('isAbove', 'y_old', 'y_new'),
                ),
                effects=(
                    ('at', 'r', 'x', 'y_new'),
                    neg(('at', 'r', 'x', 'y_old')),
                    neg(('notOccupied', 'x', 'y_new')),
                    ('notOccupied', 'x', 'y_old'),
                ),
            ),
        ))
        problem = Problem(
            domain,
            {
                'row': tuple(self.init_row),
                'col': tuple(self.init_col),
                'robot': tuple(self.init_robots),
            },
            init=(
                tuple(self.init_state)
            ),
            goal=(
                tuple(self.init_goal)
            )
        )

        plan = planner(problem, verbose=None)

        # Parse out the moves
        robot_and_move = []
        if plan is not None:
            for action in plan:
                action_and_robot = (action.name, action.sig[1]) # The action name and the robot
                robot_and_move.append(action_and_robot)

        return robot_and_move

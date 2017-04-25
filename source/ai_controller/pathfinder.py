'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on April 15, 2017

View the full repository here https://github.com/car-chase/amoebots
'''

from __future__ import print_function
from pyddl import Domain, Problem, Action, neg, planner

class Pathfinder:

    def __init__(self, options, world_grid, robot_goal_positions):
        self.init_row = []
        self.init_col = []
        self.init_occupied = []
        self.init_robots = []
        self.init_goals = []
        self.options = options

        # Determine which robots_numbers are active
        active_robots = []
        for index, robot in enumerate(robot_goal_positions):
            active_robots.append(robot[0])

        # Parse the world to generate the initial state
        self.generate_init_state(self.options["ARENA_SIZE"], world_grid, active_robots)

        # Parse the goal positions to generate a goal state
        self.generate_goal_state(robot_goal_positions)

    def generate_init_state(self, world_size, world_grid, active_robots):
        self.init_occupied = []
        self.init_row = []
        self.init_col = []
        self.init_robots = []

        for row in range(world_size):
            for col in range(world_size):
                if world_grid[row][col].occupied is None:
                    self.init_occupied.append(('notOccupied', col, row))
                elif world_grid[row][col].occupied.robot_number in active_robots:
                    self.init_occupied.append(('at', world_grid[row][col].occupied.robot_number, col, row))
                    self.init_robots.append(world_grid[row][col].occupied.robot_number)
                else:
                    self.init_robots.append(world_grid[row][col].occupied.robot_number)
            self.init_row.append(row)
            self.init_col.append(row)

        for inc in range(world_size):
            self.init_occupied.append(('isLeftOf', inc, inc + 1))
            self.init_occupied.append(('isAbove', inc, inc + 1))

    def generate_goal_state(self, robots):
        self.init_goal = []
        for robot in robots:
            self.init_goal.append(('at', robot[0], robot[1][0], robot[1][1]))

    def problem(self, verbose):
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
                tuple(self.init_occupied)
            ),
            goal=(
                tuple(self.init_goal)
            )
        )

        def to_coordinates(state):
            grid = {}
            #for p in state:
            #    if p[0] == 'at':
            #        grid[p[1]] = (p[2], p[3])
            return grid

        goal_coords = to_coordinates(problem.goals)

        def manhattan_distance_heuristic(state):
            state_coords = to_coordinates(state.predicates)
            dist = 0
            for k in goal_coords.keys():
                c1, r1 = goal_coords[k]
                c2, r2 = state_coords[k]
                dist += (abs(c1 - c2) + abs(r1 - r2))
            return dist

        plan = planner(problem, heuristic=manhattan_distance_heuristic, verbose=verbose)
        robot_and_move = []
        if plan is None:
            print('No Plan!')
        else:
            for action in plan:
                action_and_robot = (action.name, action.sig[1])  # This is returning the action name and the robot
                robot_and_move.append(action_and_robot)
        
        return robot_and_move

    def start_algorithm(self):
        from optparse import OptionParser
        parser = OptionParser(usage="Usage: %prog [options]")
        parser.add_option('-q', '--quiet', action='store_false', dest='verbose', default=True, 
                          help="don't print statistics to stdout")

        # Parse arguments
        opts, args = parser.parse_args()
        robot_and_move = self.problem(opts.verbose)
        return robot_and_move

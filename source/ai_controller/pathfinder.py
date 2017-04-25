'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on April 15, 2017

View the full repository here https://github.com/car-chase/amoebots
'''

import math
import pddl_algorithm


class Pathfinder:

    def __init__(self, options):
        self.options = options

    def robot_goal_assignment(self, world):
        goal_positions = [] # [(goal_x, goal_y)]
        robot_and_position = [] # [(robot_number, (robot_x, robot_y))]
        robot_and_goal = [] # [(robot_number, (goal_x, goal_y))]

        for row in range(self.options["ARENA_SIZE"]):
            for col in range(self.options["ARENA_SIZE"]):
                if world.grid[row][col].goal is True:
                    goal_positions.append(world.grid[row][col].position)
                if world.grid[row][col].occupied is not None:
                    robot_and_position.append((world.grid[row][col].occupied.robot_number,
                                               world.grid[row][col].position))

        # Loop over the goals
        for goal_index, goal in enumerate(goal_positions):

            # The farthest away a robot can possibly be
            closest_distance = float("inf")

            # Loop over each robot for the goal
            for index, entry in enumerate(robot_and_position):
                if entry is None:
                    continue

                dist = math.hypot(entry[1][0] - goal[0],   # x2 - x1
                                  entry[1][1] - goal[1])   # y2 - y1

                if dist < closest_distance:
                    closest_robot = entry[0]
                    ele_with_robot = index
                    closest_distance = dist

            # We have compared all robots, now assign the winner to the goal
            print(closest_robot, " to ", goal)
            robot_and_goal.append((closest_robot, goal))

            robot_and_position[ele_with_robot] = None
            goal_positions[goal_index] = None

        return robot_and_goal

    def generate_moves(self, world):

        robot_and_goal = self.robot_goal_assignment(world)

        robots = []
        robot_goals = []

        for index, entry in enumerate(robot_and_goal):
            print("robotID", entry[0])
            robots.append(entry[0])
            robot_goals.append(entry)
            if len(robots) % self.options["ROBOTS_PLANNED_PER_ITERATION"] == 0:
                pddl_algorithm.generate_init_state(self.options["ARENA_SIZE"], world, robots)
                pddl_algorithm.generate_goal_state(robot_goals)
                robots = []
                robot_goals = []
                robot_moves = pddl_algorithm.start_algorithm()
                if len(robot_moves) > 0:
                    return robot_moves
            elif index == len(robot_and_goal) - 1: # It is the last one
                pddl_algorithm.generate_init_state(self.options["ARENA_SIZE"], world, robots)
                pddl_algorithm.generate_goal_state(robot_goals)
                robot_moves = pddl_algorithm.start_algorithm()
                if len(robot_moves) > 0:
                    return robot_moves
        return None

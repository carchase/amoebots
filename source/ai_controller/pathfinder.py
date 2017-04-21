import world_model
import math
import pddl_algorithm

goal_position = []
robot_position_and_object = []
robot_goal_and_position = []

def robot_goal_assignment(world_size_grid, world):

    for row in range(world_size_grid):
        for col in range(world_size_grid):
            if world.grid[row][col].goal is True:
                goal_position.append(world.grid[row][col].position)
            if world.grid[row][col].occupied is not None:
                robot_position_and_object.append((world.grid[row][col].position,
                                                  world.grid[row][col].occupied.robot_number))

    print(robot_position_and_object)

    # Check if anyone is at an existing goal
    # for goal_index, goal in enumerate(goal_position):
    #     for robot_index, robot in enumerate(robot_position_and_object):
    #         if robot is None:
    #             continue

    #         if goal == robot[0]:
    #             world.grid[goal[1]][goal[0]].robot_goal = robot[1]
    #             goal_position[goal_index] = None
    #             robot_position_and_object[robot_index] = None
    #             break

    # print(robot_position_and_object)

    # Loop over the goals
    for goal_index, goal in enumerate(goal_position):

        # The farthest away a robot can possibly be
        dist_temp = float("inf")

        # Loop over each robot for the goal
        for robot_index, robot in enumerate(robot_position_and_object):
            if robot is None:
                continue

            dist = math.hypot(robot[0][0] - goal[0],   # x2 - x1
                              robot[0][1] - goal[1])   # y2 - y1

            if dist < dist_temp:
                robot_with_shortest_distance = robot[1]
                ele_with_robot = robot_index

        # We have compared all robots, now assign the winner to the goal
        print(robot_with_shortest_distance, " to ", goal)
        world.grid[goal[1]][goal[0]].robot_goal = robot_with_shortest_distance
        robot_goal_and_position.append((robot_with_shortest_distance, goal[0], goal[1]))
        dist_temp = dist

        robot_position_and_object[ele_with_robot] = None
        goal_position[goal_index] = None

    print(robot_goal_and_position)


def generate_moves(world_grid_size, world):
    if(len(robot_goal_and_position) == 0):
        robot_goal_assignment(world_grid_size, world)

    for item in range(len(robot_goal_and_position)):
        print("robotID", robot_goal_and_position[item][0])
        algorithm = pddl_algorithm
        algorithm.generate_init_state(world_grid_size, world, robot_goal_and_position[item][0])
        algorithm.generate_goal_state(robot_goal_and_position[item][0], robot_goal_and_position[item][1],
                                      robot_goal_and_position[item][2])
        robot_moves = algorithm.start_algorithm()
        if len(robot_moves) > 0:
            return robot_moves

    return None

# orig_world = world_model.Arena(5, 5)
# world_size_grid = 5
# for robot in range(world_size_grid):
#     init_robots.append(world_model.Robot(robot, 0))

# orig_world.grid[0][0].occupied = init_robots[0]
# orig_world.grid[0][4].occupied = init_robots[1]
# orig_world.grid[4][0].occupied = init_robots[2]
# orig_world.grid[4][4].occupied = init_robots[3]
# orig_world.grid[2][2].occupied = init_robots[4]
# orig_world.grid[2][1].goal = True
# orig_world.grid[2][2].goal = True
# orig_world.grid[2][3].goal = True
# orig_world.grid[1][2].goal = True
# orig_world.grid[3][2].goal = True
# generate_moves(world_size_grid, orig_world)
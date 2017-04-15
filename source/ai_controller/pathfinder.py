import world_model
import math
import pddl_algorithm

goal_position = []
init_robots = []
robot_position_and_object = []
robot_goal_and_position = []


def robot_goal_assignment(world_size_grid, world):

    for row in range(world_size_grid):
        for col in range(world_size_grid):
            if world.grid[row][col].goal is True:
                goal_position.append(world.grid[row][col].position)
            if world.grid[row][col].occupied is not None:
                robot_position_and_object.append((world.grid[row][col].position,
                                                  world.grid[row][col].occupied.port_id))

    # Check if anyone is at an existing goal
    goals_deleted = 0
    for goal in range(len(goal_position)):
        for robot in range(len(robot_position_and_object)):
            if goal_position[goal - goals_deleted] == robot_position_and_object[robot][0]:
                world.grid[goal_position[goal - goals_deleted][1]][goal_position[goal - goals_deleted][0]].robot_goal = robot_position_and_object[robot][1]
                del goal_position[goal - goals_deleted]
                del robot_position_and_object[robot]
                goals_deleted += 1
                break

    dist_temp = 0
    for i in range(len(goal_position)):
        robot_with_shortest_distance = 0
        ele_with_robot = 0
        for j in range(len(goal_position)):
            dist = math.hypot(robot_position_and_object[j][0][0] - goal_position[0][0],   # x2 - x1
                              robot_position_and_object[j][0][1] - goal_position[0][1])   # y2 - y1

            if dist < dist_temp or dist is 0:
                robot_with_shortest_distance = robot_position_and_object[j][1]
                ele_with_robot = j
            elif len(goal_position) == 1:
                robot_with_shortest_distance = robot_position_and_object[j][1]
                ele_with_robot = j

        print(robot_with_shortest_distance, " to ", goal_position[0][0], goal_position[0][1])
        world.grid[goal_position[0][1]][goal_position[0][0]].robot_goal = robot_with_shortest_distance
        robot_goal_and_position.append((robot_with_shortest_distance, goal_position[0][0], goal_position[0][1]))
        del(robot_position_and_object[ele_with_robot])
        dist_temp = dist

        del(goal_position[0])


def generate_moves(world_grid_size, world):
    robot_goal_assignment(world_grid_size, world)

    for item in range(len(robot_goal_and_position)):
        print("robotID", robot_goal_and_position[item][0])
        algorithm = pddl_algorithm
        algorithm.generate_init_state(world_grid_size, world, robot_goal_and_position[item][0])
        algorithm.generate_goal_state(robot_goal_and_position[item][0], robot_goal_and_position[item][1],
                                      robot_goal_and_position[item][2])
        algorithm.start_algorithm()

    

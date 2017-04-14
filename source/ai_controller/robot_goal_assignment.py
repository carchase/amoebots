import world_model
import math
import pddl_algorithm

goal_position = []
init_robots = []
robot_position_and_object = []
robot_goal_and_position = []


def robot_goal_assignment(world_size_grid, WORLD):

    for row in range(world_size_grid):
        for col in range(world_size_grid):
            if WORLD.grid[row][col].goal is True:
                goal_position.append(WORLD.grid[row][col].position)
            if WORLD.grid[row][col].occupied is not None:
                robot_position_and_object.append((WORLD.grid[row][col].position, WORLD.grid[row][col].occupied.port_id))

    dist_temp = 0
    for i in range(len(goal_position)):
        for j in range(len(goal_position)):
            dist = math.hypot(robot_position_and_object[j][0][0] - goal_position[0][0],   # x2 - x1
                              robot_position_and_object[j][0][1] - goal_position[0][1])   # y2 - y1

            if dist < dist_temp:
                robot_with_shortest_distance = robot_position_and_object[j][1]
                ele_with_robot = j
            elif len(goal_position) == 1:
                robot_with_shortest_distance = robot_position_and_object[j][1]
                ele_with_robot = j

            if WORLD.grid[goal_position[0][0]][goal_position[0][1]].robot_goal is None and j is len(goal_position)-1:
                print(robot_with_shortest_distance)
                WORLD.grid[goal_position[0][0]][goal_position[0][1]].robot_goal = robot_with_shortest_distance
                robot_goal_and_position.append((robot_with_shortest_distance, goal_position[0][0], goal_position[0][1]))
                del(robot_position_and_object[ele_with_robot])
            dist_temp = dist

        del(goal_position[0])


def main():
    WORLD = world_model.Arena(5, 5)
    world_size_grid = 5

    for robot in range(world_size_grid):
        init_robots.append(world_model.Robot(robot, 0))

    WORLD.grid[0][0].occupied = init_robots[0]
    WORLD.grid[0][4].occupied = init_robots[1]
    WORLD.grid[4][0].occupied = init_robots[2]
    WORLD.grid[4][4].occupied = init_robots[3]
    WORLD.grid[2][2].goal = True
    WORLD.grid[2][1].goal = True
    WORLD.grid[3][2].goal = True
    WORLD.grid[2][3].goal = True
    robot_goal_assignment(world_size_grid, WORLD)

    for item in range(len(robot_goal_and_position)):
        pddl_algorithm.generate_init_state(world_size_grid, WORLD, init_robots)
        pddl_algorithm.generate_goal_state(robot_goal_and_position[item][0], robot_goal_and_position[item][1], robot_goal_and_position[item][2])
        pddl_algorithm.start_algorithm()

main()


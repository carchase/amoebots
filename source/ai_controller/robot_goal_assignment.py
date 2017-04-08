import world_model
import math

goal_position = []
robot_position = []
init_robots = []
robot_id = []
robot_position_and_object = []


def robot_goal_assignment(world_size_grid, world_size_centimeter, how_many_robots):
    WORLD = world_model.Arena(world_size_grid, world_size_centimeter)

    for robot in range(how_many_robots):
        init_robots.append(world_model.Robot(robot, 0))

    WORLD.grid[0][0].occupied = init_robots[0]
    WORLD.grid[0][6].occupied = init_robots[1]
    WORLD.grid[6][0].occupied = init_robots[2]
    WORLD.grid[6][6].occupied = init_robots[3]
    WORLD.grid[3][3].goal = True
    WORLD.grid[3][2].goal = True
    WORLD.grid[4][3].goal = True
    WORLD.grid[2][3].goal = True

    for row in range(world_size_grid):
        for col in range(world_size_grid):
            if WORLD.grid[row][col].goal is True:
                goal_position.append(WORLD.grid[row][col].position)
            if WORLD.grid[row][col].occupied is not None:
                robot_position_and_object.append((WORLD.grid[row][col].position, WORLD.grid[row][col].occupied))
                # robot_position.append(WORLD.grid[row][col].position)
                # robot_id.append(WORLD.grid[row][col].occupied.port_id)

    shortest_dist = 0
    for i in range(len(goal_position)):
        for j in range(len(goal_position)):
            dist = math.hypot(robot_position_and_object[j][0][0] - goal_position[i][0],   # x2 - x1
                              robot_position_and_object[j][0][1] - goal_position[i][1])   # y2 - y1

            print('i: ', i,
                  'j: ', j,
                  'x2 - x1: ', robot_position_and_object[j][0][0] - goal_position[i][0],
                  'y2 - y1: ', robot_position_and_object[j][0][1] - goal_position[i][1],
                  'distance between the two locations: ', dist)

            if dist < shortest_dist:
                shortest_dist = dist
                robot_with_shortest_distance = robot_position_and_object[j][1]
                print("I've made it to the if statement!")
                if WORLD.grid[goal_position[i][0]][goal_position[i][1]].robot_goal is None and j == len(goal_position):
                    print("I've made it to add a robot to the robot_goal!")
                    WORLD.grid[goal_position[i][0]][goal_position[i][1]].robot_goal = robot_with_shortest_distance
                    del(robot_position_and_object[j])
                    del(goal_position[i])
            else:
                shortest_dist = dist

        print('\n\nNext Comparison')

def main():
    robot_goal_assignment(7, 7, 4)

main()


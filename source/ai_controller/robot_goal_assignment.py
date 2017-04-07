import world_model

goal_position = []
robot_position = []

def robot_goal_assignment():
    row_len = len(world_model.grid[0])
    col_len = len(world_model.grid)

    world_model.grid[3][3].goal = True
    world_model.grid[3][2].goal = True
    world_model.grid[4][3].goal = True
    world_model.grid[2][3].goal = True

    for row in range(row_len):
        for col in range(col_len):
            if world_model.grid[row][col].goal is not False:
                goal_position.append(world_model.grid[row][col].position)
            if world_model.grid[row][col].occupied is not None:
                robot_position.append(world_model.grid[row][col].occupied.robot_id.position)

    comparison_holder = 0
    shortest_path_length = 0
    for r_position in robot_position:
        for g_position in goal_position:
            comparison_holder = r_position - g_position
            if comparison_holder < shortest_path_length:
                shortest_path_length = comparison_holder


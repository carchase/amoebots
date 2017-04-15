from __future__ import print_function
from pyddl import Domain, Problem, Action, neg, planner
import time
import world_model

init_array = []
init_row = []
init_col = []
init_goal = []
init_robots = []
robot_and_move = []


def generate_init_state(world_size_grid, world, robot):
    global init_array
    global init_row
    global init_col
    global init_robots
    init_array = []
    init_row = []
    init_col = []
    init_robots = []

    for row in range(world_size_grid):
        for col in range(world_size_grid):
            if world.grid[row][col].occupied is None:
                init_array.append(('notOccupied', col, row))
            elif world.grid[row][col].occupied.port_number is robot:
                init_array.append(('at', world.grid[row][col].occupied.port_number, col, row))
                init_robots.append(world.grid[row][col].occupied.port_number)
            else:
                init_robots.append(world.grid[row][col].occupied.port_number)
        init_row.append(row)
        init_col.append(row)

    for inc in range(world_size_grid):
        init_array.append(('isLeftOf', inc, inc + 1))
        init_array.append(('isAbove', inc, inc + 1))

    print(init_robots)

def generate_goal_state(robot, x, y):
    global init_goal
    init_goal = []
    init_goal.append(('at', robot, x, y))

def problem(verbose):
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
            'row': tuple(init_row),
            'col': tuple(init_col),
            'robot': tuple(init_robots),
        },
        init=(
            tuple(init_array)
        ),
        goal=(
            tuple(init_goal)
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
    if plan is None:
        print('No Plan!')
    else:
        for action in plan:
            action_and_robot = (action.name, action.sig[1])  # This is returning the action name and the robot
            robot_and_move.append(action_and_robot)



def start_algorithm():
    from optparse import OptionParser
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option('-q', '--quiet',
                      action='store_false', dest='verbose', default=True,
                      help="don't print statistics to stdout")

    # Parse arguments
    opts, args = parser.parse_args()
    st = time.time()
    problem(opts.verbose)
    print("TOOK " + str((time.time()-st)/60) + " MINUTES")
    return robot_and_move

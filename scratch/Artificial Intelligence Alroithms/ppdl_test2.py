'''
Author: Ben Smith
CS465: Senior Design

This program should start the shell of what our PDDL is going to be for our Senior Design Project
Here, we will define, using the pyddl library, a PDDL for our planning algorithm to control
our smores robots.

Initial State: Our robots are going to start in random locations within the arena.

Goal State: The robots are going to form 1 of 2 or 3 formations.


Some things to note:
1. Make sure to discretize x and y because the robots are not going to be in their squares, perfectly.
So, to make up for the room for error, we're going to need to make these pixel values cleaner.

Try to create some actions that let the robots move diagonally.

To explain some of the variables:
robot: this refers to the robots that will be in the arena.
x and y: are the current position of the robot.
posX, posY, negX, and negY: These variables indicate when the robot is moving.
    neg being negative, and pos being positive.

'''
from __future__ import print_function
from pyddl import Domain, Problem, Action, neg, planner

def problem(verbose):
    domain = Domain((
        Action('move-up',
               parameters=(
                   ('robot', 'r'),
                   ('position', 'x'),
                   ('position', 'y'),
                   ('position', 'y+1'),
               ),
               preconditions=(
                   ('at', 'r', 'x', 'y'),
               ),
               effects=(
                   neg(('at', 'r', 'x', 'y')),
                   ('at', 'r', 'x', 'y+1'),
               ),
               ),
    ))
    problem = Problem(
        domain,
        {'robot': (1, 2),
         'position': (0, 1),
         },
        init=(
            ('at', 1, 0, 0),
            ('at', 2, 1, 0),
        ),
        goal=(
            ('at', 1, 0, 1),
            ('at', 2, 1, 1),
        )
    )

    # The following is code directly from the example.
    def to_coordinates(state):
        grid = {}
        for p in state:
            if p[0] == 'at':
                grid[p[1]] = (p[2], p[3])
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
            print(action)


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option('-q', '--quiet',
                      action='store_false', dest='verbose', default=True,
                      help="don't print statistics to stdout")

    # Parse arguments
    opts, args = parser.parse_args()
    problem(opts.verbose)
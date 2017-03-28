from __future__ import print_function
from pyddl import Domain, Problem, Action, neg, planner
import time

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
            'row': (0, 1, 2, 3, 4, 5, 6),
            'col': (0, 1, 2, 3, 4, 5, 6),
            'robot': (0,1),
        },
        init=(
#        MODIFY THE FOLLOWING. Make sure that you do TWO things for the starting position
#        of each robot. If the robot r starts at position x,y, then:
#        1) Comment out the line ('notOccupied',r,x,y)
#        2) Add the line ('at',r,x,y)
#        In the below example, there are three robots, and the goal is to move robot 0 to
#        position (4,0).
            ('notOccupied', 6, 0),
            ('notOccupied', 5, 0),
        	('notOccupied', 4, 0),
        	# ('notOccupied', 3, 0),
        	('notOccupied', 2, 0),
        	('notOccupied', 1, 0),
        	('notOccupied', 0, 0),
            ('notOccupied', 6, 1),
            ('notOccupied', 5, 1),
        	('notOccupied', 4, 1),
        	('notOccupied', 3, 1),
        	('notOccupied', 2, 1),
        	('notOccupied', 1, 1),
        	('notOccupied', 0, 1),
            ('notOccupied', 6, 2),
            ('notOccupied', 5, 2),
        	('notOccupied', 4, 2),
        	('notOccupied', 3, 2),
        	('notOccupied', 2, 2),
        	('notOccupied', 1, 2),
        	('notOccupied', 0, 2),
            ('notOccupied', 6, 3),
            ('notOccupied', 5, 3),
        	('notOccupied', 4, 3),
        	('notOccupied', 3, 3),
        	('notOccupied', 2, 3),
        	('notOccupied', 1, 3),
        	('notOccupied', 0, 3),
            ('notOccupied', 6, 4),
            ('notOccupied', 5, 4),
        	('notOccupied', 4, 4),
        	('notOccupied', 3, 4),
        	('notOccupied', 2, 4),
        	('notOccupied', 1, 4),
        	('notOccupied', 0, 4),
            ('notOccupied', 6, 5),
            ('notOccupied', 5, 5),
            ('notOccupied', 4, 5),
            ('notOccupied', 3, 5),
            ('notOccupied', 2, 5),
            ('notOccupied', 1, 5),
            ('notOccupied', 0, 5),
            ('notOccupied', 6, 6),
            ('notOccupied', 5, 6),
            ('notOccupied', 4, 6),
            ('notOccupied', 3, 6),
            ('notOccupied', 2, 6),
            ('notOccupied', 1, 6),
            ('notOccupied', 0, 6),
        	('isLeftOf', 0, 1),
        	('isLeftOf', 1, 2),
        	('isLeftOf', 2, 3),
        	('isLeftOf', 3, 4),
            ('isLeftOf', 4, 5),
            ('isLeftOf', 5, 6),
        	('isAbove', 0, 1),
        	('isAbove', 1, 2),
        	('isAbove', 2, 3),
        	('isAbove', 3, 4),
            ('isAbove', 4, 5),
            ('isAbove', 5, 6),
        	('at',0,3,0),
        	# ('at',1,2,0),
            # ('at',2,1,0),
            # ('at',3,0,0),
            # ('at',4,3,2),
        ),
        goal=(
        #Set the goal as follows. This one lines them all up vertically.
            ('at',0,2,4),
            # ('at',1,1,4),
            # ('at',2,3,4),
            # ('at',3,2,5),
            # ('at',4,3,5),
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
            print(action)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option('-q', '--quiet',
                      action='store_false', dest='verbose', default=True,
                      help="don't print statistics to stdout")

    # Parse arguments
    opts, args = parser.parse_args()
# st = time.time()
problem(opts.verbose)
# print("TOOK " + str((time.time()-st)/60) + " MINUTES")
from __future__ import print_function
from pyddl import Domain, Problem, Action, neg, planner

def problem(verbose):
    domain = Domain((
        Action('move_up',
                parameters=(('robot', 'r'), ('position', 'x'), ('position', 'y'), ('position', 'y+1'),),
               preconditions=(('dec', 'y+1', 'y'), ('at', 'r', 'x', 'y'), neg(('at', 'r', 'x', 'y+1')),),
               effects=(neg(('at', 'r', 'x', 'y')), ('at', 'r', 'x', 'y+1'),),
               ),
        Action('move_down',
               parameters=(('robot', 'r'), ('position', 'x'), ('position', 'y'), ('position', 'y-1'),),
               preconditions=(('inc', 'y-1', 'y'), ('at', 'r', 'x', 'y'), neg(('at', 'r', 'x', 'y-1')),),
               effects=(neg(('at', 'r', 'x', 'y')), ('at', 'r', 'x', 'y-1'),),
               ),
        Action('move_left',
               parameters=(('robot', 'r'), ('position', 'x'), ('position', 'y'), ('position', 'x-1'),),
               preconditions=(('dec', 'x-1', 'x'), ('at', 'r', 'x', 'y'), neg(('at', 'r', 'x', 'x-1')),),
               effects=(neg(('at', 'r', 'x', 'y')), ('at', 'r', 'x', 'x-1'),),
               ),
        Action('move_right',
               parameters=(('robot', 'r'), ('position', 'x'), ('position', 'y'), ('position', 'x+1'),),
               preconditions=(('inc', 'x+1', 'x'), ('at', 'r', 'x', 'y'), neg(('at', 'r', 'x', 'x+1')),),
               effects=(neg(('at', 'r', 'x', 'y')), ('at', 'r', 'x', 'x+1'),),
               ),
    ))
    problem = Problem(domain,
                      {'robot': (1, 2),
                       'position': (0, 1), },
                      init=(('at', 1, 0, 0), ('at', 2, 1, 1),),
                      goal=(('at', 1, 0, 1), ('at', 2, 1, 0),))

#     plan = planner(problem, verbose=verbose)
#     if plan is None:
#         print('No Plan!')
#     else:
#         for action in plan:
#             print(action)
#
# if __name__ == '__main__':
#     from optparse import OptionParser
#
#     parser = OptionParser(usage="Usage: %prog [options]")
#     parser.add_option('-q', '--quiet',
#                       action='store_false', dest='verbose', default=True,
#                       help="don't print statistics to stdout")
#
#     # Parse arguments
#     opts, args = parser.parse_args()
#     problem(opts.verbose)

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
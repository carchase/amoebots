import world_model
import movement_level

ROBOT0 = world_model.Robot("robot0")
ROBOT1 = world_model.Robot("robot1")
ROBOT2 = world_model.Robot("robot2")
ROBOT3 = world_model.Robot("robot3")

WORLD = world_model.Grid(7, 35)
WORLD.grid[0][0].occupied = ROBOT0
WORLD.grid[0][6].occupied = ROBOT1
WORLD.grid[6][0].occupied = ROBOT2
WORLD.grid[6][6].occupied = ROBOT3

'''
[[T, 0, 0, 0, 0, 0, T],
 [0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0],
 [T, 0, 0, 0, 0, 0, T]]
'''
movement_level = movement_level.MovementLevel(None)
import world_model

WORLD = world_model.Grid(7, 35)
WORLD.get_tile((0, 0)).occupied = world_model.Robot("robot0")
WORLD.get_tile((0, 6)).occupied = world_model.Robot("robot1")
WORLD.get_tile((6, 0)).occupied = world_model.Robot("robot2")
WORLD.get_tile((6, 6)).occupied = world_model.Robot("robot3")

'''
[[T, 0, 0, 0, 0, 0, T],
 [0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0],
 [T, 0, 0, 0, 0, 0, T]]
'''

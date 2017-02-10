# File:          SupervisorController.py
# Date:          
# Description:   
# Author:        
# Modifications: 

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, LED, DistanceSensor
#
# or to import the entire module. Ex:
#  from controller import *
from controller import Supervisor

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class SupervisorController (Supervisor):
  
  # User defined function for initializing and running
  # the SupervisorController class
  def run(self):
    
    # Main loop
    while True:
      # Perform a simulation step of 64 milliseconds
      # and leave the loop when the simulation is over
      if self.step(64) == -1:
        break
      
      print(getRobotPosition(self, 'Module'))
      print(getRobotOrientation(self, 'Module'))
    
    # Enter here exit cleanup code

# Returns the position of the given robot
# params: self, DEF name of robot
# return: Position vector of robot, or None if robot is not found
def getRobotPosition(self, robot):
  robot_node = self.getFromDef(robot)
  if robot_node is None:
    return None
  return robot_node.getPosition()

# Returns the orientation of the given robot
# params: self, DEF name of robot
# return: 3x3 rotational matrix of robot, or None if robot is not found
def getRobotOrientation(self, robot):
  robot_node = self.getFromDef(robot)
  if robot_node is None:
    return None
  o = robot_node.getOrientation()
  return [[o[0], o[1], o[2]], [o[3], o[4], o[5]], [o[6], o[7], o[8]]]

# The main program starts from here

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = SupervisorController()
controller.run()

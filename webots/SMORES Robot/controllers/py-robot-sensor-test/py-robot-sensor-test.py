# File:          py-robot-sensor-test.py
# Date:          
# Description:   
# Author:        
# Modifications: 

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, LED, DistanceSensor
#
# or to import the entire module. Ex:
#  from controller import *
from controller import *

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class RobotSensorTest (Robot):
  
  # User defined function for initializing and running
  # the py-robot-sensor-test class
  def run(self):
    
    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    # led = self.getLed('led')
    ds_left = self.getDistanceSensor("ds_left")
    ds_right = self.getDistanceSensor("ds_right")

    ds_left.enable(64)
    ds_right.enable(64)

    # print str(ds_left.getMinRange()) + "-" + str(ds_left.getMaxRange())
    # print str(ds_right.getMinRange()) + "-" + str(ds_right.getMaxRange())
    
    # Main loop
    while True:
      # Perform a simulation step of 64 milliseconds
      # and leave the loop when the simulation is over
      if self.step(64) == -1:
        break
      
      # Read the sensors:
      # Enter here functions to read sensor data, like:
      #  val = ds.getValue()
      lval = ds_left.getValue()
      rval = ds_right.getValue()
      
      # Process sensor data here.
      print str(lval) + ", " + str(rval)
      
      # Enter here functions to send actuator commands, like:
      # led.set(1)
    
    # Enter here exit cleanup code

# The main program starts from here

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = RobotSensorTest()
controller.run()

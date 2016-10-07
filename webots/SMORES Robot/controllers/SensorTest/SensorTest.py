# File:          SensorTest.py
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
class SensorTest (Robot):
  
  # User defined function for initializing and running
  # the SensorTest class
  def run(self):
    
    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  led = self.getLed('ledname')
    top_ds = self.getDistanceSensor("distance_sensor_1")
    right_ds = self.getDistanceSensor("distance_sensor_2")
    left_ds = self.getDistanceSensor("distance_sensor_3")

    top_ds.enable(64)
    right_ds.enable(64)
    left_ds.enable(64)
    
    # Main loop
    while True:
      # Perform a simulation step of 64 milliseconds
      # and leave the loop when the simulation is over
      if self.step(64) == -1:
        break
      
      # Read the sensors:
      # Enter here functions to read sensor data, like:
      #  val = ds.getValue()
      top_val = top_ds.getValue()
      print "Top: " + str(top_val)
      right_val = right_ds.getValue()
      print "Right: " + str(right_val)
      left_val = left_ds.getValue()
      print "Left: " + str(left_val)

      # Process sensor data here.
      
      # Enter here functions to send actuator commands, like:
      #  led.set(1)
    
    # Enter here exit cleanup code

# The main program starts from here

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = SensorTest()
controller.run()

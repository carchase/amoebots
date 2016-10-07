# File:          ModuleTest.py
# Date:          
# Description:   
# Author:        
# Modifications: 

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, LED, DistanceSensor
#
# or to import the entire module. Ex:
#  from controller import *
from controller import Robot
import math

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class ModuleTest (Robot):

  speed = 1
  
  # User defined function for initializing and running
  # the ModuleTest class
  def run(self):
    
    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  led = self.getLed('ledname')
    top_motor = self.getMotor("Bending Motor")
    # top_motor.setPosition(-1)
    left_motor = self.getMotor("Left Wheel Motor")
    left_motor.setPosition(float('inf'))
    right_motor = self.getMotor("Right Wheel Motor")
    right_motor.setPosition(float('inf'))
    
    cam = self.getCamera("camera")
    cam.enable(64)

    right_ds = self.getDistanceSensor("right sonar")
    right_ds.enable(64)
    left_ds = self.getDistanceSensor("left sonar")
    left_ds.enable(64)

    top_conn = self.getConnector("top conn")
    top_conn.enablePresence(64)
    left_conn = self.getConnector("left conn")
    left_conn.enablePresence(64)
    right_conn = self.getConnector("right conn")
    right_conn.enablePresence(64)
    back_conn = self.getConnector("back conn")
    back_conn.enablePresence(64)

    # Main loop
    while True:
      # Perform a simulation step of 64 milliseconds
      # and leave the loop when the simulation is over
      if self.step(64) == -1:
        break
      
      # Read the sensors:
      # Enter here functions to read sensor data, like:
      #  val = ds.getValue()
      right_dist = right_ds.getValue()
      left_dist = left_ds.getValue()
      
      # Process sensor data here.
      print "right: " + str(right_dist)
      print "left: " + str(left_dist)     

      # Enter here functions to send actuator commands, like:
      #  led.set(1)
      if left_dist < 10:
        turn(self, left_motor, right_motor, 90)
      elif right_dist < 10:
        turn(self, left_motor, right_motor, -90)
      elif top_conn.getPresence() == 1:
        left_motor.setVelocity(0)
        right_motor.setVelocity(0)
      else:
        left_motor.setVelocity(self.speed)
        right_motor.setVelocity(self.speed)
    
    # Enter here exit cleanup code

def turn(self, left_motor, right_motor, degrees):
  radians = math.radians(degrees)
  turn_time = 10.0 / (self.speed / radians)
  if radians >= 0:
    left_motor.setVelocity(self.speed)
    right_motor.setVelocity(-self.speed)
  else:
    left_motor.setVelocity(-self.speed)
    right_motor.setVelocity(self.speed)
  self.step((int) (100 * turn_time)) # TODO: what is the proper multiplier (and make it not a magic number)?

# The main program starts from here

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = ModuleTest()
controller.run()

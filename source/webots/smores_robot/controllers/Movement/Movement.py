# File:          Movement.py
# Date:          11/26/2016
# Description:   
# Author:        Jeffery Ross
# Modifications: 

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, LED, DistanceSensor
#
# or to import the entire module. Ex:
#  from controller import *
from controller import Robot
import time

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class Movement (Robot):
  
  # User defined function for initializing and running
  # the Movement class
  def run(self):
    
    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  led = self.getLed('ledname')
    top_motor = self.getMotor("Bending Motor")
    top_motor.setPosition(float('inf'))
    left_motor = self.getMotor("Left Wheel Motor")
    left_motor.setPosition(float('inf'))
    right_motor = self.getMotor("Right Wheel Motor")
    right_motor.setPosition(float('inf'))

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

      # read cmd and vel here!
      
      
      # Process sensor data here.
      
      # Enter here functions to send actuator commands, like:
      #  led.set(1)
      handleInput(cmd, vel)
    
    # Enter here exit cleanup code

def handleInput(cmd, vel):
  if cmd == 1:
    print 'Moving forward'
    moveWheels(vel, vel, True)
  elif cmd == 2:
    print 'Moving backward'
    moveWheels(-vel, -vel, True)
  elif cmd == 3:
    print 'Turning left'
    moveWheels(0, vel, True)
  elif cmd == 4:
    print 'Turning right'
    moveWheels(vel, 0, True)
  elif cmd == 5:
    print 'Stopping'
    moveWheels(0, 0, False)
  elif cmd == 6:
    print 'Stopping arm'
    moveArm(0, False)
  elif cmd == 7:
    print 'Moving arm' # up?
    moveArm(vel, True)
  elif cmd == 8:
    print 'Moving arm' # down?
    moveArm(-vel, True)
  elif cmd == 11:
    print 'Moving forward'
    moveWheels(vel, vel, False)
  elif cmd == 12:
    print 'Moving backward'
    moveWheels(-vel, -vel, False)
  elif cmd == 13:
    print 'Turning left'
    moveWheels(0, vel, False)
  elif cmd == 14:
    print 'Turning right'
    moveWheels(vel, 0, False)
  elif cmd == 15:
    print 'Moving arm' # up?
    moveArm(vel, False)
  elif cmd == 16:
    print 'Moving arm' # down?
    moveArm(-vel, False)
  else:
    print 'Invalid command ' + str(cmd)

def moveWheels(left, right, delay):
  left_motor.setVelocity(left)
  right_motor.setVelocity(right)
  if delay:
    time.sleep(1)
    moveWheels(0, 0, False)

def moveArm(velocity, delay):
  top_motor.setVelocty(velocity)
  if delay:
    time.sleep(1)
    moveArm(0, False)

# The main program starts from here

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = Movement()
controller.run()

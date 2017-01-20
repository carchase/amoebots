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

top_motor = None
left_motor = None
right_motor = None
top_conn = None
left_conn = None
right_conn = None
back_conn = None

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class Movement (Robot):

  # User defined function for initializing and running
  # the Movement class
  def run(self):
    global top_motor
    global left_motor
    global right_motor
    global top_conn
    global left_conn
    global right_conn
    global back_conn

    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  led = self.getLed('ledname')
    top_motor = self.getMotor("Bending Motor")
    # top_motor.setPosition(float('inf'))
    left_motor = self.getMotor("Left Wheel Motor")
    # left_motor.setPosition(float('inf'))
    right_motor = self.getMotor("Right Wheel Motor")
    # right_motor.setPosition(float('inf'))

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

      # read cmd, vel, delay here!
      
      # Process sensor data here.
      
      # Enter here functions to send actuator commands, like:
      #  led.set(1)
      print action(self, cmd, vel, delay)
    
    # Enter here exit cleanup code

# Signifies which action robot will take
# vel indicates how fast motor will move
# delay indicates the delay prior to the command being terminated
# which may be used to indicate encoder position in the future
def action(self, cmd, vel, delay):
  global top_motor
  global left_motor
  global right_motor

  whichStop = 0

  if cmd == 1:
    move(self, left_motor, vel, 1)
    move(self, right_motor, vel, 1)
    message = 'Moving forward for ' + str(delay)
  elif cmd == 2:
    move(self, left_motor, vel, -1)
    move(self, right_motor, vel, -1)
    message = 'Moving backward for ' + str(delay)
  elif cmd == 3:
    move(self, left_motor, vel, 1)
    move(self, right_motor, vel, -1)
    message = 'Turning left for ' + str(delay)
  elif cmd == 4:
    move(self, left_motor, vel, -1)
    move(self, right_motor, vel, 1)
    message = 'Turning right for ' + str(delay)
  elif cmd == 5:
    move(self, top_motor, vel, 1)
    message = 'Moving the arm down ' + str(delay)
    whichStop = 1
  elif cmd == 6:
    move(self, top_motor, vel, -1)
    message = 'Moving the arm up ' + str(delay)
    whichStop = 1
  elif cmd == 7:
    message = 'Move key out'
    whichStop = 2
  elif cmd == 8:
    message = 'Move key in'
    whichStop = 2
  else:
    message = 'Invalid command ' + str(cmd)

  # delay is used to allow the motor to move for a predetermined
  # amount of time before it's turned off
  self.step(delay)

  # indicates which stop function is called
  if whichStop == 0:
    right_motor.setVelocity(0)
    left_motor.setVelocity(0)
  elif whichStop == 1:
    top_motor.setVelocity(0)

  return message

def move(self, motor, speed, direction):
  # move motor specific speed and direction
  # speed: 0 is off, 255 is full speed
  # direction: 1 clockwise, -1 counter-clockwise

  motor.setPosition(float('inf'))
  motor.setVelocity(direction * speed)

# The main program starts from here

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = Movement()
controller.run()

# File:          eyebot_test.py
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
import time

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class eyebot_test (Robot):

	# User defined function for initializing and running
	# the eyebot_test class
	def run(self):

		# You should insert a getDevice-like function in order to get the
		# instance of a device of the robot. Something like:
		#  led = self.getLed('ledname')

		# initialize camera
		cam = self.getCamera("camera")
		cam.enable(64)

		# initialize sonar sensors
		right_ds = self.getDistanceSensor("right distance sensor")
		right_ds.enable(64)
		left_ds = self.getDistanceSensor("left distance sensor")
		left_ds.enable(64)

		# initialize side connectors
		right_conn = self.getConnector("right connector")
		right_conn.enablePresence(64)
		left_conn = self.getConnector("left connector")
		left_conn.enablePresence(64)
		back_conn = self.getConnector("back connector")
		back_conn.enablePresence(64)
		front_conn = self.getConnector("front connector")
		front_conn.enablePresence(64)

		# initialize wheel motors
		left_wheel = self.getMotor("left wheel motor")
		left_wheel.setPosition(float('inf'))
		right_wheel = self.getMotor("right wheel motor")
		right_wheel.setPosition(float('inf'))
		back_wheel = self.getMotor("back wheel motor")
		back_wheel.setPosition(float('inf'))

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
			# print "right: " + str(right_dist)
			# print "left: " + str(left_dist)

			# Enter here functions to send actuator commands, like:
			#  led.set(1)
			print 'moving forward'
			move('forward', left_wheel, right_wheel, back_wheel)
			self.step(1000)
			print 'moving backwards'
			move('backward', left_wheel, right_wheel, back_wheel)
			self.step(1000)
			print 'turning left'
			move('left', left_wheel, right_wheel, back_wheel)
			self.step(1000)
			print 'turning right'
			move('right', left_wheel, right_wheel, back_wheel)
			self.step(1000)

		# Enter here exit cleanup code

def move(direction, left_wheel, right_wheel, back_wheel):
	if direction == 'forward':
		left_wheel.setVelocity(1)
		right_wheel.setVelocity(1)
		back_wheel.setVelocity(0)
	elif direction == 'backward':
		left_wheel.setVelocity(-1)
		right_wheel.setVelocity(-1)
		back_wheel.setVelocity(0)
	elif direction == 'left':
		left_wheel.setVelocity(0)
		right_wheel.setVelocity(0)
		back_wheel.setVelocity(-1)
	elif direction == 'right':
		left_wheel.setVelocity(0)
		right_wheel.setVelocity(0)
		back_wheel.setVelocity(1)

# The main program starts from here

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = eyebot_test()
controller.run()

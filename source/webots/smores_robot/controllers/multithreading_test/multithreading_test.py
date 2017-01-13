# File:          multithreading_test.py
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
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self):
		print "Starting " + self.name
		print_time(self.name, self.counter, 5)
		print "Exiting " + self.name

def print_time(threadName, delay, counter):
	while counter:
		if exitFlag:
			threadName.exit()
		time.sleep(delay)
		print "%s: %s" % (threadName, time.ctime(time.time()))
		counter -= 1

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class multithreading_test (Robot):

  # User defined function for initializing and running
  # the multithreading_test class
	def run(self):

		# You should insert a getDevice-like function in order to get the
		# instance of a device of the robot. Something like:
		#  led = self.getLed('ledname')
		# Create new threads
		thread1 = myThread(1, "Thread-1", 1)
		thread2 = myThread(2, "Thread-2", 2)

		# Start new Threads
		thread1.start()
		thread2.start()

		# Main loop
		while True:
			# Perform a simulation step of 64 milliseconds
			# and leave the loop when the simulation is over
			if self.step(64) == -1:
			  break

			# Read the sensors:
			# Enter here functions to read sensor data, like:
			#  val = ds.getValue()

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
controller = multithreading_test()
controller.run()

# File:          MyController.py
# Date:          
# Description:   
# Author:        Ben Smith
# Modifications: 

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, LED, DistanceSensor
#
# or to import the entire module. Ex:
#  from controller import *
from controller import Robot
import socket

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class MyController (Robot):
  
  # User defined function for initializing and running
  # the MyController class
  def run(self):
    
    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  led = self.getLed('ledname')
    
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
TCP_IP = '192.168.2.81'
TCP_Port = 4999
BufferSize = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_Port))
s.listen(5)

conn, addr = s.accept()
print('Connection Address: ', addr)
while 1:
    data = conn.recv(BufferSize)
    if not data:
        break
    print('received data: ', data)
    #echo
    conn.send(data)
    conn.close()

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = MyController()
controller.run()



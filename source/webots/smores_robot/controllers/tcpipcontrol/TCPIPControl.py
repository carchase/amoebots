# File:          TCPIPControl.py
# Date:          Ben Smith
# Description:   
# Author:        
# Modifications: 

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, LED, DistanceSensor
#
# or to import the entire module. Ex:
#  from controller import *
from controller import Robot
import socket
import SocketServer

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class TCPIPControl (Robot):
  
  # User defined function for initializing and running
  # the TCPIPControl class
  def run(self):
    
    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  led = self.getLed('ledname')
    main()
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
def main():
    host, port = 'localhost', 5000
    # data = 'My ID is: 1'.join(sys.argv[1:])
    data = 'My ID is: 1'

    # create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server and send data
    sock.connect((host, port))
    sock.send(data + '\n')

    # receive data from the server and shut down.
    received = str(sock.recv(1024)).split()

    print 'Sent:        {}'.format(data)
    print 'Received:    {}'.format(received[0] + ', ' + received[1])

    hostport = SetupNewHostPort(received)

    StartServer(hostport[0], hostport[1])

def SetupNewHostPort(hostport):
    host = hostport[0]
    port = int(hostport[1])
    return host, port

class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #Make calls to the API here. This should handle all the commands.
        #Here are some fake commands for now.
        if(self.data == 'Forward'):
            print 'Forward'
        elif(self.data == 'Left'):
            print 'Left'
        elif(self.data == 'Right'):
            print 'Right'
        elif(self.data == 'Backward'):
            print 'Backward'



def StartServer(host, port):
    # create the server, binding the localhost to the assigned port
    server = SocketServer.TCPServer((host, port), TCPHandler)
    print 'Opening Port on: ', port, '...\n'
    # activate the server and keep it running until told not to.
    server.serve_forever()



def APICommand(command):
    print ('This is a command that will be sent to the API.', command)



# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = TCPIPControl()
controller.run()

# File:          TCPIPControl.py
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
import SocketServer
from time import sleep
from threading import Thread


tcp_command = None
tcp_velocity = None

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions

class TCPIPControl(Robot):
    top_motor = None
    left_motor = None
    right_motor = None
    top_conn = None
    left_conn = None
    right_conn = None
    back_conn = None
    tcp_received = False

    tcp_command = None
    tcp_velocity = None

    # User defined function for initializing and running
    # the TCPIPControl class
    def handle_input(self, cmd, vel):
        if cmd == 1:
            print 'Moving forward'
            self.move_wheels(-vel, -vel, True)
        elif cmd == 2:
            print 'Moving backward'
            self.move_wheels(vel, vel, True)
        elif cmd == 3:
            print 'Turning left'
            self.move_wheels(0, vel, True)
        elif cmd == 4:
            print 'Turning right'
            self.move_wheels(vel, 0, True)
        elif cmd == 5:
            print 'Stopping'
            self.move_wheels(0, 0, False)
        elif cmd == 6:
            print 'Stopping arm'
            self.move_arm(0, False)
        elif cmd == 7:
            print 'Moving arm'  # up?
            self.move_arm(vel, True)
        elif cmd == 8:
            print 'Moving arm'  # down?
            self.move_arm(-vel, True)
        elif cmd == 11:
            print 'Moving forward'
            self.move_wheels(vel, vel, False)
        elif cmd == 12:
            print 'Moving backward'
            self.move_wheels(-vel, -vel, False)
        elif cmd == 13:
            print 'Turning left'
            self.move_wheels(0, vel, False)
        elif cmd == 14:
            print 'Turning right'
            self.move_wheels(vel, 0, False)
        elif cmd == 15:
            print 'Moving arm'  # up?
            self.move_arm(vel, False)
        elif cmd == 16:
            print 'Moving arm'  # down?
            self.move_arm(-vel, False)
        else:
            print 'Invalid command ' + str(cmd)

    def move_wheels(self, left, right, delay):
        self.left_motor.setVelocity(left)
        self.right_motor.setVelocity(right)
        if delay:
            if right != 0 and left != 0:
                self.step(2000)
            else:
                self.step(1000)
            self.move_wheels(0, 0, False)
        else:
            self.tcp_received = False

    def move_arm(self, velocity, delay):
        self.top_motor.setPosition(velocity / 2.0)
        if delay:
            self.step(500)
            self.move_arm(0, False)
        else:
            self.tcp_received = False

    def setup_new_host_port(self, hostport):
        host = hostport[0]
        port = int(hostport[1])
        return host, port

    def connect_to_controller(self):
        host, port = '192.168.2.82', 5000
        # data = 'My ID is: 1'.join(sys.argv[1:])
        # data = (b'{\"type\": \"SMORES\",\"id\": \"1\", \"ip\": \"' + bytes(socket.gethostbyname(socket.gethostname())) + b'\"}')
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

        hostport = self.setup_new_host_port(received)
        server = SocketServer.TCPServer((hostport[0], hostport[-1]), TCPHandler)

        print 'Opening Port on: ', hostport[1], '...\n'
        return server

    def run(self):
        # calls the function which connects the robot to the controller
        server = self.connect_to_controller()

        # You should insert a getDevice-like function in order to get the
        # instance of a device of the robot. Something like:
        #  led = self.getLed('ledname')

        # So, the way this is handled here is stupid, but I have no choice because this is
        # how the devs of Webots decided to make their controller. Anyway, here is the list
        # of commands that will control the different motors on the robot.
        self.top_motor = self.getMotor("Bending Motor")
        self.top_motor.setPosition(float('0'))
        self.left_motor = self.getMotor("Left Wheel Motor")
        self.left_motor.setPosition(float('inf'))
        self.right_motor = self.getMotor("Right Wheel Motor")
        self.right_motor.setPosition(float('inf'))

        self.top_conn = self.getConnector("top conn")
        self.top_conn.enablePresence(64)
        self.left_conn = self.getConnector("left conn")
        self.left_conn.enablePresence(64)
        self.right_conn = self.getConnector("right conn")
        self.right_conn.enablePresence(64)
        self.back_conn = self.getConnector("back conn")
        self.back_conn.enablePresence(64)

        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)

        global tcp_command
        global tcp_velocity

        #Main loop
        while True:
            # Perform a simulation step of 64 milliseconds
            # and leave the loop when the simulation is over
            if self.step(64) == -1:
                break

            # handle one request per loop
            if not self.tcp_received:
                server.handle_request()
                self.tcp_received = True

            # if there was a request, do the command
            if self.tcp_received:
                self.handle_input(tcp_command, tcp_velocity)

            self.step(500)

# The main program starts from here
class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global tcp_velocity
        global tcp_command
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        # Make calls to the API here. This should handle all the commands.
        # Here are some fake commands for now.
        self.data = self.data.split(' ')
        tcp_command = int(self.data[0])
        tcp_velocity = int(self.data[1]) / 100
        self.request.send(b'Got it')
        self.request.close()

# class Thread(threading.Thread):
#     #This class is for multi-threading.
#     #Use this thread like in the following example.
#     #thread1 = myThread(1, "Thread-1", 1)
#     #
#     def __init__(self, ThreadID, name, counter):
#         self.ThreadID = ThreadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print 'Starting: ', self.name
#         print_time(self.name, self.counter, 5)
#         print "Exiting " + self.name

# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             threadName.exit()
#         time.sleep(delay)
#         print "%s: %s" % (threadName, time.ctime(time.time()))
#         counter -= 1
# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.

controller = TCPIPControl()
controller.run()

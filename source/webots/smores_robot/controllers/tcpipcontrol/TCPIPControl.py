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
from threading import Thread, Lock
from multiprocessing import Queue
from time import sleep
import math

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions

class TCPIPControl(Robot):
    # User defined function for initializing and running
    # the TCPIPControl class
    def handle_input(self, cmd, vel, delay):

        # variables for the motors
        self.top_motor = None
        self.left_motor = None
        self.right_motor = None
        self.top_conn = None
        self.left_conn = None
        self.right_conn = None
        self.back_conn = None
        self.gps = None
        self.compass = None

        self.top_motor = self.getMotor("Bending Motor")
        # top_motor.setPosition(float('inf'))
        self.left_motor = self.getMotor("Left Wheel Motor")
        # left_motor.setPosition(float('inf'))
        self.right_motor = self.getMotor("Right Wheel Motor")
        # right_motor.setPosition(float('inf'))

        self.top_conn = self.getConnector("top conn")
        self.top_conn.enablePresence(64)
        self.left_conn = self.getConnector("left conn")
        self.left_conn.enablePresence(64)
        self.right_conn = self.getConnector("right conn")
        self.right_conn.enablePresence(64)
        self.back_conn = self.getConnector("back conn")
        self.back_conn.enablePresence(64)

        self.gps = self.getGPS("gps")
        self.gps.enable(64)
        self.compass = self.getCompass("compass")
        self.compass.enable(64)

        whichStop = 0


        if cmd == 1:
            move(self, left_motor, vel, 1)
            move(self, right_motor, vel, 1)
            message = jsonResponse('text', 'Moving forward for ' + str(delay))
        elif cmd == 2:
            move(self, left_motor, vel, -1)
            move(self, right_motor, vel, -1)
            message = jsonResponse('text', 'Moving backward for ' + str(delay))
        elif cmd == 3:
            move(self, left_motor, vel, 1)
            move(self, right_motor, vel, -1)
            message = jsonResponse('text', 'Turning left for ' + str(delay))
        elif cmd == 4:
            move(self, left_motor, vel, -1)
            move(self, right_motor, vel, 1)
            message = jsonResponse('text', 'Turning right for ' + str(delay))
        elif cmd == 5:
            move(self, top_motor, vel, 1)
            message = jsonResponse('text', 'Moving the arm down ' + str(delay))
            whichStop = 1
        elif cmd == 6:
            move(self, top_motor, vel, -1)
            message = jsonResponse('text', 'Moving the arm up ' + str(delay))
            whichStop = 1
        elif cmd == 7:
            message = jsonResponse('text', 'Move key out')
            whichStop = 2
        elif cmd == 8:
            message = jsonResponse('text', 'Move key in')
            whichStop = 2
        elif cmd == 97:
            message = jsonResponse('text', 'Robot position: ' + str(getPosition(gps)))
        elif cmd == 98:
            message = jsonResponse('text', 'Robot orientation: ' + str(getBearing(compass)))
        elif cmd == 99:
            message = jsonResponse('json', '{\"type\":\"smore\"}')


        # delay is used to allow the motor to move for a predetermined
        # amount of time before it's turned off
        self.step(delay)

        # indicates which stop function is called
        if whichStop == 0:
            self.right_motor.setVelocity(0)
            self.left_motor.setVelocity(0)
        elif whichStop == 1:
            self.top_motor.setVelocity(0)

        return message

    def move(self, motor, speed, direction):
        # move motor specific speed and direction
        # speed: 0 is off, 255 is full speed
        # direction: 1 clockwise, -1 counter-clockwise
        motor.setPosition(float('inf'))
        motor.setVelocity(direction * speed)

    # returns the position of the given gps in a 3d vector <x, y, z>
    def getPosition(gps):
        return gps.getValues()

    # returns the bearing of the given compass in degrees
    def getBearings(compass):
        north = compass.getValues()
        rad = math.atan2(north[0], north[1])
        bearing = (rad - 1.5708) / math.pi * 180.0
        if bearing < 0.0:
            bearing += 360.0
        return bearing

    def jsonResponse(content, data):
        message = "{\"content\":\"" + content + "\",\"data\":\"" + data + "\"}"
        return message

    def setup_new_host_port(self, hostport):
        host = hostport[0]
        port = int(hostport[1])
        return host, port

    def get_address(self):
        # The host gethostbyname method is only working on my (Ben Smith's) computer because the
        # host that it's connecting to is my own computer. This will need to change if the connection
        # is external.
        # host, port = socket.gethostbyname(socket.gethostname()), 5000
        host, port = '10.100.239.200', 5000
        # data = 'My ID is: 1'.join(sys.argv[1:])
        data = (b'{\"type\": \"SMORES\",\"id\": \"1\", \"ip\": \"' + bytes(socket.gethostbyname(socket.gethostname())) + b'\"}')
        # data = 'My ID is: 1'

        # create a socket (SOCK_STREAM means a TCP socket)
        print 'before socket connection'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'after socket connection'
        # connect to the server and send data
        sock.connect((host, port))
        sock.send(data + '\n')

        # receive data from the server and shut down.
        received = str(sock.recv(1024)).split()

        print 'Sent:        {}'.format(data)
        print 'Received:    {}'.format(received[0] + ', ' + received[1])

        return received

    def tcp_server(self, host, port, fromTCPQueue, fromTCPLock, toTCPQueue, toTCPLock):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((host, port))
        except socket.error as msg:
            print "bind failed, error code: ", msg

        print "socket.bind complete."
        s.listen(0)
        conn, addr = s.accept()
        print "connection to: ", conn
        while True:
            data = conn.recv(1024).strip()
            data = data.split(' ')

            print 'Putting command into the queue.'
            fromTCPQueue.put(data)
            fromTCPLock.release()

            toTCPLock.acquire()

            response = toTCPQueue.get()

            print "sending response ", response
            conn.send(bytes(response))

    def run(self):
        print 'Inside the run method.'

        address = self.get_address()

        host = address[0]
        port = int(address[1])
        fromTCPQueue = Queue()
        toTCPQueue = Queue()
        fromTCPLock = Lock()
        toTCPLock = Lock()

        toTCPLock.acquire()
        fromTCPLock.acquire()

        server_thread = Thread(target=self.tcp_server, args=(host, port, fromTCPQueue, fromTCPLock, toTCPQueue, toTCPLock))
        server_thread.start()

        # The queue is where all the commands will be stored and accessed over TCP and in the Simulator.
        # The queue_free is a boolean that lets the program know when the queue is accessible.
        global queue_free

        # Main loop
        while True:
            # Perform a simulation step of 64 milliseconds
            # and leave the loop when the simulation is over
            if self.step(64) == -1:
                break
            # If the queue is free, lock the queue, get the command from the queue
            # lock the queue, and then handle the command.

            fromTCPLock.acquire()
            command = fromTCPQueue.get()

            print "Commands from queue: ", command[0], '...', command[1], '...', command[2]
            # The first two commands are sent to the command function using the command
            # type and then the velocity.
            response = self.handle_input(int(command[0]), int(command[1])/100, int(command[2]))
            toTCPQueue.put(response)
            toTCPLock.release()

            # The command will execute for the specified duration of time.
            # self.step(int(command[2]))
            print 'loop executed'

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.

controller = TCPIPControl()
controller.run()

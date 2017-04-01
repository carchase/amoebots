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

velocity = 1          # in rad/s
cmPerSecond = 5
degPerSecond = 52.5
topDegPerSecond = 57.5

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions

class TCPIPControl(Robot):
    # User defined function for initializing and running
    # the TCPIPControl class
    def handle_input(self, cmd, magnitude):

        # robot id
        self.robot_id = 'robot-1'

        # variables for the motors
        self.top_motor = None
        self.top_wheel_motor = None
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
        top_wheel_motor = self.getMotor("Top Wheel Motor")
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

        # delay to give sensors time to get initial values
        self.step(64)

        if cmd == 1:
            self.move(self.left_motor, velocity, 1)
            self.move(self.right_motor, velocity, 1)
            message = self.jsonResponse('text', 'Moving forward ' + str(magnitude) + ' cm')
        elif cmd == 2:
            self.move(self.left_motor, velocity, -1)
            self.move(self.right_motor, velocity, -1)
            message = self.jsonResponse('text', 'Moving backward ' + str(magnitude) + ' cm')
        elif cmd == 3:
            self.move(self.left_motor, velocity, 1)
            self.move(self.right_motor, velocity, -1)
            message = self.jsonResponse('text', 'Turning left ' + str(magnitude) + ' degrees')
        elif cmd == 4:
            self.move(self.left_motor, velocity, -1)
            self.move(self.right_motor, velocity, 1)
            message = self.jsonResponse('text', 'Turning right ' + str(magnitude) + ' degrees')
        elif cmd == 5:
            self.move(self.top_motor, velocity, 1)
            message = self.jsonResponse('text', 'Moving the arm down ' + str(magnitude) + ' degrees')
            whichStop = 1
        elif cmd == 6:
            self.move(self.top_motor, velocity, -1)
            message = self.jsonResponse('text', 'Moving the arm up ' + str(magnitude) + ' degrees')
            whichStop = 1
        elif cmd == 7:
            self.move(self.top_wheel_motor, velocity, 1)
            message = self.jsonResponse("text", "Spin the arm clockwise " + str(magnitude) + ' degrees')
            whichStop = 1
        elif cmd == 8:
            self.move(self.top_wheel_motor, velocity, -1)
            message = self.jsonResponse("text", "Spin the arm in counterclockwise " + str(magnitude) + ' degrees')
            whichStop = 1
        elif cmd == 9:
            message = self.jsonResponse('text', 'Move key out')
            whichStop = 2
        elif cmd == 10:
            message = self.jsonResponse('text', 'Move key in')
            whichStop = 2
        elif cmd == 90:
            message = self.jsonResponse('robot-info', '{\"type\":\"sim-smores\",\"id\":\"' + self.robot_id + '\"}')
        elif cmd == 92:
            message = self.jsonResponse('sensor-simulator', '{\"id\":\"' + self.robot_id + '\",\"data\":{\"x\":' + str(self.getPosition(self.gps)[0]) + ',\"y\":' + str(self.getPosition(self.gps)[2]) + ',\"heading\":'+ str(self.getBearing(self.compass)) + '} }')
        elif cmd == 99:
            message = self.jsonResponse('json', '{\"type\":\"smore\"}')
        else:
            message = self.jsonResponse('unsupported', '{\"data\":\"command not supported\"}')


        # delay is used to allow the motor to move for a predetermined
        # amount of time before it's turned off
        self.step(self.getDelay(cmd, magnitude))

        # indicates which stop function is called
        if whichStop == 0:
            self.right_motor.setVelocity(0)
            self.left_motor.setVelocity(0)
        elif whichStop == 1:
            self.top_motor.setVelocity(0)

        return message

    def move(self, motor, speed, direction):
        ''' Moves motor specific speed and direction

        Args:
            speed (int): 0 is off, 255 is full speed
            direction(int): 1 clockwise, -1 counter-clockwise
        '''
        motor.setPosition(float('inf'))
        motor.setVelocity(direction * speed)

    def getPosition(self, gps):
        '''
        Returns the position of the given gps in a 3d vector <x, y, z>

        Args:
            gps (GPS): the gps module on the robot
        '''
        return gps.getValues()

    def getBearing(self, compass):
        '''
        Returns the bearing of the given compass in degrees

        Args:
            compass (Compass): the compass module on the robot
        '''
        # get compass value as matrix
        north = compass.getValues()
        # convert to degrees
        rad = math.atan2(north[0], north[1])
        bearing = (rad - 1.5708) / math.pi * 180.0
        if bearing < 0.0:
            bearing += 360.0
        return bearing

    def jsonResponse(self, content, data):
        '''
        Generates a json message to return to the communication level

        Args:
            content (string): the content type to tag the json object
            data (string): the data to place inside the json object
        '''
        if content == 'json':
            message = "{\"content\":\"" + content + "\",\"data\":" + data + "}"
        else:
            message = "{\"content\":\"" + content + "\",\"data\":\"" + data + "\"}"
        return message

    def getDelay(self, cmd, magnitude):
        '''
        Finds the duration of a movement command, given the base speed, to move
        the specified magnitude

        Args:
            cmd (int): the given command
            magnitude (int): the distance to move
        '''
        if cmd == 1 or cmd == 2:
            return int(((1.0 * magnitude) / cmPerSecond) * 1000)
        elif cmd == 3 or cmd == 4:
            return int(((1.0 * magnitude) / degPerSecond) * 1000)
        elif cmd == 5 or cmd == 6:
            return int(((1.0 * magnitude) / topDegPerSecond) * 1000)
        elif cmd == 7 or cmd == 8:
            return int(((1.0 * magnitude) / topDegPerSecond) * 1000)
        else:
            return 1000

    def setup_new_host_port(self, hostport):
        host = hostport[0]
        port = int(hostport[1])
        return host, port

    def get_address(self):
        # The host gethostbyname method is only working on my (Ben Smith's) computer because the
        # host that it's connecting to is my own computer. This will need to change if the connection
        # is external.
        host, port = socket.gethostbyname(socket.gethostname()), 5000
        # host, port = '10.100.239.200', 5000
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

            print "Commands from queue: ", command[0], '...', command[1] #, '...', command[2]
            # The first two commands are sent to the command function using the command
            # type and then the velocity.
            response = self.handle_input(int(command[0]), int(command[1]))# /100, int(command[2]))
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

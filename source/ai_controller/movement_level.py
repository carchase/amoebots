'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Oct 11, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

import random
import math
from time import sleep
from message import Message
from world_model import Grid, Robot, Sensor

class MovementLevel:
    """
    The movement level of the AI controller.  This level consolidates all the sensor data into a
    world model that can be processed by the AI level.  This level also converts high-level
    movement commands into low-level commands that the robots can interpret.

    Args:
        options (dict): The dictionary containing the program settings.

    Attributes:
        options (dict): The dictionary containing the program settings.
        keep_running (bool): Boolean that keeps the main event loop running.
        connections (dict): A dictionary that maps the program levels to their respective queues.
    """

    def __init__(self, options):
        self.options = options
        self.keep_running = True
        self.connections = {}
        self.world_model = Grid(options.get("ARENA_SIZE"), options.get("ARENA_SIZE_CM"))
        self.robots = []
        self.sensors = []
        self.aligned = False

    def movement_level_main(self, mov_input, com_input, ai_input, main_input):
        """
        The main event loop of the movement level.  The loop checks for messages to the level,
        interprets the message, and performs the appropriate action.

        Args:
            mov_input (Queue): The queue for receiving messages in the movement level.
            com_input (Queue): The queue for sending messages to the communication level.
            ai_input (Queue): The queue for sending messages to the AI level.
            main_input (Queue): The queue for sending messages to the main level.
        """

        self.connections['COM_LEVEL'] = ['running', com_input, None]
        self.connections['MOV_LEVEL'] = ['running', mov_input, None]
        self.connections['AI_LEVEL'] = ['running', ai_input, None]
        self.connections['MAIN_LEVEL'] = ['running', main_input, None]

        self.connections["MAIN_LEVEL"][1].put(Message('MOV_LEVEL', 'MAIN_LEVEL', 'info', {
            'message': 'MOV_LEVEL is running'
        }))

        # Infinite loop to keep the process running
        while self.keep_running:
            try:

                # Get items from input queue until it is not empty
                while not self.connections['MOV_LEVEL'][1].empty():

                    message = self.connections['MOV_LEVEL'][1].get()

                    # make sure the response is a list object
                    if isinstance(message, Message):

                        # if the item is a 'add' add the robot to the CON_DICT
                        if message.category == 'command':
                            self.process_command(message)

                        elif message.category == 'response':
                            self.process_response(message)

                        #relay message to destination
                        if message.destination != "MOV_LEVEL":
                            relay_to = self.connections[message.destination][1]
                            relay_to.put(message)

                        elif self.options['DUMP_MSGS_TO_MAIN']:
                            self.connections["MAIN_LEVEL"][1].put(message)

                    else:
                        # un-handled message
                        # send this un-handled message to main
                        # for raw output to the screen
                        self.connections["MAIN_LEVEL"][1].put(message)

                # Check the sensors
                self.check_sensors()

                # Check if align is necessary
                if self.ready_for_align():
                    self.align_robots()

                sleep(self.options["MOV_LOOP_SLEEP_INTERVAL"])

            except Exception as err:
                # Catch all exceptions and log them.
                self.connections["MAIN_LEVEL"][1].put(Message('MOV_LEVEL', 'MAIN_LEVEL', 'error', {
                    'message': str(err)
                }))

                # Raise the exception again so it isn't lost.
                if self.options["RAISE_ERRORS_AFTER_CATCH"]:
                    raise

    def process_command(self, message):
        """
        The command processor of the movement level.  It processes messages categorized as
        "commands".

        Args:
            message (Message): The message object to be processed.
        """

        if message.data.get('directive') == 'add':
            # Determine what kind of connection this is
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', message.origin, 'movement', {
                'command': 90,
                'magnitude': 0,
                'message': "Determine robot info"
            }))

        elif message.category == 'command' and message.data.get('directive') == 'failure':
            # if the item is a 'failure', remove the process from the CON_DICT
            if self.connections.get(message.origin) != None:
                del self.connections[message.origin]

            # TODO: Cleanup sensor/robot failure

        elif message.data.get('directive') == 'shutdown' and message.origin == 'MAIN_LEVEL':
            # The level has been told to shutdown.  Kill all the children!!!
            # Loop over the child processes and shut them shutdown

            self.connections["MAIN_LEVEL"][1].put(Message('MOV_LEVEL', 'MAIN_LEVEL', 'info', {
                'message': 'Shutting down MOV_LEVEL'
            }))

            # End the com_level
            self.keep_running = False

    def process_response(self, message):
        """
        The response processor of the movement level.  It processes messages categorized as
        "response".

        Args:
            message (Message): The message object to be processed.
        """
        if message.data.get("content") == 'robot-info':
            # Configure the movement level to control this device
            if message.data.get('data').get('type') == 'sim-smores':
                self.robots.append(Robot(message.data.get('data').get('id'),
                                         message.origin, message.data.get('data').get('type')))
                self.sensors.append(Sensor(message.data.get('data').get('id'), message.origin,
                                           message.data.get('data').get('type')))
        elif message.data.get("content") == 'sensor-simulator':
            # read position and heading
            for robot in self.robots:
                if robot.robot_id == message.data.get('data').get('id'):
                    robot.position = ((message.data.get('data').get('data').get('x') * 100),
                                      (message.data.get('data').get('data').get('y') * 100))
                    robot.heading = message.data.get('data').get('data').get('heading')
                    old_tile = self.world_model.find_tile(robot)
                    if old_tile != None:
                        old_tile.occupied = None
                    new_tile = self.world_model.get_tile_real_coords(robot.position)
                    new_tile.occupied = robot

                    # Realign the robot after sensor data
                    self.aligned = False

            for sensor in self.sensors:
                if sensor.sensor_id == message.data.get('data').get('id'):
                    sensor.received = True


    def check_sensors(self):
        """
        Send position and heading update commands to all sensors.
        """
        for sensor in self.sensors:
            if not sensor.asked and sensor.sensor_type == 'sim-smores':
                self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', sensor.port_id, 'movement', {
                    'command': 92,
                    'magnitude': 0,
                    'message': 'Get simulator sensor data'
                }))
                sensor.asked = True

    def ready_for_align(self):
        """
        Determine if all the sensors have been read and the robots are
        ready for the alignment process.
        """
        if len(self.robots) < self.options["NUMBER_OF_DEVICES"]:
            return False

        if self.aligned:
            return False

        for sensor in self.sensors:
            if not sensor.received:
                return False

        return True


    def align_robots(self):
        """
        Iterate through all the robots and check if they are misaligned to their
        tiles. If so the misaligned robots are realigned.
        """

        self.aligned = True

        for robot in self.robots:
            # align to grid if necessary
            if (abs(robot.position[0] - self.world_model.find_tile(robot).center[0])
                    > self.options.get('MAX_MISALIGNMENT')
                    or abs(robot.position[1] - self.world_model.find_tile(robot).center[1])
                    > self.options.get('MAX_MISALIGNMENT')):
                self.align(robot)

    def freakout(self, destination):
        """
        Instructs robots to take a number of random moves to "shake" them apart from each other.
        """
        for i in range(5):
            a = random.randint(1, 4)
            t = random.randint(2, 5)
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': a,
                'magnitude': t
            }))

        # Example command
        # self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
        #     'command': 8,
        #     'magnitude': 2,
        #     'message': 'Arm direction 2 spin command'
        # }))

    def align(self, robot):
        """
        Aligns the robot to the center of the tile it's on.
        """
        tile_center = self.world_model.find_tile(robot).center

        # When in doubt, the robot turns left because all angles are from true north (0 to 359)
        turn_center_command = 3
        turn_north_command = 3

        # get angle of center relative to north
        center_heading = get_angle(robot.position, tile_center)

        # get distance to center
        distance_to_center = get_distance(robot.position, tile_center)

        # get the angle to turn to center
        angle_to_center = robot.heading - center_heading

        # make right turn center if left turn > 180
        if angle_to_center > 180:
            angle_to_center = 360 - angle_to_center
            turn_center_command = 4

        # make rught turn to north if left turn > 180
        if center_heading > 180:
            center_heading = 360 - center_heading
            turn_north_command = 4

        # turn to center
        self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', robot.port_id, 'movement', {
            'command': turn_center_command,
            'magnitude': abs(round(angle_to_center)),
            'message': 'Turn to center'
        }))

        # move to center
        self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', robot.port_id, 'movement', {
            'command': 1,
            'magnitude': abs(round(distance_to_center)),
            'message': 'Move to center'
        }))

        # face north
        self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', robot.port_id, 'movement', {
            'command': turn_north_command,
            'magnitude': abs(round(center_heading)),
            'message': 'Turn to center'
        }))

def get_distance(old_position, new_position):
    return math.sqrt((new_position[0] - old_position[0]) ** 2 +
                     (new_position[1] - old_position[1]) ** 2)

def get_angle(old_position, new_position):
    # calculate slope of line between old and new positions
    rise = (new_position[1] - old_position[1])
    run = (new_position[0] - old_position[0])

    # calculate angle between line and x-axis
    inner_angle = math.degrees(math.atan(float(rise) / run))

    # get angle to the north based on quadrant
    if run < 0:
        return inner_angle + 270
    else:
        return inner_angle + 90

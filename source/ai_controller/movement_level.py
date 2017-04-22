'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Oct 11, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

import random
import math
from time import sleep
import jsonpickle
from message import Message
from world_model import Arena, Robot, Sensor

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
        self.world_model = Arena(options["ARENA_SIZE"], options["ARENA_SIZE_CM"])
        self.robots = dict()
        self.sensors = dict()
        self.aligned = False
        self.processing_plan = False
        self.scramble_robots = False

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

                # Scramble robot positions if necessary
                if self.scramble_robots:
                    for port_id, robot in self.robots.items():
                        self.freakout(port_id)
                    self.scramble_robots = False

                # Check the sensors
                self.check_sensors()

                # Check if align is necessary
                if self.ready_for_align():
                    self.align_robots()

                # Send message to move into formation
                if self.aligned and not self.processing_plan:
                    self.connections['AI_LEVEL'][1].put(Message('MOV_LEVEL', 'AI_LEVEL', 'command', {
                        'message': "Submitting world model for pathfinding plan",
                        'directive': "generate-plan",
                        'args': jsonpickle.encode(self.world_model)
                    }))
                    self.processing_plan = True

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

        if message.data['directive'] == 'add':
            # Determine what kind of connection this is
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', message.origin, 'movement', {
                'command': 90,
                'magnitude': 0,
                'message': "Determine robot info"
            }))

        elif message.data["directive"] == 'execute-plan':
            self.process_plan(message.data['args'])

        elif message.category == 'command' and message.data['directive'] == 'failure':
            # if the item is a 'failure', remove the process from the CON_DICT
            if self.connections[message.origin] != None:
                del self.connections[message.origin]

            # TODO: Cleanup sensor/robot failure

        elif message.data['directive'] == 'shutdown' and message.origin == 'MAIN_LEVEL':
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
        if message.data["content"] == 'robot-info':
            # Configure the movement level to control this device
            if message.data['data']['type'] == 'sim-smores':
                self.robots[message.origin] = Robot(None, message.origin,
                                                    message.data['data']['type'])
                self.sensors[message.origin] = Sensor(message.origin,
                                                      message.data['data']['type'])

            elif message.data['data']['type'] == 'smores':
                self.robots[message.origin] = Robot(message.data['data']['id'], message.origin,
                                                    message.data['data']['type'])

            elif message.data['data']['type'] == 'camera':
                self.sensors[message.origin] = Sensor(message.origin,
                                                      message.data['data']['type'])

        elif message.data["content"] == 'sensor-camera':
            print(message.data["data"])
            sensor = self.sensors[message.origin]
            
            if message.data["data"] == {}:
                sensor.asked = False
            else:
                # iterate over robots in the message
                for robot_id in message.data['data']:
                    print(robot_id)
                    # get robot associated with robot_id
                    robot = self.get_robot(robot_id)

                    if robot != None:
                        # read position and heading
                        robot.position = ((message.data["data"][robot_id]['x']),
                                        (message.data["data"][robot_id]['y']))
                        robot.heading = message.data["data"][robot_id]['heading']
                        self.update_tile(robot)

                sensor.received = True
                self.aligned = False

        elif message.data["content"] == 'ping':
            # read position and heading
            robot = self.robots[message.origin]
            
            # make sure that the robot is in position
            if robot.robot_type == "sim-smores":
                robot.position = ((message.data['data']['x'] * 100), (message.data['data']['y'] * 100))
                robot.heading = message.data['data']['heading']
                self.update_tile(robot)

                sensor = self.sensors[message.origin]
                sensor.received = True
                self.aligned = False
            # elif robot.robot_type == "smores":
            #     sensor = self.sensors["CAM_PROCESS"]
            #     sensor.asked = False
            #     sensor.received = False

        elif message.data["content"] == 'move-result':
            robot = self.robots[message.origin]
            robot.queued_commands = robot.queued_commands - 1

            # If it's done moving, ask for it's position again.
            if robot.queued_commands == 0 and robot.robot_type == "sim-smores":
                sensor = self.sensors[message.origin]
                sensor.asked = False
                sensor.received = False
            elif robot.queued_commands == 0 and robot.robot_type == "smores":
                sensor = self.sensors["CAM_PROCESS"]
                sensor.asked = False
                sensor.received = False

    def check_sensors(self):
        """
        Send position and heading update commands to all sensors.
        """

        # Make sure that all the robots have checked
        if len(self.robots) < self.options["NUMBER_OF_DEVICES"]:
            return False

        for port_id, sensor in self.sensors.items():
            if not sensor.asked and sensor.sensor_type == 'sim-smores':
                self.connections['COM_LEVEL'][1].put(
                    Message('MOV_LEVEL', sensor.port_id, 'movement', {
                        'command': 99,
                        'magnitude': 0,
                        'message': 'Get simulator sensor data'
                    }))
            elif not sensor.asked and sensor.sensor_type == 'camera':
                self.connections['COM_LEVEL'][1].put(
                    Message('MOVE_LEVEL', sensor.port_id, 'movement', {
                        'command': 91,
                        'magnitude': 0,
                        'message': 'Get camera sensor data'
                    }))
            sensor.asked = True

    def ready_for_align(self):
        """
        Determine if all the sensors have been read and the robots are
        ready for the alignment process.
        """
        if len(self.robots) < self.options["NUMBER_OF_DEVICES"]:
            return False

        for sensor_id, sensor in self.sensors.items():
            if not sensor.received:
                return False

        for port_id, robot in self.robots.items():
            if robot.queued_commands > 0:
                return False
            if self.world_model.find_tile(robot) is None:
                print("FREAK OUT", robot.robot_id)
                # Robots need to be shaken apart
                self.scramble_robots = True
                return False

        return True


    def align_robots(self):
        """
        Iterate through all the robots and check if they are misaligned to their
        tiles. If so the misaligned robots are realigned.
        """
        misaligned = 0
        for port_id, robot in self.robots.items():
            # align to grid if necessary
            if ((robot.heading > self.options['MAX_NORTH_MISALIGNMENT'] and
                 robot.heading < (360 - self.options['MAX_NORTH_MISALIGNMENT'])) or
                    abs(robot.position[0] - self.world_model.find_tile(robot).center[0])
                    > self.options['MAX_CNTR_MISALIGNMENT']
                    or abs(robot.position[1] - self.world_model.find_tile(robot).center[1])
                    > self.options['MAX_CNTR_MISALIGNMENT']):
                misaligned += 1
                self.aligned = False
                self.align(robot)
        if misaligned == 0:
            self.aligned = True

    def freakout(self, destination):
        """
        Instructs robots to take a number of random moves to "shake" them apart from each other.

        Args:
            Destination (int): the port id of the robot to shake out
        """
        self.robots[destination].queued_commands = self.options['FREAKOUT_ITERATIONS'] * 2
        for count in range(self.options['FREAKOUT_ITERATIONS']):
            # Generate turn command
            action = random.randint(3, 4)
            magnitude = random.randint(0, 180)

            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': action,
                'magnitude': magnitude
            }))

            # Generate move command
            action = 1
            magnitude = random.randint(8, 16)

            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': action,
                'magnitude': magnitude
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

        Args:
            Robot (Robot): the robot to align the the tile center
        """
        tile_center = self.world_model.find_tile(robot).center

        # get angle of center relative to north
        center_heading = get_angle(robot.position, tile_center)

        # get distance to center
        distance_to_center = get_distance(robot.position, tile_center)

        # get the angle to turn to center
        angle_to_center = robot.heading - center_heading

        # make right turn center if left turn > 180
        turn_center_command, angle_to_center = get_turn(angle_to_center)

        # make right turn to north if left turn > 180
        turn_north_command, center_heading = get_turn(center_heading)

        # turn to center
        self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', robot.port_id, 'movement', {
            'command': turn_center_command,
            'magnitude': abs(round(angle_to_center)),
            'message': 'Turn to center'
        }))
        robot.queued_commands += 1

        # move to center
        self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', robot.port_id, 'movement', {
            'command': 1,
            'magnitude': abs(round(distance_to_center)),
            'message': 'Move to center'
        }))
        robot.queued_commands += 1

        # face north
        self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', robot.port_id, 'movement', {
            'command': turn_north_command,
            'magnitude': abs(round(center_heading)),
            'message': 'Turn to center'
        }))
        robot.queued_commands += 1

    def process_plan(self, actions):
        """
        Executes the commands generated by the PDDL in the AI layer.
        For every action in the plan the robots turn to their tile
        destination, move 1 tile length, and then reset their facing
        to north.

        Args:
            actions (Tuple[]): Array of actions generated by the AI
            in order, in the form (command, port ID of robot)
        """

        for action in actions:
            # read command and robot's port id from the action schema
            command = action[0]

            # convert robot number to port_id
            for robot_port_id, robot in self.robots.items():
                if robot.robot_number == action[1]:
                    port_id = robot_port_id
                    robot_obj = robot
                    break

            # get destination angle
            if command == "moveUp":
                turn_dest = 0
            elif command == "moveRight":
                turn_dest = 90
            elif command == "moveDown":
                turn_dest = 180
            elif command == "moveLeft":
                turn_dest = 270

            # turn to destination
            turn_magnitude = robot_obj.heading - turn_dest

            # make right turn center if left turn > 180
            turn_command, turn_magnitude = get_turn(turn_magnitude)

            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', port_id, 'movement', {
                'command': turn_command,
                'magnitude': abs(round(turn_magnitude)),
                'message': 'Turn to destination'
            }))
            self.robots[port_id].queued_commands += 1

            # get destination distance
            distance = round(self.world_model.cm_per_tile)

            # move to destination
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', port_id, 'movement', {
                'command': 1,
                'magnitude': distance,
                'message': 'Move to destination'
            }))
            self.robots[port_id].queued_commands += 1

            # update robot heading
            robot_obj.heading = turn_dest

        # Force everything to realign and then recalculate path
        self.aligned = False
        self.processing_plan = False

    def update_tile(self, robot):
        """
        Update the which tile the robot is on.

        Args:
            robot (Robot): The robot to update
        """
        old_tile = self.world_model.find_tile(robot)
        if old_tile != None:
            old_tile.occupied = None
        new_tile = self.world_model.get_tile_real_coords(robot.position)
        new_tile.occupied = robot

    def get_robot(self, robot_id):
        """
        Get the robot associated with the given robot id

        Args:
            robot_id (int): the robot id to search for
        """
        for port_id, robot in self.robots.items():
            if robot_id == robot.robot_id:
                return robot
        return None

def get_distance(old_position, new_position):
    """
    Returns the Pythagorean distance between two points.

    Args:
        old_position (Tuple): first position, in the form (row, col)
        new_position (Tuple): second position, in the form (row, col)
    """
    return math.sqrt((new_position[0] - old_position[0]) ** 2 +
                     (new_position[1] - old_position[1]) ** 2)

def get_angle(old_position, new_position):
    """
    Calculates the absolute angle between two points, relative to north.
    For example, get_angle((0, 0), (0, -1)) would return 270 degrees,
    the angle from north the line intersecting the two positions forms.

    Args:
        old_position (Tuple): first position, treated as the center coordinate,
        in the form (row, col)
        new_position (Tuple): second position, towards which the intersecting line
        is calculated, in the form (row, col)
    """
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

def switch_turn(old_turn):
    """
    Switchs from a left turn to a right turn and vis versa

    Args:
        old_turn (int): the turn to switch (3 = left, 4 = right)
    """
    if old_turn == 3:
        return 4
    else:
        return 3

def get_turn(turn_magnitude):
    # When in doubt, the robot turns left because all angles are from true north (0 to 359)
    turn_command = 3

    # make right turn if left turn > 180
    if turn_magnitude < 0:
        turn_magnitude = abs(turn_magnitude)
        turn_command = switch_turn(turn_command)

    if turn_magnitude > 180:
        turn_magnitude = 360 - turn_magnitude
        turn_command = switch_turn(turn_command)

    return turn_command, turn_magnitude

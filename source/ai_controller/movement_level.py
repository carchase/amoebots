'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Oct 11, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

from time import sleep
from message import Message

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
        self.first_connect = True
        self.one = True

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
                            # TODO: Process response
                            message.destination = "MAIN_LEVEL"

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

                # Do rest of stuff

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
            if self.first_connect:
                self.first_connect = False
                sleep(12)

            self.cycle_commands(message.origin)

        elif message.category == 'command' and message.data.get('directive') == 'failure':
            # if the item is a 'failure', remove the process from the CON_DICT
            if self.connections.get(message.origin) != None:
                del self.connections[message.origin]

        elif message.data.get('directive') == 'shutdown' and message.origin == 'MAIN_LEVEL':
            # The level has been told to shutdown.  Kill all the children!!!
            # Loop over the child processes and shut them shutdown

            self.connections["MAIN_LEVEL"][1].put(Message('MOV_LEVEL', 'MAIN_LEVEL', 'info', {
                'message': 'Shutting down MOV_LEVEL'
            }))

            # End the com_level
            self.keep_running = False

    def cycle_commands(self, destination):
        """
        A dummy function that cycles all the commands available to the robot.

        Args:
            destination (str): The destination com/tcp port for the commands.
        """

        if self.one:
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': 1,
                'magnitude': 2,
                'message': 'Forward movement command'
            }))
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': 4,
                'magnitude': 2,
                'message': 'Right movement command'
            }))
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': 1,
                'magnitude': 1,
                'message': 'Forward movement command'
            }))
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': 4,
                'magnitude': 5,
                'message': 'Right movement command'
            }))
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': 1,
                'magnitude': 1,
                'message': 'Forward movement command'
            }))
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': 3,
                'magnitude': 5,
                'message': 'Left movement command'
            }))
            self.one = False
        else:
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': 1,
                'magnitude': 2,
                'message': 'Forward movement command'
            }))
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': 3,
                'magnitude': 2,
                'message': 'Left movement command'
            }))
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': 1,
                'magnitude': 1,
                'message': 'Forward movement command'
            }))
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': 3,
                'magnitude': 5,
                'message': 'Left movement command'
            }))
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': 1,
                'magnitude': 1,
                'message': 'Forward movement command'
            }))
            self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
                'command': 4,
                'magnitude': 5,
                'message': 'Right movement command'
            }))
            self.one = True

        # self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
        #     'command': 5,
        #     'velocity': 150,
        #     'duration': .5,
        #     'message': 'Arm direction 1 movement command'
        # }))
        # self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
        #     'command': 6,
        #     'velocity': 150,
        #     'duration': .5,
        #     'message': 'Arm direction 2 movement command'
        # }))
        # self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
        #     'command': 7,
        #     'velocity': 150,
        #     'duration': 2,
        #     'message': 'Arm direction 1 spin command'
        # }))
        # self.connections['COM_LEVEL'][1].put(Message('MOV_LEVEL', destination, 'movement', {
        #     'command': 8,
        #     'velocity': 150,
        #     'duration': 2,
        #     'message': 'Arm direction 2 spin command'
        # }))

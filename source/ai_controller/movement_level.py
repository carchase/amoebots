'''
This file contains the code for managing the world model.  It updates the world model
with data from the communication level and gives the model to the AI level.  It also
converts AI movement commands into low-level commands which are sent to the
communication level.

Created on Oct 11, 2016
View the full repository here https://github.com/car-chase/amoebots
'''

from time import sleep
from message import Message

class movement_level:
    con_dict = {}

    def __init__(self, options):
        self.options = options
        self.infinite_loop = True

    def movement_level_main(self, mov_input, com_input, ai_input, main_input):
        self.con_dict['COM_LEVEL'] = com_input
        self.con_dict['MOV_LEVEL'] = mov_input
        self.con_dict['AI_LEVEL'] = ai_input
        self.con_dict['MAIN_LEVEL'] = main_input

        self.con_dict["MAIN_LEVEL"].put(Message('MOV_LEVEL', 'MAIN_LEVEL', 'info', {
            'message': 'Movement_level is running'
        }))

        # Infinite loop to keep the process running
        while self.infinite_loop:
            try:

                # Get items from input queue until it is not empty
                while not self.con_dict['MOV_LEVEL'].empty():

                    message = self.con_dict['MOV_LEVEL'].get()

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
                            relay_to = self.con_dict[message.destination][0]
                            relay_to.put(message)

                        elif self.options['DUMP_MSGS_TO_MAIN']:
                            self.con_dict["MAIN_LEVEL"].put(message)

                    else:
                        # un-handled message
                        # send this un-handled message to main
                        # for raw output to the screen
                        self.con_dict["MAIN_LEVEL"].put(message)

                # Do rest of stuff

                sleep(.1)

            except Exception as err:
                self.con_dict["MAIN_LEVEL"].put(Message('MOV_LEVEL', 'MAIN_LEVEL', 'error', {
                    'message': str(err)
                }))

    def process_command(self, message):

        if message.data.get('directive') == 'add':
            self.cycle_commands(message.origin)

        elif message.category == 'command' and message.data.get('directive') == 'failure':
            # if the item is a 'failure', remove the process from the CON_DICT
            if self.con_dict.get(message.origin) != None:
                del self.con_dict[message.origin]

        elif message.data.get('directive') == 'shutdown' and message.origin == 'MAIN_LEVEL':
            # The level has been told to shutdown.  Kill all the children!!!
            # Loop over the child processes and shut them shutdown

            self.con_dict["MAIN_LEVEL"].put(Message('MOV_LEVEL', 'MAIN_LEVEL', 'info', {
                'message': 'Shutting down MOV_LEVEL'
            }))

            # End the com_level
            self.infinite_loop = False

    def cycle_commands(self, destination):
        self.con_dict['COM_LEVEL'].put(Message('MOV_LEVEL', destination, 'movement', {
            'command': 1,
            'velocity': 150,
            'duration': 2,
            'message': 'Forward movement command'
        }))
        self.con_dict['COM_LEVEL'].put(Message('MOV_LEVEL', destination, 'movement', {
            'command': 2,
            'velocity': 150,
            'duration': 2,
            'message': 'Backward movement command'
        }))
        self.con_dict['COM_LEVEL'].put(Message('MOV_LEVEL', destination, 'movement', {
            'command': 3,
            'velocity': 150,
            'duration': 2,
            'message': 'Left movement command'
        }))
        self.con_dict['COM_LEVEL'].put(Message('MOV_LEVEL', destination, 'movement', {
            'command': 4,
            'velocity': 150,
            'duration': 2,
            'message': 'Right movement command'
        }))
        self.con_dict['COM_LEVEL'].put(Message('MOV_LEVEL', destination, 'movement', {
            'command': 5,
            'velocity': 150,
            'duration': .5,
            'message': 'Arm direction 1 movement command'
        }))
        self.con_dict['COM_LEVEL'].put(Message('MOV_LEVEL', destination, 'movement', {
            'command': 6,
            'velocity': 150,
            'duration': .5,
            'message': 'Arm direction 2 movement command'
        }))
        self.con_dict['COM_LEVEL'].put(Message('MOV_LEVEL', destination, 'movement', {
            'command': 7,
            'velocity': 150,
            'duration': 2,
            'message': 'Arm direction 1 movement command'
        }))
        self.con_dict['COM_LEVEL'].put(Message('MOV_LEVEL', destination, 'movement', {
            'command': 8,
            'velocity': 150,
            'duration': 2,
            'message': 'Arm direction 2 movement command'
        }))

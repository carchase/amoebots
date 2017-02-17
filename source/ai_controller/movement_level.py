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

CON_DICT = {}
INFINITE_LOOP = True

def movement_level_main(MOV_INPUT, COM_INPUT, AI_INPUT, MAIN_INPUT, DUMP_MSGS_TO_MAIN):
    MAIN_INPUT.put(Message('MOV_LEVEL', 'MAIN_INPUT', 'info', {
        'message': 'Movement_level is running'
    }))

    CON_DICT['COM_LEVEL'] = COM_INPUT
    CON_DICT['MOV_LEVEL'] = MOV_INPUT
    CON_DICT['AI_LEVEL'] = AI_INPUT
    CON_DICT['MAIN_LEVEL'] = MAIN_INPUT

    global INFINITE_LOOP
    INFINITE_LOOP = True

    # Infinite loop to keep the process running
    while INFINITE_LOOP:
        try:

            # Get items from input queue until it is not empty
            while not MOV_INPUT.empty():

                message = MOV_INPUT.get()

                # make sure the response is a list object
                if isinstance(message, Message):

                    # if the item is a 'add' add the robot to the CON_DICT
                    if message.category == 'command':
                        process_command(message)

                    elif message.category == 'response':
                        # TODO: Process response
                        message.destination = "MAIN_LEVEL"

                    #relay message to destination
                    if message.destination != "MOV_LEVEL":
                        relay_to = CON_DICT[message.destination][0]

                        relay_to.put(message)

                    elif DUMP_MSGS_TO_MAIN:
                        MAIN_INPUT.put(message)


                # un-handled message
                else:

                    # send this un-handled message to main
                    # for raw output to the screen
                    MAIN_INPUT.put(message)

            # Do rest of stuff

            sleep(.1)

        except Exception as err:
            MAIN_INPUT.put(Message('MOV_LEVEL', 'MAIN_LEVEL', 'error', {'message': str(err)}))

def process_command(message):

    if message.data.get('directive') == 'add':
        CON_DICT['COM_LEVEL'].put(Message('MOV_LEVEL', message.origin, 'movement', {
            'command': 1,
            'velocity': 150,
            'duration': 2,
            'message': 'Forward movement command'
        }))
        CON_DICT['COM_LEVEL'].put(Message('MOV_LEVEL', message.origin, 'movement', {
            'command': 2,
            'velocity': 150,
            'duration': 2,
            'message': 'Backward movement command'
        }))
        CON_DICT['COM_LEVEL'].put(Message('MOV_LEVEL', message.origin, 'movement', {
            'command': 3,
            'velocity': 150,
            'duration': 2,
            'message': 'Left movement command'
        }))
        CON_DICT['COM_LEVEL'].put(Message('MOV_LEVEL', message.origin, 'movement', {
            'command': 4,
            'velocity': 150,
            'duration': 2,
            'message': 'Right movement command'
        }))
        # CON_DICT['COM_LEVEL'].put(Message('MOV_LEVEL', response.origin, 'movement', {
        #     'command': 5,
        #     'velocity': 150,
        #     'duration': .5,
        #     'message': 'Arm direction 1 movement command'
        # }))
        # CON_DICT['COM_LEVEL'].put(Message('MOV_LEVEL', response.origin, 'movement', {
        #     'command': 6,
        #     'velocity': 150,
        #     'duration': .5,
        #     'message': 'Arm direction 2 movement command'
        # }))
        # CON_DICT['COM_LEVEL'].put(Message('MOV_LEVEL', response.origin, 'movement', {
        #     'command': 7,
        #     'velocity': 150,
        #     'duration': 2,
        #     'message': 'Arm direction 1 movement command'
        # }))
        # CON_DICT['COM_LEVEL'].put(Message('MOV_LEVEL', response.origin, 'movement', {
        #     'command': 8,
        #     'velocity': 150,
        #     'duration': 2,
        #     'message': 'Arm direction 2 movement command'
        # }))

    elif message.category == 'command' and message.data.get('directive') == 'failure':
        # if the item is a 'failure', remove the process from the CON_DICT
        if CON_DICT.get(message.origin) != None:
            del CON_DICT[message.origin]

    elif message.data.get('directive') == 'shutdown' and message.origin == 'MAIN_LEVEL':
        # the level has been told to shutdown.  Kill all the children!!!
        # Loop over the child processes and shut them shutdown

        CON_DICT["MAIN_LEVEL"].put(Message('AI_LEVEL', 'MAIN_LEVEL', 'info', {
            'message': 'Shutting down AI level'
        }))

        # End the com_level
        global INFINITE_LOOP
        INFINITE_LOOP = False
'''
This file contains the code for the AI control algorithms.

Created on Oct 11, 2016
View the full repository here https://github.com/car-chase/amoebots
'''

from time import sleep
from message import Message

CON_DICT = {}
INFINITE_LOOP = True

def ai_level_main(AI_INPUT, MOV_INPUT, MAIN_INPUT, DUMP_MSGS_TO_MAIN):
    MAIN_INPUT.put(Message('AI_LEVEL', 'MAIN_LEVEL', 'info', {'message': 'AI_level is running'}))

    CON_DICT['AI_LEVEL'] = ['running', AI_INPUT, None]
    CON_DICT['MOV_LEVEL'] = ['running', MOV_INPUT, None]
    CON_DICT['MAIN_LEVEL'] = ['running', MAIN_INPUT, None]

    global INFINITE_LOOP
    INFINITE_LOOP = True

    # Infinite loop to keep the process running
    while INFINITE_LOOP:
        try:
            # Get items from input queue until it is not empty
            while not AI_INPUT.empty():

                message = AI_INPUT.get()

                # make sure the message is a Message object
                if isinstance(message, Message):

                    # Appropriately process the message depending on its category
                    if message.category == 'command':
                        process_command(message)

                    # relay message to destination
                    if message.destination != "AI_LEVEL":
                        relay_to = CON_DICT[message.destination][1]

                        relay_to.put(message)

                    elif DUMP_MSGS_TO_MAIN:
                        MAIN_INPUT.put(message)

            # Do rest of stuff

            sleep(.1)

        except Exception as err:
            MAIN_INPUT.put(Message('AI_LEVEL', 'MAIN_LEVEL', 'error', {'message': str(err)}))

def process_command(message):
    if message.data.get('directive') == 'shutdown' and message.origin == 'MAIN_LEVEL':
        # the level has been told to shutdown.  Kill all the children!!!
        # Loop over the child processes and shut them shutdown

        CON_DICT["MAIN_LEVEL"][1].put(Message('AI_LEVEL', 'MAIN_LEVEL', 'info', {
            'message': 'Shutting down AI level'
        }))

        # End the com_level
        global INFINITE_LOOP
        INFINITE_LOOP = False

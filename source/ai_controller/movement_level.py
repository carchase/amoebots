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

MOV_DICT = {}

def movement_level_main(MOV_INPUT, COM_INPUT, AI_INPUT, MAIN_INPUT):
    MAIN_INPUT.put(Message('MOV_LEVEL', 'MAIN_INPUT', 'info', {
        'message': 'Movement_level is running'
    }))

    MOV_DICT['COM_LEVEL'] = COM_INPUT
    MOV_DICT['MOV_LEVEL'] = MOV_INPUT
    MOV_DICT['AI_LEVEL'] = AI_INPUT
    MOV_DICT['MAIN_LEVEL'] = MAIN_INPUT

    # Infinite loop to keep the process running
    while True:
        try:

            # Get items from input queue until it is not empty
            while not MOV_INPUT.empty():

                response = MOV_INPUT.get()

                # make sure the response is a list object
                if isinstance(response, Message):

                    # if the item is a 'add' add the robot to the MOV_DICT
                    if response.category == 'command' and response.data.get('directive') == 'add':
                        MOV_DICT[response.origin] = [COM_INPUT]
                        COM_INPUT.put(Message('MOV_LEVEL', response.origin, 'movement', {
                            'command': 1,
                            'velocity': 150,
                            'duration': 2,
                            'message': 'Forward movement command'
                        }))
                        COM_INPUT.put(Message('MOV_LEVEL', response.origin, 'movement', {
                            'command': 2,
                            'velocity': 150,
                            'duration': 2,
                            'message': 'Backward movement command'
                        }))
                        COM_INPUT.put(Message('MOV_LEVEL', response.origin, 'movement', {
                            'command': 3,
                            'velocity': 150,
                            'duration': 2,
                            'message': 'Left movement command'
                        }))
                        COM_INPUT.put(Message('MOV_LEVEL', response.origin, 'movement', {
                            'command': 4,
                            'velocity': 150,
                            'duration': 2,
                            'message': 'Right movement command'
                        }))
                        # COM_INPUT.put(Message('MOV_LEVEL', response.origin, 'movement', {
                        #     'command': 5,
                        #     'velocity': 150,
                        #     'duration': .5,
                        #     'message': 'Arm direction 1 movement command'
                        # }))
                        # COM_INPUT.put(Message('MOV_LEVEL', response.origin, 'movement', {
                        #     'command': 6,
                        #     'velocity': 150,
                        #     'duration': .5,
                        #     'message': 'Arm direction 2 movement command'
                        # }))
                        # COM_INPUT.put(Message('MOV_LEVEL', response.origin, 'movement', {
                        #     'command': 7,
                        #     'velocity': 150,
                        #     'duration': 2,
                        #     'message': 'Arm direction 1 movement command'
                        # }))
                        # COM_INPUT.put(Message('MOV_LEVEL', response.origin, 'movement', {
                        #     'command': 8,
                        #     'velocity': 150,
                        #     'duration': 2,
                        #     'message': 'Arm direction 2 movement command'
                        # }))

                    elif (response.category == 'command'
                          and response.data.get('directive') == 'failure'):
                        # if the item is a 'failure', remove the process from the MOV_DICT
                        if MOV_DICT.get(response.origin) != None:
                            del MOV_DICT[response.origin]

                    elif response.category == 'response':
                        # TODO: Process response
                        response.destination = "MAIN_LEVEL"

                    #relay message to destination
                    if response.destination != "MOV_LEVEL":
                        relay_to = MOV_DICT[response.destination][0]

                        relay_to.put(response)

                    else:
                        MAIN_INPUT.put(response)


                # un-handled message
                else:

                    # send this un-handled message to main
                    # for raw output to the screen
                    MAIN_INPUT.put(response)

            # Do rest of stuff

            sleep(.1)

        except Exception as err:
            MAIN_INPUT.put(Message('MOV_LEVEL', 'MAIN_LEVEL', 'error', {'message': str(err)}))

'''
This file contains the code for managing the world model.  It updates the world model
with data from the communication level and gives the model to the AI level.  It also 
converts AI movement commands into low-level commands which are sent to the 
communication level.

Created on Oct 11, 2016
View the full repository here https://github.com/car-chase/amoebots
'''

from multiprocessing import Process, Queue
from time import sleep

MOV_DICT = {}

def movement_level_main(MOV_INPUT, COM_INPUT, AI_INPUT, MAIN_INPUT):
    MAIN_INPUT.put({
        'destination': 'MAIN_INPUT',
        'type': 'info',
        'origin': 'MOV_LEVEL',
        'message': 'Movement_level is running'
    })

    MOV_DICT['COM_INPUT'] = [COM_INPUT]
    MOV_DICT['MOV_INPUT'] = [MOV_INPUT]
    MOV_DICT['AI_INPUT'] = [AI_INPUT]
    MOV_DICT['MAIN_INPUT'] = [MAIN_INPUT]

    # Infinite loop to keep the process running
    while(True):

        # Get items from input queue until it is not empty
        while not MOV_INPUT.empty():
            
            RESPONSE = MOV_INPUT.get()

            # make sure the response is a list object
            if isinstance(RESPONSE, dict):
                
                # if the item is a 'add' add the robot to the MOV_DICT
                if RESPONSE.get('type') == 'command' and RESPONSE.get('message') == 'add':
                    MOV_DICT[RESPONSE['origin']] = [COM_INPUT]
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '2 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '1 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '3 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '4 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '7 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '8 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '2 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '1 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '3 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '4 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '7 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '8 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '2 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '1 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '3 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '4 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '7 150'
                    })
                    COM_INPUT.put({
                        'destination': RESPONSE['origin'],
                        'type': 'command',
                        'origin': 'MOV_LEVEL',
                        'message': '8 150'
                    })

                elif RESPONSE.get('type') == 'command' and RESPONSE['message'] == 'failure':
                    # if the item is a 'failure', remove the process from the MOV_DICT
                    if MOV_DICT.get(RESPONSE.get('origin')) != None:
                        del MOV_DICT[RESPONSE.get('origin')]

                elif RESPONSE.get('type') == 'result':

                    # forward to the mov level
                    RESPONSE['destination'] = "MOV_INPUT"

                #relay message to destination
                if RESPONSE['destination'] != "MOV_INPUT":
                    RELAY_TO = CON_DICT[RESPONSE['destination']][1]

                    RELAY_TO.put(RESPONSE)

                else:
                    MAIN_INPUT.put(RESPONSE)


            # un-handled message
            else:

                # send this un-handled message to main
                # for raw output to the screen
                MAIN_INPUT.put(RESPONSE)
        # Do rest of stuff

        sleep(.5)
'''
This file contains the code for managing the world model.  It updates the world model
with data from the communication level and gives the model to the AI level.  It also 
converts AI movement commands into low-level commands which are sent to the 
communication level.

Created on Oct 11, 2016
View the full repository here https://github.com/car-chase/amoebots
'''

MOV_DICT = None

from multiprocessing import Process, Queue
from time import sleep

def movement_level_main(MOV_INPUT, COM_INPUT, AI_INPUT, MAIN_INPUT):
    MAIN_INPUT.put({
        'destination': 'MAIN_INPUT',
        'type': 'info',
        'origin': 'mov_level',
        'message': 'Movement_level is running'
    })

    # Infinite loop to keep the process running
    while(True):

        # Get items from input queue until it is not empty
        while not MOV_INPUT.empty():
            MAIN_INPUT.put(MOV_INPUT.get()) # For now just parrot

            
        # Do rest of stuff

        sleep(1)
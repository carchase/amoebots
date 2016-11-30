'''
This file contains the code for the AI control algorithms.

Created on Oct 11, 2016
View the full repository here https://github.com/car-chase/amoebots
'''

from multiprocessing import Process, Queue
from time import sleep

def ai_level_main(AI_INPUT, MOV_INPUT, MAIN_INPUT):
    MAIN_INPUT.put({
        'destination': 'MAIN_INPUT',
        'type': 'info',
        'origin': 'AI_LEVEL',
        'message': 'AI_level is running'
    })
    
    # Infinite loop to keep the process running
    while(True):

        # Get items from input queue until it is not empty
        while not MAIN_INPUT.empty():
            MAIN_INPUT.put(AI_INPUT.get()) # For now just parrot

        # Do rest of stuff

        sleep(1)
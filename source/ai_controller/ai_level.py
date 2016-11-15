'''
This file contains the code for the AI control algorithms.

Created on Oct 11, 2016
View the full repository here https://github.com/car-chase/amoebots
'''

from multiprocessing import Process, Queue
from time import sleep

def ai_level_main(AI_INPUT, TO_MOVEMENT, TO_MAIN):
    TO_MAIN.put({
        'type': 'info',
        'origin': 'ai__level',
        'message': 'AI_level is running'
    })
    
    # Infinite loop to keep the process running
    while(True):

        # Get items from input queue until it is not empty
        while not AI_INPUT.empty():
            TO_MAIN.put(AI_INPUT.get()) # For now just parrot

        # Do rest of stuff

        sleep(1)
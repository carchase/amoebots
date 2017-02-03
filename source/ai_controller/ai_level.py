'''
This file contains the code for the AI control algorithms.

Created on Oct 11, 2016
View the full repository here https://github.com/car-chase/amoebots
'''

from time import sleep
from message import Message

def ai_level_main(AI_INPUT, MOV_INPUT, MAIN_INPUT):
    MAIN_INPUT.put(Message('AI_LEVEL', 'MAIN_LOG', 'info', {'message': 'AI_level is running'}))

    # Infinite loop to keep the process running
    while True:
        try:
            # Get items from input queue until it is not empty
            while not MAIN_INPUT.empty():
                MAIN_INPUT.put(AI_INPUT.get()) # For now just parrot

            # Do rest of stuff

            sleep(1)

        except Exception as err:
            MAIN_INPUT.put(Message('AI_LEVEL', 'MAIN_LOG', 'error', {'message': str(err)}))

'''
This file contains the code for main.  It starts the two main processes (bot_listener)
and controller.

Created on Nov 1, 2016
View the full repository here https://github.com/car-chase/amoebots
'''

from multiprocessing import Process, Queue, Array

import communication_level
import movement_level
import ai_level

# Make the global queues
MAIN_INPUT_QUEUE = Queue()
COM_INPUT_QUEUE = Queue()
MOVEMENT_INPUT_QUEUE = Queue()
AI_INPUT_QUEUE = Queue()

if __name__ == "__main__":
    # Instantiate the processes
    COMMUNICATION_LEVEL = Process(target=communication_level.com_level_main, args=(MAIN_INPUT_QUEUE, COM_INPUT_QUEUE, MOVEMENT_INPUT_QUEUE))

    # Start the event loop on the movement_level
    COMMUNICATION_LEVEL.start()

    # Start the event loop on the communication_level

    # Start the event loop on the ai_level
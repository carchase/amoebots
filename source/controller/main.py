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
TO_PROCESSES = Queue()
FROM_PROCESSES = Queue()
TO_COM_LEVEL = Queue()
FROM_COM_LEVEL = Queue()

if __name__ == "__main__":
    # Instantiate the processes
    COMMUNICATION_LEVEL = Process(target=communication_level.com_level_main, args=(FROM_PROCESSES, TO_PROCESSES, TO_COM_LEVEL, FROM_COM_LEVEL))

    # Start the event loop on the movement_level
    COMMUNICATION_LEVEL.start()

    # Start the event loop on the communication_level

    # Start the event loop on the ai_level
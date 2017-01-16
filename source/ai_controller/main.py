'''
This file contains the code for main.  It starts the two main processes (bot_listener)
and controller.

Created on Nov 1, 2016
View the full repository here https://github.com/car-chase/amoebots
'''

from multiprocessing import Process, Queue
from time import sleep

import communication_level
import movement_level
import ai_level

def mainLoop():
    # Make the global queues
    MAIN_INPUT_QUEUE = Queue()
    COM_INPUT_QUEUE = Queue()
    MOVEMENT_INPUT_QUEUE = Queue()
    AI_INPUT_QUEUE = Queue()

    # Instantiate the processes
    COMMUNICATION_LEVEL = Process(target=communication_level.com_level_main, args=(COM_INPUT_QUEUE, MOVEMENT_INPUT_QUEUE, MAIN_INPUT_QUEUE))
    MOVEMENT_LEVEL = Process(target=movement_level.movement_level_main, args=(MOVEMENT_INPUT_QUEUE, COM_INPUT_QUEUE, AI_INPUT_QUEUE, MAIN_INPUT_QUEUE))
    AI_LEVEL = Process(target=ai_level.ai_level_main, args=(AI_INPUT_QUEUE, MOVEMENT_INPUT_QUEUE, MAIN_INPUT_QUEUE))
    
    # Start the processes
    COMMUNICATION_LEVEL.start()
    MOVEMENT_LEVEL.start()
    AI_LEVEL.start()

    # Infinite loop to keep checking the queue for information
    while(True):
        
        # Check the main input queue and display logs
        checkLogs(MAIN_INPUT_QUEUE)
        
        sleep(.1)

def checkLogs(MAIN_INPUT_QUEUE):
    while not MAIN_INPUT_QUEUE.empty():
        chunk = MAIN_INPUT_QUEUE.get()
        
        # Ensure that the message is a log message
        if type(chunk) is dict and chunk.get('type') != None and chunk.get('message') != None and chunk.get('origin') != None and chunk.get('destination') != None:
            print('To: ', chunk['destination'] + '\tFrom: ', chunk['origin'], chunk['type'] + ': ', chunk['message'])
        else:
            # Otherwise print out the raw data
            print('raw:', chunk)

if __name__ == "__main__":
    mainLoop()
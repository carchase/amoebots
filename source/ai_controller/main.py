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
from message import Message

def main_loop():
    # Make the global queues
    main_queue = Queue()
    com_input_queue = Queue()
    mov_input_queue = Queue()
    ai_input_queue = Queue()

    # Instantiate the processes
    com_level_process = Process(target=communication_level.com_level_main,
                                args=(com_input_queue, mov_input_queue, main_queue))
    mov_level_process = Process(target=movement_level.movement_level_main,
                                args=(mov_input_queue, com_input_queue, ai_input_queue, main_queue))
    ai_level_process = Process(target=ai_level.ai_level_main,
                               args=(ai_input_queue, mov_input_queue, main_queue))

    # Start the processes
    com_level_process.start()
    mov_level_process.start()
    ai_level_process.start()

    # Infinite loop to keep checking the queue for information
    while True:

        # Check the main input queue and display logs
        check_logs(main_queue)

        sleep(.1)

def check_logs(log_queue):
    while not log_queue.empty():
        chunk = log_queue.get()

        # Ensure that the message is a log message
        if isinstance(chunk, Message):
            print(chunk.to_string())
        else:
            # Otherwise print out the raw data
            print('RAW:', chunk)

if __name__ == "__main__":
    main_loop()

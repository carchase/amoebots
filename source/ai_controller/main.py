'''
This file contains the code for main.  It starts the two main processes (bot_listener)
and controller.

Created on Nov 1, 2016
View the full repository here https://github.com/car-chase/amoebots
'''

from multiprocessing import Process, Queue
from time import sleep
import signal
import inspect

import communication_level
import movement_level
import ai_level
from message import Message

CON_DICT = {}

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

    # Add the processes to the connection map
    CON_DICT["COM_LEVEL"] = ["running", com_input_queue, com_level_process]
    CON_DICT["MOV_LEVEL"] = ["running", mov_input_queue, mov_level_process]
    CON_DICT["AI_LEVEL"] = ["running", ai_input_queue, ai_level_process]

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

def signal_handler(signal, frame):
    # Get the origin of the SIGINT
    origin = inspect.getouterframes(frame)[0].function

    # Initilize shutdown only once, if the signal is from the main frame
    if origin == "main_loop":
        print("Initiating shutdown")

        # Loop over the child processes and shut them shutdown
        for key in CON_DICT:
            CON_DICT[key][1].put(Message('MAIN_LEVEL', key, 'command', {
                'message': 'Issuing shutdown command to ' + key,
                'directive': 'shutdown',
            }))
            # CON_DICT[key][2].join()
            # CON_DICT[key][0] = "stopped"

    # Don't do anything for the other frames

# Reigister the SIGINT signal handler
# This captures a ctrl+c and causes the controller to shutdown.
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    main_loop()

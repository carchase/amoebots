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

# ***************** Constants used to configure the controller *****************
OPTIONS = {
    'DUMP_MSGS_TO_MAIN': False, # Show all messages in main log output
    'NUMBER_OF_DEVICES': 5 # The number of devices that the controller expects to use
}
# ******************************************************************************

CON_DICT = {}
INFINITE_LOOP = True
MAIN_QUEUE = Queue()

def main_loop():

    init_levels()

    global INFINITE_LOOP
    INFINITE_LOOP = True

    # Infinite loop to keep checking the queue for information
    while INFINITE_LOOP:

        # Check the main input queue and display logs
        check_messages()

        sleep(.1)

def init_levels():
    # Make the queues
    com_input_queue = Queue()
    mov_input_queue = Queue()
    ai_input_queue = Queue()

    # Instantiate the levels
    mov_level = movement_level.movement_level(OPTIONS)

    # Instantiate the processes
    com_level_process = Process(target=communication_level.com_level_main,
                                args=(com_input_queue, mov_input_queue,
                                      MAIN_QUEUE, OPTIONS))
    mov_level_process = Process(target=mov_level.movement_level_main,
                                args=(mov_input_queue, com_input_queue, ai_input_queue, MAIN_QUEUE))
    ai_level_process = Process(target=ai_level.ai_level_main,
                               args=(ai_input_queue, mov_input_queue,
                                     MAIN_QUEUE, OPTIONS))

    # Start the processes
    com_level_process.start()
    mov_level_process.start()
    ai_level_process.start()

    # Add the processes to the connection map
    CON_DICT["COM_LEVEL"] = ["running", com_input_queue, com_level_process]
    CON_DICT["MOV_LEVEL"] = ["running", mov_input_queue, mov_level_process]
    CON_DICT["AI_LEVEL"] = ["running", ai_input_queue, ai_level_process]

def check_messages():
    while not MAIN_QUEUE.empty():
        message = MAIN_QUEUE.get()

        # Ensure that the message is a log message
        if isinstance(message, Message):
            print(message.to_string())
        else:
            # Otherwise print out the raw data
            print('RAW:', message)

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
            CON_DICT[key][2].join()
            CON_DICT[key][0] = "stopped"
            check_messages()

        # Check the logs one last time
        check_messages()

        # End the com_level
        global INFINITE_LOOP
        INFINITE_LOOP = False

    # Don't do anything for the other frames

# Reigister the SIGINT signal handler
# This captures a ctrl+c and causes the controller to shutdown.
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    main_loop()

'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Feb 24, 2017

View the full repository here https://github.com/car-chase/amoebots
'''

from multiprocessing import Process, Queue
from time import sleep
from communication_level import CommunicationLevel
from movement_level import MovementLevel
from ai_level import AiLevel
from message import Message

class MainLevel:
    """
    The main level of the AI controller.  This level handles the creation of the lower levels,
    manages the lower levels, and consolidates log messages.

    Args:
        options (dict): The dictionary containing the program settings.

    Attributes:
        options (dict): The dictionary containing the program settings.
        keep_running (bool): Boolean that keeps the main event loop running.
        connections (dict): A dictionary that maps the program levels to their respective queues.
        main_input_queue (queue): The queue that all levels use to send logs.
    """

    def __init__(self, options):
        self.options = options
        self.keep_running = True
        self.connections = {}
        self.main_input_queue = Queue()

    def main_loop(self):
        """
        The main loop that waits for logs and displays them.
        """

        self.init_levels()

        # Infinite loop to keep checking the queue for information
        while self.keep_running:

            # Check the main input queue and display logs
            self.check_messages()

            sleep(self.options["MAIN_LOOP_SLEEP_INTERVAL"])

    def init_levels(self):
        """
        Initilizes all the levels of the controller.
        """

        # Make the queues
        com_input_queue = Queue()
        mov_input_queue = Queue()
        ai_input_queue = Queue()

        # Instantiate the levels
        com_level = CommunicationLevel(self.options)
        mov_level = MovementLevel(self.options)
        ai_level = AiLevel(self.options)

        # Instantiate the processes
        com_level_process = Process(target=com_level.com_level_main,
                                    args=(com_input_queue, mov_input_queue, self.main_input_queue))
        mov_level_process = Process(target=mov_level.movement_level_main,
                                    args=(mov_input_queue, com_input_queue, ai_input_queue,
                                          self.main_input_queue))
        ai_level_process = Process(target=ai_level.ai_level_main,
                                   args=(ai_input_queue, mov_input_queue, self.main_input_queue))

        # Start the processes
        com_level_process.start()
        mov_level_process.start()
        ai_level_process.start()

        # Add the processes to the connection map
        self.connections["COM_LEVEL"] = ["running", com_input_queue, com_level_process]
        self.connections["MOV_LEVEL"] = ["running", mov_input_queue, mov_level_process]
        self.connections["AI_LEVEL"] = ["running", ai_input_queue, ai_level_process]

    def check_messages(self):
        """
        Checks the main input queue for new messages.
        """
        while not self.main_input_queue.empty():
            message = self.main_input_queue.get()

            # Ensure that the message is a log message
            if isinstance(message, Message):
                print(message.to_string())
            else:
                # Otherwise print out the raw data
                print('RAW:', message)

    def shutdown(self):
        """
        Shuts down all the lower levels of the controller and then terminates the main level.
        """
        # Loop over the child processes and shut them shutdown
        for key in self.connections:
            self.connections[key][1].put(Message('MAIN_LEVEL', key, 'command', {
                'message': 'Issuing shutdown command to ' + key,
                'directive': 'shutdown',
            }))
            self.connections[key][2].join()
            self.connections[key][0] = "stopped"
            self.check_messages()

        # Check the logs one last time
        self.check_messages()

        # End the com_level
        self.keep_running = False

'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Oct 11, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

from time import sleep
import jsonpickle
from message import Message

class AiLevel:
    """
    The AI level of the AI controller.  This level performs the pathfinding on the world and
    generates the commands for the robot to execute.

    Args:
        options (dict): The dictionary containing the program settings.

    Attributes:
        options (dict): The dictionary containing the program settings.
        keep_running (bool): Boolean that keeps the main event loop running.
        connections (dict): A dictionary that maps the program levels to their respective queues.
    """

    def __init__(self, options):
        self.options = options
        self.keep_running = True
        self.connections = {}
        self.world_model = None

    def ai_level_main(self, ai_input, mov_input, main_input):
        """
        The main event loop of the movement level.  The loop checks for messages to the level,
        interprets the message, and performs the appropriate action.

        Args:
            ai_input (Queue): The queue for receiving messages in the AI level.
            mov_input (Queue): The queue for sending messages to the movement level.
            main_input (Queue): The queue for sending messages to the main level.
        """

        self.connections['AI_LEVEL'] = ['running', ai_input, None]
        self.connections['MOV_LEVEL'] = ['running', mov_input, None]
        self.connections['MAIN_LEVEL'] = ['running', main_input, None]

        main_input.put(Message('AI_LEVEL', 'MAIN_LEVEL', 'info', {
            'message': 'AI_LEVEL is running'
        }))

        # Infinite loop to keep the process running
        while self.keep_running:
            try:
                # Get items from input queue until it is not empty
                while not self.connections["AI_LEVEL"][1].empty():

                    message = self.connections["AI_LEVEL"][1].get()

                    # make sure the message is a Message object
                    if isinstance(message, Message):

                        # Appropriately process the message depending on its category
                        if message.category == 'command':
                            self.process_command(message)

                        # relay message to destination
                        if message.destination != "AI_LEVEL":
                            relay_to = self.connections[message.destination][1]

                            relay_to.put(message)

                        elif self.options['DUMP_MSGS_TO_MAIN']:
                            main_input.put(message)

                # Do rest of stuff

                sleep(self.options["AI_LOOP_SLEEP_INTERVAL"])

            except Exception as err:
                # Catch all exceptions and log them.
                self.connections["MAIN_LEVEL"][1].put(Message('AI_LEVEL', 'MAIN_LEVEL', 'error', {
                    'message': str(err)
                }))

                # Raise the exception again so it isn't lost.
                if self.options["RAISE_ERRORS_AFTER_CATCH"]:
                    raise

    def process_command(self, message):
        """
        The command processor of the AI level.  It processes messages categorized as
        "commands".

        Args:
            message (Message): The message object to be processed.
        """

        if message.data['directive'] == 'generate-moves':
            # Parse out the world model
            world = jsonpickle.decode(message.data['args'])
            print("world parsed")
            print(world)
        
        elif message.data['directive'] == 'shutdown' and message.origin == 'MAIN_LEVEL':
            # the level has been told to shutdown.  Kill all the children!!!
            # Loop over the child processes and shut them shutdown

            self.connections["MAIN_LEVEL"][1].put(Message('AI_LEVEL', 'MAIN_LEVEL', 'info', {
                'message': 'Shutting down AI_LEVEL'
            }))

            # End the com_level
            self.keep_running = False

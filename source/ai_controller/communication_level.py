'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Nov 1, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

from multiprocessing import Process, Queue
from time import sleep
from bot_process import BotProcess
from com_listener import COMListener
from tcp_listener import TCPListener
from serial.tools import list_ports
from message import Message

class CommunicationLevel:
    """
    The communication level of the AI controller.  This level facilitates communication between the
    higher levels and the robots.  It also listens for new connections.

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

    def com_level_main(self, com_input, mov_input, main_input):
        """
        The main event loop of the communication level.  The loop checks for messages to the level,
        interprets the message, and performs the appropriate action.

        Args:
            com_input (Queue): The queue for receiving messages in the communication level.
            mov_input (Queue): The queue for sending messages to the movement level.
            main_input (Queue): The queue for sending messages to the main level.
        """

        self.connections['COM_LEVEL'] = ['running', com_input, None]
        self.connections['MOV_LEVEL'] = ['running', mov_input, None]
        self.connections['MAIN_LEVEL'] = ['running', main_input, None]

        self.connections["MAIN_LEVEL"][1].put(Message('COM_LEVEL', 'MAIN_LEVEL', 'info', {
            'message': 'COM_LEVEL is running'
        }))

        # start the tcp listener
        tcp_listener_input = Queue()
        tcp_listener = TCPListener(self.options)
        tcp_listener_process = Process(target=tcp_listener.tcp_listener_main,
                                       args=(tcp_listener_input, self.connections["COM_LEVEL"][1]))
        tcp_listener_process.start()
        self.connections['TCP_LISTENER'] = ['running', tcp_listener_input, tcp_listener_process]

        # infinite loop to keep checking the queue for information
        while self.keep_running:
            try:
                # get items from queue until it's empty
                while not self.connections["COM_LEVEL"][1].empty():

                    message = self.connections["COM_LEVEL"][1].get()

                    # make sure the message is a Message object
                    if isinstance(message, Message):

                        # Appropriately process the message depending on its category
                        if message.category == 'command':
                            self.process_command(message)

                        elif message.category == 'response':
                            # TODO: Get the revelant data and forward it to MOV_LEVEL

                            # if isinstance(response.data, dict):
                            #     print(response.data)

                            message.destination = "MAIN_LEVEL"

                        # relay message to destination
                        if message.destination != "COM_LEVEL":
                            relay_to = self.connections[message.destination][1]

                            relay_to.put(message)

                        elif self.options['DUMP_MSGS_TO_MAIN']:
                            self.connections["MAIN_LEVEL"][1].put(message)

                    # un-handled message
                    else:
                        # send this un-handled message to main
                        # for raw output to the screen
                        self.connections["MAIN_LEVEL"][1].put(message)

                # check for unconnected robots
                self.scan_com_ports()

                # sleep so that this is not constantly eating processing time
                sleep(self.options["COM_LOOP_SLEEP_INTERVAL"])

            except Exception as err:
                # Catch all exceptions and log them.
                self.connections["MAIN_LEVEL"][1].put(Message('COM_LEVEL', 'MAIN_LEVEL', 'error', {
                    'message': str(err)
                }))

                # Raise the exception again so it isn't lost.
                if self.options["RAISE_ERRORS_AFTER_CATCH"]:
                    raise

    def process_command(self, message):
        """
        The command processor of the movement level.  It processes messages categorized as
        "commands".

        Args:
            message (Message): The message object to be processed.
        """

        if message.data.get('directive') == 'add':
            # if the command is an 'add' directive start a new BotProcess
            bot_input = Queue()
            bot = BotProcess(message.origin, self.options)
            bot_process = Process(target=bot.bot_process_main,
                                  args=(bot_input, self.connections["COM_LEVEL"][1]))

            # push the data to the new bot process
            if message.data.get("args") != None:
                bot_input.put(message.data.get("args"))

            bot_process.start()

            self.connections[message.origin] = ['running', bot_input, bot_process]

            # forward to the mov level
            message.destination = "MOV_LEVEL"

        elif message.data.get('directive') == 'failure':
            # if there was an error then close the connection

            self.connections[message.origin][2].join()
            del self.connections[message.origin]

            # forward to the mov level
            message.destination = "MOV_LEVEL"

        elif message.data.get('directive') == 'shutdown' and message.origin == 'MAIN_LEVEL':
            # the level has been told to shutdown.  Kill all the children!!!
            # Loop over the child processes and shut them shutdown

            self.connections["MAIN_LEVEL"][1].put(Message('COM_LEVEL', 'MAIN_LEVEL', 'info', {
                'message': 'Shutting down COM_LEVEL and child processes'
            }))

            for key in self.connections:
                # Ensure that the connection is a child and not just a queue
                if self.connections[key][2] != None:
                    self.connections[key][1].put(Message('COM_LEVEL', key, 'command', {
                        'message': 'Shutdown ' + key,
                        'directive': 'shutdown',
                    }))
                    self.connections[key][2].join()
                    self.connections[key][0] = "stopped"

            # End the com_level
            self.keep_running = False

    def scan_com_ports(self):
        """
        Scans the open COM ports and opens a listener on them to see if it can establish a
        connection.

        Args:
            message (Message): The message object to be processed.
        """

        # create list of open ports
        ports = list(list_ports.comports())

        # for each port in the list: check if port already exists
        # if exists then skip
        for port in ports:

            address = port[0]

            if address not in self.connections:

                self.connections["MAIN_LEVEL"][1].put(Message('COM_LEVEL', 'MAIN_LEVEL', 'info', {
                    'message': 'Attempting to connect to com port: ' + address
                }))

                #start new process if the serial port is not already open
                com_listener_input = Queue()
                com_listener = COMListener(self.options)
                com_listener_process = Process(target=com_listener.com_listener_main,
                                               args=(address, com_listener_input,
                                                     self.connections["COM_LEVEL"][1]))
                com_listener_process.start()
                self.connections[address] = ['checking', com_listener_input, com_listener_process]

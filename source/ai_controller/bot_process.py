'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Nov 1, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

from time import sleep
import socket
import json
from serial import Serial
from message import Message

class BotProcess:
    """
    Facilitates communication with a robot.  Both TCP and COM processes use this class.

    Args:
        address (str): The COM/TCP address that the robot is using.
        options (dict): The dictionary containing the program settings.

    Attributes:
        bot_input (Queue): The queue for receiving messages in the bot process.
        com_input (Queue): The queue for sending messages to the communication level.
        keep_running (bool): Boolean that keeps the main event loop running.
    """

    def __init__(self, address, options):
        self.address = address
        self.options = options
        self.bot_input = None
        self.com_input = None
        self.keep_running = True

        # Set the TCP socket timeout
        socket.setdefaulttimeout(self.options["TCP_PORT_TIMEOUT"])

    def bot_process_main(self, bot_input, com_input):
        """
        The main function of a bot process.  It checks the connection type (TCP/COM) and hands off
        processing to the appropriate handler.

        Args:
            com_input (Queue): The queue for sending messages to the communication level.
            bot_input (Queue): The queue for receiving messages in the bot process.
        """

        self.bot_input = bot_input
        self.com_input = com_input

        self.com_input.put(Message(self.address, 'MAIN_LEVEL', 'info', {
            'message': 'BOT_PROCESS is running on ' + self.address
        }))

        # Determine if the bot is TCP or COM
        try:
            if self.address[0:3] == "COM":
                self.com_input.put(Message(self.address, 'MAIN_LEVEL', 'info', {
                    'message': 'Bot is on a com port'
                }))
                self.com_process()
            elif self.address[0:3] == "TCP":
                self.com_input.put(Message(self.address, 'MAIN_LEVEL', 'info', {
                    'message': 'Bot is on a tcp port'
                }))
                self.tcp_process()
            else:
                self.com_input.put(Message(self.address, 'COM_LEVEL', 'command', {
                    'directive': 'failure',
                    'message': 'Bot is on an unsupported port type'
                }))

        except Exception as err:
            # Catch all exceptions and log them.
            self.com_input.put(Message(self.address, 'COM_LEVEL', 'command', {
                'directive': 'failure',
                'message': 'Failed with the following error: ' + str(err)
            }))

            # Raise the exception again so it isn't lost.
            if self.options["RAISE_ERRORS_AFTER_CATCH"]:
                raise

        return 0

    def com_process(self):
        """
        The main event loop of a COM port robot.
        """
        with Serial(self.address, self.options["BAUD"],
                    timeout=self.options["COM_PORT_TIMEOUT"]) as connection:

            self.com_input.put(Message(self.address, 'MAIN_LEVEL', 'info', {
                'message': 'Connected to robot'
            }))

            # establish connection and clear the buffer from the robot
            response = connection.readline()
            while connection.inWaiting() > 0:
                response = connection.read(connection.inWaiting())

            while self.keep_running:
                self.wait_for_commands(self.options["BOT_LOOP_SLEEP_INTERVAL"],
                                       self.options["BOT_SLEEP_INTERVALS_PER_PING"])

                # there is data in the queue
                while not self.bot_input.empty():
                    message = self.bot_input.get()

                    # make sure the message is a list object
                    if isinstance(message, Message):

                        # check if the message is a movement command
                        if message.category == 'movement':

                            command = message.data.get("command")
                            magnitude = message.data.get("magnitude")

                            mov_str = str(command) + " " + str(magnitude)

                            self.com_input.put(Message(self.address, 'MAIN_LEVEL', 'info', {
                                'message': 'Given command: ' + mov_str
                            }))

                            connection.write(bytes(mov_str, "utf-8"))

                            response = connection.readline().strip().decode()

                            while connection.inWaiting() > 0:
                                response = response + connection.read(
                                    connection.inWaiting()).strip().decode()

                            if response == '':
                                self.com_input.put(Message(self.address, 'COM_LEVEL', 'command', {
                                    'directive': 'failure',
                                    'message': 'Failed to get a response from robot'
                                }))

                                return 0

                            else:
                                parsed_res = json.loads(response)

                                self.com_input.put(
                                    Message(self.address, 'COM_LEVEL', 'response', parsed_res)
                                )

                        elif (message.data.get('directive') == 'shutdown'
                              and message.origin == 'COM_LEVEL'):

                            connection.close()

                            # the listener has been told to shutdown.
                            self.com_input.put(Message(self.address, 'MAIN_LEVEL', 'info', {
                                'message': 'Shutting down ' + self.address
                            }))

                            self.keep_running = False

    def tcp_process(self):
        """
        The main event loop of a COM port robot.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            self.com_input.put(Message(self.address, 'MAIN_LEVEL', 'info', {
                'message': 'Connected to robot'
            }))

            # Get the connection data
            connection_data = self.bot_input.get()

            # Sleep for a few seconds to let the TCP client get setup
            sleep(2)
            connection.connect((connection_data.get('ip'), int(self.address[4:])))

            while self.keep_running:
                self.wait_for_commands(self.options["BOT_LOOP_SLEEP_INTERVAL"],
                                       self.options["BOT_SLEEP_INTERVALS_PER_PING"])

                # there is data in the queue
                while not self.bot_input.empty():
                    message = self.bot_input.get()

                    # check if the message is a movement command
                    if message.category == 'movement':

                        command = message.data.get("command")
                        magnitude = message.data.get("magnitude")

                        mov_str = str(command) + " " + str(magnitude)

                        self.com_input.put(Message(self.address, 'MAIN_LEVEL', 'info', {
                            'message': 'Given command: ' + mov_str
                        }))

                        # send data on the socket
                        connection.send(bytes(mov_str, "utf-8"))

                        response = connection.recv(1024).strip().decode()

                        self.com_input.put(Message(self.address, 'COM_LEVEL', 'response', {
                            'message': 'Received the following response: '
                                       + response.replace('\r\n', ' ')}))

                    elif (message.data.get('directive') == 'shutdown'
                          and message.origin == 'COM_LEVEL'):

                        connection.close()

                        # the listener has been told to shutdown.
                        self.com_input.put(Message(self.address, 'MAIN_LEVEL', 'info', {
                            'message': 'Shutting down ' + self.address
                        }))

                        self.keep_running = False

    def wait_for_commands(self, timeout, intervals_per_ping):
        """
        Loops forever until a command is put in the bot_input.  Pings the robot periodically to
        ensure the connection is still active.

        Args:
            timeout (float): The time in seconds that the loop should wait before checking for data.
            intervals_per_ping (int): Number of intervals that should run before a ping is sent.
        """

        interval = 0

        # wait until a command has been issued
        while self.bot_input.empty():
            sleep(timeout)
            interval = interval + 1
            if interval >= intervals_per_ping:
                self.bot_input.put(Message(self.address, self.address, 'movement', {
                    'command': 99, # Ping command
                    'magnitude': 0,
                    'message': 'Pinging Robot'
                }))

'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Nov 1, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

import socketserver
import json
from message import Message

class TCPListener:
    """
    Listens for new bots trying to communicate over TCP.  It acts as a TCP server so that TCP bots
    can register their ports and ip addresses with the system.  Registered bots are given a port
    where they can expect to hear from the server.  After registering with the TCP listener, bots
    must create a TCP server and wait for commands from the controller.

    NOTE:
    The data sent to the listener should be an encided dictionary like the following
    b'{\"type\": \"SMORES\",\"id\": \"robot-1\", \"ip\": \"192.168.1.1\"}'

    Args:
        options (dict): The dictionary containing the program settings.

    Attributes:
        options (dict): The dictionary containing the program settings.
        static_com_input (Queue): Static value. Queue for pushing commands from the TCPHandler
        static_next_port (int): Static value. The next available port for a TCP robot to use.
        listener_input (Queue): The queue for receiving messages in the listener level.
        com_input (Queue): The queue for sending messages to the communication level.
        keep_running (bool): Boolean that keeps the main event loop running.
    """

    # Need a static queue since there is no other way to send messages from the TCPHandler
    static_com_input = None

    # Need static port numbers so that the TCPHandler can access this value
    static_next_port = 10000

    def __init__(self, options):
        self.options = options
        self.listener_input = None
        self.com_input = None
        self.keep_running = True
        TCPListener.static_next_port = self.options["TCP_LISTENER_START_PORT"]

    def tcp_listener_main(self, listener_input, com_input):
        """
        The main event loop of the tcp listener.  The loop checks for messages to the level,
        interprets the message, and performs the appropriate action.

        Args:
            main_input (Queue): The queue for receiving messages in the TCP listener.
            com_input (Queue): The queue for sending messages to the communication level.
        """

        # Set queues
        self.com_input = com_input
        self.listener_input = listener_input
        TCPListener.static_com_input = com_input

        self.com_input.put(Message('TCP_LISTENER', 'MAIN_LEVEL', 'info', {
            'message': 'TCP_LISTENER is running'
        }))

        # Create the server, binding the localhost to the assigned port.
        server = socketserver.TCPServer(
            (self.options["TCP_LISTENER_IP"], self.options["TCP_LISTENER_PORT"]),
            TCPListener.TCPHandler
        )
        server.socket.settimeout(1)

        # Enter the main event loop
        while self.keep_running:
            while not self.listener_input.empty():

                message = self.listener_input.get()

                # Appropriately process the message depending on its category
                if isinstance(message, Message) and message.category == 'command':
                    self.process_command(message)

                else:
                    # Echo back the message if it doesn't know what to do
                    self.com_input.put(message)

            server.handle_request()

    def process_command(self, message):
        """
        The command processor of the TCP listener.  It processes messages categorized as
        "commands".

        Args:
            message (Message): The message object to be processed.
        """

        if message.data.get('directive') == 'shutdown' and message.origin == 'COM_LEVEL':

            # the listener has been told to shutdown.
            self.com_input.put(Message('TCP_LISTENER', 'MAIN_LEVEL', 'info', {
                'message': 'Shutting down TCP_LISTENER'
            }))

            self.keep_running = False

    class TCPHandler(socketserver.BaseRequestHandler):
        """
        Handles a TCP request.
        """

        def handle(self):
            # self.request is the TCP socket connected to the client
            # data should be a byte string containing an encoded dictionary
            self.data = self.request.recv(1024).strip().decode("utf-8")

            # attempt to load the dictionary
            try:
                self.data = json.loads(self.data)

                # check if it is a supported model
                if self.data.get("type") == "SMORES":
                    # assign the robot a port and inform the com level
                    self.request.send(bytes(self.data.get('ip') + ' ' +
                                            str(TCPListener.static_next_port),
                                            "utf-8"))

                    TCPListener.static_com_input.put(Message(
                        "TCP:" + str(TCPListener.static_next_port),
                        'COM_LEVEL', 'command',
                        {
                            'directive': 'add',
                            'args': self.data,
                            'message': 'Received TCP information'
                        }
                    ))

                    TCPListener.static_next_port = TCPListener.static_next_port + 1

                else:
                    self.request.send(bytes("Unsupported robot type", "utf-8"))

            except Exception as err:
                # Catch all exceptions and log them.
                TCPListener.static_com_input.put(Message('TCP_LISTENER', 'MAIN_LEVEL', 'error', {
                    'message': str(err)
                }))

                # exception occurred, attempt to inform the client of the error.
                self.request.send(bytes("Unsupported data type", "utf-8"))

                # Raise the exception again so it isn't lost.
                raise

            finally:
                # close the socket
                self.request.close()

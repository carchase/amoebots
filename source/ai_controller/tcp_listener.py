'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Nov 1, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

import socketserver
import socket
import json
from message import Message

'''
The data sent to the listener should be an encided dictionary like the following
b'{\"type\": \"SMORES\",\"id\": \"robot-1\", \"ip\": \"192.168.1.1\"}'
'''

class TCPListener:
    static_com_input = None

    def __init__(self, options):
        self.server_host = socket.gethostbyname(socket.gethostname())
        self.server_port = 5000
        self.com_input = None
        self.listener_input = None
        self.keep_running = True
        self.options = options

    def tcp_listener_main(self, com_input, listener_input):
        self.com_input = com_input
        self.listener_input = listener_input
        TCPListener.static_com_input = com_input

        self.com_input.put(Message('TCP_LISTENER', 'MAIN_LEVEL', 'info', {
            'message': 'TCP_LISTENER is running'
        }))

        # create the server, binding the localhost to the assigned port.
        server = socketserver.TCPServer((self.server_host, self.server_port),
                                        TCPListener.TCPHandler)
        server.socket.settimeout(1)

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

        return

    def process_command(self, message):

        if message.data.get('directive') == 'shutdown' and message.origin == 'COM_LEVEL':

            # the listener has been told to shutdown.
            self.com_input.put(Message('TCP_LISTENER', 'MAIN_LEVEL', 'info', {
                'message': 'Shutting down TCP_LISTENER'
            }))

            self.keep_running = False

    class TCPHandler(socketserver.BaseRequestHandler):
        """
        Handles a TCP request.

        Attributes:
            next_port (int): The next available port for a TCP robot to use.
        """
        next_port = 10000

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
                                            str(TCPListener.TCPHandler.next_port),
                                            "utf-8"))

                    TCPListener.static_com_input.put(Message(
                        "TCP:" + str(TCPListener.TCPHandler.next_port),
                        'COM_LEVEL', 'command',
                        {
                            'directive': 'add',
                            'args': self.data,
                            'message': 'Received TCP information'
                        }
                    ))

                    TCPListener.TCPHandler.next_port = TCPListener.TCPHandler.next_port + 1

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

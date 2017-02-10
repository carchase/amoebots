'''
Created on Nov 1, 2016

@author: Trevor
'''
import socketserver
import socket
import json
from time import sleep
from message import Message

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000
COM_INPUT_QUEUE = None
INFINITE_LOOP = True

'''
The data should be an encided dictionary of the following
b'{\"type\": \"SMORES\",\"id\": \"robot-1\", \"ip\": \"192.168.1.1\"}'
'''

class TCPHandler(socketserver.BaseRequestHandler):
    nextPort = 10000

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
                self.request.send(
                    bytes(self.data.get('ip') + ' ' + str(TCPHandler.nextPort), "utf-8")
                )

                global COM_INPUT_QUEUE

                COM_INPUT_QUEUE.put(Message("TCP:" + str(TCPHandler.nextPort),
                                            'COM_LEVEL', 'command',
                                            {
                                                'directive': 'add',
                                                'args': self.data,
                                                'message': 'Received TCP information'
                                            }))

                TCPHandler.nextPort = TCPHandler.nextPort + 1

            else:
                self.request.send(bytes("Unsupported robot type", "utf-8"))

        except Exception as err:
            COM_INPUT_QUEUE.put(Message('TCP_LISTENER', 'MAIN_LEVEL', 'error', {
                'message': str(err)
            }))

            # exception occurred, attempt to recover data
            self.request.send(bytes("Unsupported data type", "utf-8"))

        finally:
            # close the socket
            self.request.close()

def tcp_listener_main(COM_INPUT, PROCESS_QUEUE):
    global COM_INPUT_QUEUE
    COM_INPUT_QUEUE = COM_INPUT
    global INFINITE_LOOP
    INFINITE_LOOP = True
    COM_INPUT.put(Message('TCP_LISTENER', 'MAIN_LEVEL', 'info', {
        'message': 'TCP_listener is running'
    }))

    # create the server, binding the localhost to the assigned port.
    server = socketserver.TCPServer((SERVER_HOST, SERVER_PORT), TCPHandler)
    server.socket.settimeout(1)

    while INFINITE_LOOP:
        while not PROCESS_QUEUE.empty():

            message = PROCESS_QUEUE.get()

            # Appropriately process the message depending on its category
            if isinstance(message, Message) and message.category == 'command':
                process_command(message)

            else:
                # Echo back the message if it doesn't know what to do
                COM_INPUT_QUEUE.put(message)

        server.handle_request()

    return

def process_command(message):
    global INFINITE_LOOP

    if message.data.get('directive') == 'shutdown' and message.origin == 'COM_LEVEL':

        # the listener has been told to shutdown.
        COM_INPUT_QUEUE.put(Message('TCP_LISTENER', 'MAIN_LEVEL', 'info', {
            'message': 'Shutting down TCP listener'
        }))

        INFINITE_LOOP = False

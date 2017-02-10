'''
Created on Nov 1, 2016

@author: Trevor
'''
from time import sleep
import serial
import socket
import json
from message import Message

BAUD = '115200'
replied = False

def bot_listener_main(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    COM_INPUT.put(Message(ADDRESS, 'MAIN_LEVEL', 'info', {
        'message': 'Process_listener started on port ' + ADDRESS
    }))

    try:
        with serial.Serial(ADDRESS, BAUD, timeout=10) as PORT:

            # Call the ping command
            PORT.write(bytes("99 0 0", "utf-8"))

            response = PORT.readline().strip().decode()

            if not response == '':
                # Clean out the buffer
                while PORT.inWaiting() > 0:
                    response = response + PORT.read(PORT.inWaiting()).strip().decode()

                COM_INPUT.put(Message(ADDRESS, 'COM_LEVEL', 'command', {
                    'directive': 'add',
                    'message': 'Added a robot on port ' + ADDRESS
                }))
            else:
                COM_INPUT.put(Message(ADDRESS, 'COM_LEVEL', 'command', {
                    'directive': 'failure',
                    'message': 'Could not add robot on port ' + ADDRESS
                }))

            PORT.close()

    except Exception as e:
        COM_INPUT.put(Message(ADDRESS, 'COM_LEVEL', 'command', {
            'directive': 'failure',
            'message': 'Failed with the following error: ' + str(e)
        }))

    return 0

def bot_process_main(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    COM_INPUT.put(Message(ADDRESS, 'MAIN_LEVEL', 'info', {'message': 'Bot_process is running'}))

    # Determine if the bot is TCP or COM
    try:
        if ADDRESS[0:3] == "COM":
            COM_INPUT.put(Message(ADDRESS, 'MAIN_LEVEL', 'info', {
                'message': 'Bot is on a com port'
            }))
            com_process(ADDRESS, COM_INPUT, PROCESS_QUEUE)
        elif ADDRESS[0:3] == "TCP":
            COM_INPUT.put(Message(ADDRESS, 'MAIN_LEVEL', 'info', {
                'message': 'Bot is on a tcp port'
            }))
            tcp_process(ADDRESS, COM_INPUT, PROCESS_QUEUE)
        else:
            COM_INPUT.put(Message(ADDRESS, 'COM_LEVEL', 'command', {
                'directive': 'failure',
                'message': 'Bot is on an unsupported port type'
            }))

    except Exception as e:
        COM_INPUT.put(Message(ADDRESS, 'COM_LEVEL', 'command', {
            'directive': 'failure',
            'message': 'Failed with the following error: ' + str(e)
        }))

    return 0

def com_process(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    with serial.Serial(ADDRESS, BAUD, timeout=10) as PORT:
        COM_INPUT.put(Message(ADDRESS, 'MAIN_LEVEL', 'info', {'message': 'Connected to robot'}))

        # establish connection
        response = PORT.readline().strip().decode()
        while PORT.inWaiting() > 0:
            response = response + PORT.read(PORT.inWaiting()).strip().decode()

        INFINITE_LOOP = True

        while INFINITE_LOOP:
            waitForCommands(.1, PROCESS_QUEUE)

            # there is data in the queue
            while not PROCESS_QUEUE.empty():
                message = PROCESS_QUEUE.get()

                # make sure the message is a list object
                if isinstance(message, Message):

                    # check if the message is a movement command
                    if message.category == 'movement':

                        command = message.data.get("command")
                        velocity = message.data.get("velocity")
                        duration = message.data.get("duration")

                        movementStr = str(command) + " " + str(velocity) + " " + str(duration*1000)

                        COM_INPUT.put(Message(ADDRESS, 'MAIN_LEVEL', 'info', {
                            'message': 'Given command: ' + movementStr
                        }))

                        PORT.write(bytes(movementStr, "utf-8"))

                        sleep(duration + 4)

                        response = ''
                        while PORT.inWaiting() > 0:
                            response = response + PORT.read(PORT.inWaiting()).strip().decode()

                        if response == '':
                            COM_INPUT.put(Message(ADDRESS, 'COM_LEVEL', 'command', {
                                'directive': 'failure',
                                'message': 'Failed to get a response from robot'
                            }))

                            return 0

                        else:

                            parsed_res = json.loads(response)

                            COM_INPUT.put(Message(ADDRESS, 'COM_LEVEL', 'response', parsed_res))

                    elif (message.data.get('directive') == 'shutdown'
                          and message.origin == 'COM_LEVEL'):

                        PORT.close()

                        # the listener has been told to shutdown.
                        COM_INPUT.put(Message(ADDRESS, 'MAIN_LEVEL', 'info', {
                            'message': 'Shutting down ' + ADDRESS
                        }))

                        INFINITE_LOOP = False

def tcp_process(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET:
        COM_INPUT.put(Message(ADDRESS, 'MAIN_LEVEL', 'info', {'message': 'Connected to robot'}))

        # get the connection data
        connectionData = PROCESS_QUEUE.get()

        # sleep for a few seconds to let the simulator get setup
        sleep(2)
        SOCKET.connect((connectionData.get('ip'), int(ADDRESS[4:])))

        INFINITE_LOOP = True

        while INFINITE_LOOP:
            waitForCommands(.1, PROCESS_QUEUE)

            # there is data in the queue
            while not PROCESS_QUEUE.empty():
                message = PROCESS_QUEUE.get()

                # check if the message is a movement command
                if message.category == 'movement':

                    command = message.data.get("command")
                    velocity = message.data.get("velocity")
                    duration = message.data.get("duration")

                    movementStr = str(command) + " " + str(velocity) + " " + str(duration * 1000)

                    COM_INPUT.put(Message(ADDRESS, 'MAIN_LEVEL', 'info', {
                        'message': 'Shutting down ' + ADDRESS
                    }))

                    # send data on the socket

                    # establish the connection
                    SOCKET.send(bytes(movementStr, "utf-8"))

                    response = SOCKET.recv(1024).strip().decode()

                    COM_INPUT.put(Message(ADDRESS, 'COM_LEVEL', 'response', {
                        'message': 'Received the following response: '
                                   + response.replace('\r\n', ' ')}))

                elif message.data.get('directive') == 'shutdown' and message.origin == 'COM_LEVEL':

                    SOCKET.close()

                    # the listener has been told to shutdown.
                    COM_INPUT.put(Message(ADDRESS, 'MAIN_LEVEL', 'info', {
                        'message': 'Shutting down ' + ADDRESS
                    }))

                    INFINITE_LOOP = False

def waitForCommands(timeout, input):
    # wait until a command has been issued
    while input.empty():
        sleep(timeout)

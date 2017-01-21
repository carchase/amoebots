'''
Created on Nov 1, 2016

@author: Trevor
'''
from time import sleep
import serial
import socket
from message import Message

BAUD = '115200'
replied = False

def bot_listener_main(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    COM_INPUT.put( Message(ADDRESS, 'MAIN_LOG', 'info', {'message': 'Process_listener started on port ' + ADDRESS}))

    try:
        with serial.Serial(ADDRESS, BAUD, timeout = 10) as PORT:

            # Call the ping command
            PORT.write(bytes("99 0 0", "utf-8"))

            response = PORT.readline().strip().decode()

            if not response == '':
                # Clean out the buffer
                while PORT.inWaiting() > 0:
                    response = response + PORT.read(PORT.inWaiting()).strip().decode()

                COM_INPUT.put( Message(ADDRESS, 'COM_LEVEL', 'command', {'directive': 'add', 'message': 'Added a robot on port ' + ADDRESS}))
                
            else:
                COM_INPUT.put( Message(ADDRESS, 'COM_LEVEL', 'command', {'directive': 'failure', 'message': 'Could not add robot on port ' + ADDRESS}))
                
            PORT.close()
            
    except Exception as e:
        COM_INPUT.put( Message(ADDRESS, 'COM_LEVEL', 'command', {'directive': 'failure', 'message': 'Failed with the following error: ' + str(e)}))

    return 0

def bot_process_main(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    COM_INPUT.put( Message(ADDRESS, 'MAIN_LOG', 'info', {'message': 'Bot_process is running'}))

    # Determine if the bot is TCP or COM
    try:
        if ADDRESS[0:3] == "COM":
            COM_INPUT.put( Message(ADDRESS, 'MAIN_LOG', 'info', {'message': 'Bot is on a com port'}))
            com_process(ADDRESS, COM_INPUT, PROCESS_QUEUE)
        elif ADDRESS[0:3] == "TCP":
            COM_INPUT.put( Message(ADDRESS, 'MAIN_LOG', 'info', {'message': 'Bot is on a tcp port'}))
            tcp_process(ADDRESS, COM_INPUT, PROCESS_QUEUE)
        else:
            COM_INPUT.put( Message(ADDRESS, 'COM_LEVEL', 'command', {'directive': 'failure', 'message': 'Bot is on an unsupported port type'}))

    except Exception as e:
        COM_INPUT.put( Message(ADDRESS, 'COM_LEVEL', 'command', {'directive': 'failure', 'message': 'Failed with the following error: ' + str(e)}))

    return 0

def com_process(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    with serial.Serial(ADDRESS, BAUD, timeout = 10) as PORT:
        COM_INPUT.put( Message(ADDRESS, 'MAIN_LOG', 'info', {'message': 'Connected to robot'}))

        # establish connection            
        response = PORT.readline().strip().decode()
        while PORT.inWaiting() > 0:
            response = response + PORT.read(PORT.inWaiting()).strip().decode()
    
        while True:
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

                        movementStr = str(command) + " " + str(velocity) + " " + str(duration * 1000)

                        COM_INPUT.put( Message(ADDRESS, 'MAIN_LOG', 'info', {'message': 'Given command: ' + movementStr}))
                
                        PORT.write(bytes(movementStr, "utf-8"))

                        sleep(duration + 2)
                        
                        response = ''
                        while PORT.inWaiting() > 0:
                            response = response + PORT.read(PORT.inWaiting()).strip().decode()
                            
                        if response == '':
                            COM_INPUT.put( Message(ADDRESS, 'COM_LEVEL', 'command', {'directive': 'failure', 'message': 'Failed to get a response back from robot, aborting connection'}))
                            
                            return 0
                        
                        else:
                            COM_INPUT.put( Message(ADDRESS, 'COM_LEVEL', 'response', {'message': 'Received the following response: ' + response.replace('\r\n', ' ')}))

def tcp_process(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    # get the connection data
    data = PROCESS_QUEUE.get()
    
    while True:
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

                COM_INPUT.put( Message(ADDRESS, 'MAIN_LOG', 'info', {'message': 'Given command: ' + movementStr}))

                # open a socket
                SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                SOCKET.connect((data.get('ip'), int(ADDRESS[4:])))
                SOCKET.send(bytes(movementStr, "utf-8"))

                sleep(duration + 2)
                
                response = SOCKET.recv(1024).strip().decode()
                SOCKET.close()

                COM_INPUT.put( Message(ADDRESS, 'COM_LEVEL', 'response', {'message': 'Received the following response: ' + response.replace('\r\n', ' ')}))

def waitForCommands(timeout, input):
    # wait until a command has been issued
    while input.empty():
        sleep(timeout)
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
    COM_INPUT.put( Message(ADDRESS, 'MAIN_INPUT', 'INFO', {'message': 'Process_listener started on port ' + ADDRESS}))

    try:
        with serial.Serial(ADDRESS, BAUD, timeout = 10) as PORT:

            RESPONSE = PORT.readline().strip().decode()

            if not RESPONSE == '':
                # Clean out the buffer
                while PORT.inWaiting() > 0:
                    RESPONSE = RESPONSE + PORT.read(PORT.inWaiting()).strip().decode()

                COM_INPUT.put( Message(ADDRESS, 'COM_INPUT', 'COMMAND', {'directive': 'add', 'message': 'Added a robot on port ' + ADDRESS}))
                
            else:
                COM_INPUT.put( Message(ADDRESS, 'COM_INPUT', 'COMMAND', {'directive': 'failure', 'message': 'Could not add robot on port ' + ADDRESS}))
                
            PORT.close()
            
    except Exception as e:
        COM_INPUT.put( Message(ADDRESS, 'COM_INPUT', 'COMMAND', {'directive': 'failure', 'message': 'Received the following error: ' + e}))

    return 0

def bot_process_main(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    COM_INPUT.put( Message(ADDRESS, 'MAIN_INPUT', 'INFO', {'message': 'bot_process is running'}))

    # Determine if the bot is TCP or COM
    try:
        if ADDRESS[0:3] == "COM":
            COM_INPUT.put( Message(ADDRESS, 'MAIN_INPUT', 'INFO', {'message': 'bot is on a com port'}))
            com_process(ADDRESS, COM_INPUT, PROCESS_QUEUE)
        elif ADDRESS[0:3] == "TCP":
            COM_INPUT.put( Message(ADDRESS, 'MAIN_INPUT', 'INFO', {'message': 'bot is on a tcp port'}))
            tcp_process(ADDRESS, COM_INPUT, PROCESS_QUEUE)
        else:
            COM_INPUT.put( Message(ADDRESS, 'COM_INPUT', 'COMMAND', {'directive': 'failure', 'message': 'Bot is on an unsupported port type'}))

    except Exception as e:
        COM_INPUT.put( Message(ADDRESS, 'COM_INPUT', 'COMMAND', {'directive': 'failure', 'message': 'Received the following error: ' + e}))

    return 0

def com_process(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    with serial.Serial(ADDRESS, BAUD, timeout = 10) as PORT:
        COM_INPUT.put( Message(ADDRESS, 'MAIN_INPUT', 'INFO', {'message': 'Connected to robot'}))

        # establish connection            
        RESPONSE = PORT.readline().strip().decode()
        while PORT.inWaiting() > 0:
            RESPONSE = RESPONSE + PORT.read(PORT.inWaiting()).strip().decode()
    
        while True:
            waitForCommands(.1, PROCESS_QUEUE)

            # there is data in the queue
            while not PROCESS_QUEUE.empty():
                message = PROCESS_QUEUE.get()

                # make sure the message is a list object
                if isinstance(message, dict):

                    # check if the message is a command
                    if message.get('type') == 'command':
                        
                        COM_INPUT.put( Message(ADDRESS, 'MAIN_INPUT', 'INFO', {'message': 'Given command: ' + message.data.get('directive')}))
                
                        PORT.write(bytes(message.get('message'), "utf-8"))
                        
                        sleep(message.get('duration') + 1)
                        
                        RESPONSE = ""
                        while PORT.inWaiting() > 0:
                            RESPONSE = RESPONSE + PORT.read(PORT.inWaiting()).strip().decode()
                            
                        if RESPONSE == '':
                            COM_INPUT.put({
                                'destination': 'MAIN_INPUT',
                                'origin': ADDRESS,
                                'type': 'command',
                                'message': 'failure'})
                            
                            return 0
                        
                        else:
                            COM_INPUT.put({
                                'destination': 'MAIN_INPUT',
                                'origin': ADDRESS,
                                'type': 'result',
                                'message': RESPONSE.replace('\r\n', ' ')})

def tcp_process(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    # get the connection data
    data = PROCESS_QUEUE.get()
    
    while True:
        waitForCommands(.1, PROCESS_QUEUE)

        # there is data in the queue
        while not PROCESS_QUEUE.empty():
            message = PROCESS_QUEUE.get()

            # check if the message is a command
            if message.get('type') == 'command':
                
                COM_INPUT.put({
                    'destination': 'MAIN_INPUT',
                    'origin': ADDRESS,
                    'type': 'info',
                    'message': 'given command ' + message.get('message')})

                # open a socket
                SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                SOCKET.connect((data.get('ip'), int(ADDRESS[4:])))
                SOCKET.send(bytes(message.get('message'), "utf-8"))
                RESPONSE = SOCKET.recv(1024).strip().decode()
                SOCKET.close()
                sleep(3)

                COM_INPUT.put({
                    'destination': 'COM_INPUT',
                    'origin': ADDRESS,
                    'type': 'result',
                    'message': RESPONSE})

def waitForCommands(timeout, input):
    # wait until a command has been issued
    while input.empty():
        sleep(timeout)
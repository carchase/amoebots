'''
Created on Nov 1, 2016

@author: Trevor
'''
from time import sleep
import serial
import socket

BAUD = '115200'
replied = False

def bot_listener_main(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    COM_INPUT.put({
       'destination': 'MAIN_INPUT',
       'origin': ADDRESS,
       'type': 'info',
       'message': 'Process_listener started'})

    try:
        with serial.Serial(ADDRESS, BAUD, timeout = 10) as PORT:
        
            #COM_INPUT.put({
            #    'destination': 'MAIN_INPUT',
            #    'origin': ADDRESS,
            #    'type': 'result',
            #    'message': 'Connection successful'})

            RESPONSE = PORT.readline().strip().decode()

            if not RESPONSE == '':
                # Clean out the buffer
                while PORT.inWaiting() > 0:
                    RESPONSE = RESPONSE + PORT.read(PORT.inWaiting()).strip().decode()

                COM_INPUT.put({
                    'destination': 'COM_INPUT',
                    'origin': ADDRESS,
                    'type': 'command',
                    'message': 'add'})
                
            else:
                COM_INPUT.put({
                    'destination': 'COM_INPUT',
                    'origin': ADDRESS,
                    'type': 'command',
                    'message': 'failure'})
                
            PORT.close()
            
    except:
        COM_INPUT.put({
            'destination': 'COM_INPUT',
            'origin': ADDRESS,
            'type': 'command',
            'message': 'failure'})
        
    return 0

def bot_process_main(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    COM_INPUT.put(({
        'destination': 'MAIN_INPUT',
        'origin': ADDRESS,
        'type': 'info',
        'message': 'bot_process is running'}))

    # Determine if the bot is TCP or COM
    try:
        if ADDRESS[0:3] == "COM":
            COM_INPUT.put(({
                'destination': 'MAIN_INPUT',
                'origin': ADDRESS,
                'type': 'info',
                'message': 'bot is on a com port'}))
            com_process(ADDRESS, COM_INPUT, PROCESS_QUEUE)
        elif ADDRESS[0:3] == "TCP":
            COM_INPUT.put(({
                'destination': 'MAIN_INPUT',
                'origin': ADDRESS,
                'type': 'info',
                'message': 'bot is on a tcp port'}))
            tcp_process(ADDRESS, COM_INPUT, PROCESS_QUEUE)
        else:
            COM_INPUT.put({'destination': 'COM_INPUT',
                'origin': ADDRESS,
                'type': 'command',
                'message': 'failure'})

    except:
        COM_INPUT.put({'destination': 'COM_INPUT',
                        'origin': ADDRESS,
                        'type': 'command',
                        'message': 'failure'})
    return 0

def com_process(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    with serial.Serial(ADDRESS, BAUD, timeout = 10) as PORT:
        
        COM_INPUT.put({
            'destination': 'MAIN_INPUT',
            'origin': ADDRESS,
            'type': 'info',
            'message': 'connected to robot'})

        # establish connection            
        RESPONSE = PORT.readline().strip().decode()
        while PORT.inWaiting() > 0:
            RESPONSE = RESPONSE + PORT.read(PORT.inWaiting()).strip().decode()
    
        while True:
            waitForCommands(.5, PROCESS_QUEUE)

            # there is data in the queue
            while not PROCESS_QUEUE.empty():
                message = PROCESS_QUEUE.get()

                # make sure the message is a list object
                if isinstance(message, dict):

                    # check if the message is a command
                    if message.get('type') == 'command':
                        
                        COM_INPUT.put({
                            'destination': 'MAIN_INPUT',
                            'origin': ADDRESS,
                            'type': 'info',
                            'message': 'given command ' + message.get('message')})
                
                        PORT.write(bytes(message.get('message'), "utf-8"))
                        
                        sleep(5)
                        
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET:
                
        # get the connection data
        data = PROCESS_QUEUE.get()
    
        SOCKET.connect((data.get('ip'), int(ADDRESS[4:])))
        
        while True:
            waitForCommands(.5, PROCESS_QUEUE)

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
                    
                    SOCKET.send(bytes(message.get('message'), "utf-8"))
                    
                    RESPONSE = SOCKET.recv(1024).strip().decode()

                    COM_INPUT.put({
                        'destination': 'COM_INPUT',
                        'origin': ADDRESS,
                        'type': 'result',
                        'message': RESPONSE})

def waitForCommands(timeout, input):
    # wait until a command has been issued
    while input.empty():
        sleep(timeout)
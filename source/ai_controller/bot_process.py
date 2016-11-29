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
            
            PORT.write(bytes("5 150", "utf-8"))

            RESPONSE = PORT.readline().strip().decode()

            if not RESPONSE == '':
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
    
        while True:
            
            PORT.write(bytes("1 150", "utf-8"))
            
            sleep(5)
                        
            RESPONSE = PORT.readline().strip().decode()
            
            if RESPONSE == '':   
                    
                COM_INPUT.put({
                    'destination': 'MAIN_INPUT',
                    'origin': ADDRESS,
                    'type': 'command',
                    'message': 'failure'})
                
                return 0;
            
            else:
        
                COM_INPUT.put({
                    'destination': 'MAIN_INPUT',
                    'origin': ADDRESS,
                    'type': 'result',
                    'message': RESPONSE})

def tcp_process(ADDRESS, COM_INPUT, PROCESS_QUEUE):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET:
        
        SOCKET.connect(("localhost", ADDRESS[4:]))

        COM_INPUT.put({
            'destination': 'MAIN_INPUT',
            'origin': ADDRESS,
            'type': 'info',
            'message': 'connected to socket'})
    
        while True:
            
            SOCKET.send(bytes("1 150", "utf-8"))
            
            sleep(5)
                        
            RESPONSE = SOCKET.recv(1024).strip().decode()
            
            if RESPONSE == '':   
                    
                COM_INPUT.put({
                    'destination': 'COM_INPUT',
                    'origin': ADDRESS,
                    'type': 'command',
                    'message': 'failure'})
                
                return 0;
            
            else:
        
                COM_INPUT.put({
                    'destination': 'COM_INPUT',
                    'origin': ADDRESS,
                    'type': 'result',
                    'message': DECODED_RESPONSE})
'''
Created on Nov 1, 2016

@author: Trevor
'''
from time import sleep
import timeout_decorator
import serial

BAUD = '9600'
replied = False

@timeout_decorator.timeout(10)
def listener_helper(PORT):
    return PORT.readline()

def process_listener(ADDRESS, LISTEN_INPUT, PROCESS_Q):
    #LISTEN_INPUT.put({
    #    'destination': 'TO_MAIN',
    #    'origin': ADDRESS,
    #    'type': 'success',
    #    'message': 'Process_listener started'})

    try:
        with serial.Serial(ADDRESS, BAUD, timeout = 10) as PORT:
        
            #LISTEN_INPUT.put({
            #    'destination': 'TO_MAIN',
            #    'origin': ADDRESS,
            #    'type': 'success',
            #    'message': 'Connection successful'})
            
            PORT.write(str.encode(ADDRESS + " hello"))

            RESPONSE = PORT.readline()

            DECODED_RESPONSE = bytes.decode(RESPONSE)

            if not DECODED_RESPONSE == None:
                LISTEN_INPUT.put({
                    'destination': 'TO_MAIN',
                    'origin': ADDRESS,
                    'type': 'add',
                    'message': DECODED_RESPONSE})
            else:
                LISTEN_INPUT.put({
                    'destination': 'TO_MAIN',
                    'origin': ADDRESS,
                    'type': 'failure',
                    'message': 'the message timed out'})
            
    except:
        LISTEN_INPUT.put({
            'destination': 'TO_MAIN',
            'origin': ADDRESS,
            'type': 'failure',
            'message': 'exited process_listener'})
        
    return 0

def process_main(ADDRESS, COM_INPUT, PROCESS_Q):
    COM_INPUT.put(({
        'destination': 'TO_MAIN',
        'origin': ADDRESS,
        'type': 'success',
        'message': 'process_main is running'}))
    
    try:
        with serial.Serial(ADDRESS, BAUD, timeout = 10) as PORT:
        
            COM_INPUT.put({
                'destination': 'TO_MAIN',
                'origin': ADDRESS,
                'type': 'success',
                'message': 'connected to robot'})
        
            while(True):
                
                PORT.write(str.encode(ADDRESS + " hello"))
                            
                RESPONSE = PORT.readline()
                
                DECODED_RESPONSE = bytes.decode(RESPONSE)
            
                COM_INPUT.put({
                    'destination': 'TO_MAIN',
                    'origin': ADDRESS,
                    'type': 'running',
                    'message': DECODED_RESPONSE})
                
                sleep(2)
                
            COM_INPUT.put({
                'destination': 'TO_MAIN',
                'origin': ADDRESS,
                'type': 'failure',
                'message': 'exited proces_main'})
            
    except:
        COM_INPUT.put({'destination': 'TO_MAIN',
                           'origin': ADDRESS,
                           'type': 'failure',
                           'message': 'exited proces_main'})
    return 0
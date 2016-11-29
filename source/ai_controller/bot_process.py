'''
Created on Nov 1, 2016

@author: Trevor
'''
from time import sleep
import serial

BAUD = '9600'
replied = False

def bot_listener_main(ADDRESS, COM_INPUT, PROCESS_Q):
    #LISTEN_INPUT.put({
    #    'destination': 'MAIN_INPUT',
    #    'origin': ADDRESS,
    #    'type': 'result',
    #    'message': 'Process_listener started'})

    try:
        with serial.Serial(ADDRESS, BAUD, timeout = 10) as PORT:
        
            #LISTEN_INPUT.put({
            #    'destination': 'MAIN_INPUT',
            #    'origin': ADDRESS,
            #    'type': 'result',
            #    'message': 'Connection successful'})
            
            PORT.write(str.encode("1"))

            RESPONSE = PORT.readline()

            DECODED_RESPONSE = bytes.decode(RESPONSE)

            if not RESPONSE == b'':
                COM_INPUT.put({
                    'destination': 'MAIN_INPUT',
                    'origin': ADDRESS,
                    'type': 'result',
                    'message': 'add'})
                
                COM_INPUT.put({
                    'destination': 'MAIN_INPUT',
                    'origin': ADDRESS,
                    'type': 'log',
                    'message': RESPONSE})
                
            else:
                COM_INPUT.put({
                    'destination': 'MAIN_INPUT',
                    'origin': ADDRESS,
                    'type': 'command',
                    'message': 'failure'})
                
                COM_INPUT.put({
                    'destination': 'MAIN_INPUT',
                    'origin': ADDRESS,
                    'type': 'log',
                    'message': RESPONSE})
            
    except:
        COM_INPUT.put({
            'destination': 'MAIN_INPUT',
            'origin': ADDRESS,
            'type': 'command',
            'message': 'failure'})
        
    return 0

def bot_process_main(ADDRESS, COM_INPUT, PROCESS_Q):
    COM_INPUT.put(({
        'destination': 'MAIN_INPUT',
        'origin': ADDRESS,
        'type': 'result',
        'message': 'process_main is running'}))
    
    try:
        with serial.Serial(ADDRESS, BAUD, timeout = 10) as PORT:
        
            COM_INPUT.put({
                'destination': 'MAIN_INPUT',
                'origin': ADDRESS,
                'type': 'result',
                'message': 'connected to robot'})
        
            while True:
                
                PORT.write(str.encode("1"))
                            
                RESPONSE = PORT.readline()
                
                DECODED_RESPONSE = bytes.decode(RESPONSE)
                
                if RESPONSE == b'':   
                        
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
                        'message': DECODED_RESPONSE})
                
                    sleep(2)
                                
            
    except:
        COM_INPUT.put({'destination': 'MAIN_INPUT',
                           'origin': ADDRESS,
                           'type': 'command',
                           'message': 'failure'})
    return 0
'''
Created on Nov 1, 2016

@author: Trevor
'''
from multiprocessing import Process, Queue
import bot_process
import tcp_listener
import serial.tools.list_ports as ports_list
from time import sleep

#stores the connections
CON_DICT = {}

def com_level_main(COM_INPUT, MOV_INPUT, MAIN_INPUT):
    
    MAIN_INPUT.put({
        'destination': 'MAIN_INPUT',
        'origin': 'COM_INPUT',
        'type': 'info',
        'message': 'Com_level is running'})

    CON_DICT['COM_INPUT'] = ['running', COM_INPUT, None]
    CON_DICT['MOV_INPUT'] = ['running', MOV_INPUT, None]
    CON_DICT['MAIN_INPUT'] = ['running', MAIN_INPUT, None]

    # start the tcp listener
    TCP_LISTENER_QUEUE = Queue()

    TCP_LISTENER = Process(target=tcp_listener.tcp_listener_main, args=(COM_INPUT, TCP_LISTENER_QUEUE))
    TCP_LISTENER.start()
    
    CON_DICT['TCP_LISTENER'] = ['running', TCP_LISTENER_QUEUE, None]

    # infinite loop to keep checking the queue for information
    while True:
        '''MAIN_INPUT.put({
            'destination': 'MAIN_INPUT',
            'origin': 'COM_INPUT',
            'type': 'info',
            'message': 'Com_level is still running'})
        '''


        #get items from queue until it's empty
        while not COM_INPUT.empty():

            RESPONSE = COM_INPUT.get()

            #make sure the response is a list object
            if isinstance(RESPONSE, dict):
                
                #if the item in index 0 is a 'add',
                #start a new bot_process
                #add the new process to the Q_DICT
                if RESPONSE.get('message') == 'add':

                    PROCESS_QUEUE = None

                    if RESPONSE.get('origin') not in CON_DICT:
                        
                        PROCESS_QUEUE = Queue()
                        
                    else:
                        CON_DICT[RESPONSE['origin']][2].join()
                        PROCESS_QUEUE = CON_DICT[RESPONSE['origin']][1]

                    #start new process if the serial port is not already open
                    BOT_PROCESS = Process(target=bot_process.bot_process_main, args=(RESPONSE['origin'], COM_INPUT, PROCESS_QUEUE))
                    BOT_PROCESS.start()
                    

                    CON_DICT[RESPONSE['origin']] = ['running', PROCESS_QUEUE, BOT_PROCESS]

                #if the item in index 1 is a '1', remove the
                #process from the Q_DICT
                elif RESPONSE['message'] == 'failure':
                    
                    CON_DICT[RESPONSE['origin']][2].join()
                    del CON_DICT[RESPONSE['origin']]
                    
                #relay message to destination
                if RESPONSE['destination'] != "COM_INPUT":
                    RELAY_TO = CON_DICT[RESPONSE['destination']][1]

                    RELAY_TO.put(RESPONSE)

                else:
                    MAIN_INPUT.put(RESPONSE)


            #un-handled message
            else:

                #send this un-handled message to main
                #for raw output to the screen
                MAIN_INPUT.put(RESPONSE)
        
        #create list of open ports
        PORTS = list(ports_list.comports())
        
        #for each port in the list: check if port already exists
        #if exists then skip
        for p in PORTS:
            
            ADDRESS = p[0]
                
            PROCESS_QUEUE = Queue()

            if ADDRESS not in CON_DICT:
                
                #start new process if the serial port is not already open
                BOT_PROCESS = Process(target=bot_process.bot_listener_main, args=(ADDRESS, COM_INPUT, PROCESS_QUEUE))
                BOT_PROCESS.start()
                
                CON_DICT[ADDRESS] = ['checking', PROCESS_QUEUE, BOT_PROCESS]
            
        #sleep so that this is not constantly eating processing time
        sleep(1)
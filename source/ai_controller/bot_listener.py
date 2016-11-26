'''
Created on Nov 1, 2016

@author: Trevor
'''
from multiprocessing import Process, Queue
from time import sleep
from bot_process import process_listener
import serial.tools.list_ports as ports_list

Q_DICT = None
   
def listener_main(COM_INPUT, LISTEN_INPUT):
    #main process loop
    while(True):   
                 
        #sleep so that this is not constantly eating processing time
        sleep(10)
                
        #relay the response from 
        while not LISTEN_INPUT.empty():
            RESPONSE = LISTEN_INPUT.get()
            
            if RESPONSE['type'] == 'add':
                COM_INPUT.put(RESPONSE)
                
            elif RESPONSE['isDict'] == 'yes':
                Q_DICT = RESPONSE['Q_LIST']
            
            else:
                COM_INPUT.put(RESPONSE)

        #verify listener is running
        #COM_INPUT.put({
        #    'destination': 'TO_MAIN',
        #    'origin': 'bot_listener',
        #    'type': 'success',
        #    'message': 'Bot_listener is running'})
    
        #grab a list of open serial ports
        PORTS = list(ports_list.comports())
                
        #for each loop through all the open serial ports
        for p in PORTS:
            
            COM_INPUT.put({
                'destination': 'TO_MAIN',
                'origin': 'bot_listener',
                'type': 'success',
                'message': p[0]})
            
            ADDRESS = p[0]
                
            PROCESS_Q = Queue()

            #start new process if the serial port is not already open
            BOT_PROCESS = Process(target=process_listener, args=(ADDRESS, LISTEN_INPUT, PROCESS_Q))
            BOT_PROCESS.start()
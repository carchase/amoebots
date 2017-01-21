'''
Created on Nov 1, 2016

@author: Trevor
'''
from multiprocessing import Process, Queue
import bot_process
import tcp_listener
import serial.tools.list_ports as ports_list
from time import sleep
from message import Message

# stores the connections
CON_DICT = {}

def com_level_main(COM_INPUT, MOV_INPUT, MAIN_INPUT):
    MAIN_INPUT.put( Message('COM_LEVEL', 'MAIN_LOG', 'info', {'message': 'Com_level is running'}))

    CON_DICT['COM_LEVEL'] = ['running', COM_INPUT, None]
    CON_DICT['MOV_LEVEL'] = ['running', MOV_INPUT, None]
    CON_DICT['MAIN_LOG'] = ['running', MAIN_INPUT, None]

    # start the tcp listener
    tcpListenerQueue = Queue()
    tcpListener = Process(target=tcp_listener.tcp_listener_main, args=(COM_INPUT, tcpListenerQueue))
    tcpListener.start()
    CON_DICT['TCP_LISTENER'] = ['running', tcpListenerQueue, None]

    # infinite loop to keep checking the queue for information
    while True:
        try:

            # get items from queue until it's empty
            while not COM_INPUT.empty():

                response = COM_INPUT.get()

                # make sure the response is a list object
                if isinstance(response, Message):
                    
                    # if the item in index 0 is a 'add',
                    # start a new botProcess
                    # add the new process to the Q_DICT
                    if response.category == 'command' and response.data.get('directive') == 'add':

                        processQueue = None

                        if response.origin not in CON_DICT:
                            processQueue = Queue()
                            
                        else:
                            CON_DICT[response.origin][2].join()
                            processQueue = CON_DICT[response.origin][1]

                        # start new process if the serial port is not already open
                        botProcess = Process(target=bot_process.bot_process_main, args=(response.origin, COM_INPUT, processQueue))
                        
                        # push the data to the process
                        if response.data != None:
                            processQueue.put(response.data)

                        botProcess.start()

                        CON_DICT[response.origin] = ['running', processQueue, botProcess]

                        # forward to the mov level
                        response.destination = "MOV_LEVEL"
                    # if there was an error then close the connection
                    elif response.category == 'command' and response.data.get('directive') == 'failure':
                        
                        CON_DICT[response.origin][2].join()
                        del CON_DICT[response.origin]
                        
                        # forward to the mov level
                        response.destination = "MOV_LEVEL"

                    elif response.category == 'response':
                        # TODO: Get the revelant data and forward it to MOV_LEVEL
                        response.destination = "MAIN_LOG"
                        
                    # relay message to destination
                    if response.destination != "COM_LEVEL":
                        RELAY_TO = CON_DICT[response.destination][1]

                        RELAY_TO.put(response)

                    else:
                        MAIN_INPUT.put(response)


                # un-handled message
                else:

                    # send this un-handled message to main
                    # for raw output to the screen
                    MAIN_INPUT.put(response)
            
            # create list of open ports
            ports = list(ports_list.comports())
            
            # for each port in the list: check if port already exists
            # if exists then skip
            for p in ports:
                
                address = p[0]
                    
                processQueue = Queue()

                if address not in CON_DICT:

                    MAIN_INPUT.put( Message('COM_LEVEL', 'MAIN_LOG', 'info', {'message': 'Attempting to connect to com port: ' + address}))
                    
                    #start new process if the serial port is not already open
                    botProcess = Process(target=bot_process.bot_listener_main, args=(address, COM_INPUT, processQueue))
                    botProcess.start()
                    
                    CON_DICT[address] = ['checking', processQueue, botProcess]
                
            # sleep so that this is not constantly eating processing time
            sleep(.1)

        except Exception as e:
            MAIN_INPUT.put( Message('COM_LEVEL', 'MAIN_LOG', 'error', {'message': str(e)}))

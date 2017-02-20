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
INFINITE_LOOP = True

def com_level_main(COM_INPUT, MOV_INPUT, MAIN_INPUT, OPTIONS):
    MAIN_INPUT.put(Message('COM_LEVEL', 'MAIN_LEVEL', 'info', {'message': 'Com_level is running'}))

    CON_DICT['COM_LEVEL'] = ['running', COM_INPUT, None]
    CON_DICT['MOV_LEVEL'] = ['running', MOV_INPUT, None]
    CON_DICT['MAIN_LEVEL'] = ['running', MAIN_INPUT, None]

    # start the tcp listener
    tcpListenerQueue = Queue()
    tcpListener = Process(target=tcp_listener.tcp_listener_main, args=(COM_INPUT, tcpListenerQueue))
    tcpListener.start()
    CON_DICT['TCP_LISTENER'] = ['running', tcpListenerQueue, tcpListener]

    global INFINITE_LOOP
    INFINITE_LOOP = True

    # infinite loop to keep checking the queue for information
    while INFINITE_LOOP:
        try:
            # get items from queue until it's empty
            while not COM_INPUT.empty():

                message = COM_INPUT.get()

                # make sure the message is a Message object
                if isinstance(message, Message):

                    # Appropriately process the message depending on its category
                    if message.category == 'command':
                        process_command(message)

                    elif message.category == 'response':
                        # TODO: Get the revelant data and forward it to MOV_LEVEL

                        # if isinstance(response.data, dict):
                        #     print(response.data)

                        message.destination = "MAIN_LEVEL"

                    # relay message to destination
                    if message.destination != "COM_LEVEL":
                        relay_to = CON_DICT[message.destination][1]

                        relay_to.put(message)

                    elif OPTIONS['DUMP_MSGS_TO_MAIN']:
                        MAIN_INPUT.put(message)

                # un-handled message
                else:
                    # send this un-handled message to main
                    # for raw output to the screen
                    MAIN_INPUT.put(message)

            # check for unconnected robots
            scan_com_ports()

            # sleep so that this is not constantly eating processing time
            sleep(.1)

        except Exception as err:
            MAIN_INPUT.put(Message('COM_LEVEL', 'MAIN_LEVEL', 'error', {'message': str(err)}))

def process_command(message):
    if message.data.get('directive') == 'add':
        # if the command is an 'add' directive then start a new botProcess
        # and add the new process to the CON_DICT
        processQueue = Queue()

        # start new process if the serial port is not already open
        botProcess = Process(target=bot_process.bot_process_main,
                             args=(message.origin, CON_DICT["COM_LEVEL"][1], processQueue))

        # push the data to the process
        if message.data.get("args") != None:
            processQueue.put(message.data.get("args"))

        botProcess.start()

        CON_DICT[message.origin] = ['running', processQueue, botProcess]

        # forward to the mov level
        message.destination = "MOV_LEVEL"

    elif message.data.get('directive') == 'failure':
        # if there was an error then close the connection

        CON_DICT[message.origin][2].join()
        del CON_DICT[message.origin]

        # forward to the mov level
        message.destination = "MOV_LEVEL"

    elif message.data.get('directive') == 'shutdown' and message.origin == 'MAIN_LEVEL':
        # the level has been told to shutdown.  Kill all the children!!!
        # Loop over the child processes and shut them shutdown

        CON_DICT["MAIN_LEVEL"][1].put(Message('COM_LEVEL', 'MAIN_LEVEL', 'info', {
            'message': 'Shutting down COM_LEVEL and child processes'
        }))

        for key in CON_DICT:
            # Ensure that the connection is a child and not just a queue
            if CON_DICT[key][2] != None:
                CON_DICT[key][1].put(Message('COM_LEVEL', key, 'command', {
                    'message': 'Shutdown ' + key,
                    'directive': 'shutdown',
                }))
                CON_DICT[key][2].join()
                CON_DICT[key][0] = "stopped"

        # End the com_level
        global INFINITE_LOOP
        INFINITE_LOOP = False

def scan_com_ports():
    # create list of open ports
    ports = list(ports_list.comports())

    # for each port in the list: check if port already exists
    # if exists then skip
    for p in ports:

        address = p[0]

        processQueue = Queue()

        if address not in CON_DICT:

            CON_DICT["MAIN_LEVEL"][1].put(Message('COM_LEVEL', 'MAIN_LEVEL', 'info', {
                'message': 'Attempting to connect to com port: ' + address
            }))

            #start new process if the serial port is not already open
            botProcess = Process(target=bot_process.bot_listener_main,
                                 args=(address, CON_DICT["COM_LEVEL"][1], processQueue))
            botProcess.start()

            CON_DICT[address] = ['checking', processQueue, botProcess]

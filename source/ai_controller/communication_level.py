'''
Created on Nov 1, 2016

@author: Trevor
'''
from multiprocessing import Process, Queue, Array
from bot_listener import listener_main
from bot_process import process_main
from time import sleep

#stores the ports
Q_DICT = {}

def com_level_main(COM_INPUT, TO_MOVEMENT, TO_MAIN):

    Q_DICT['COM_INPUT'] = COM_INPUT
    Q_DICT['TO_MOVEMENT'] = TO_MOVEMENT
    Q_DICT['TO_MAIN'] = TO_MAIN
    LISTEN_INPUT = Queue()
    Q_DICT['listener'] = LISTEN_INPUT
    #create bot_listener process
    BOT_LISTENER = Process(target=listener_main, args=(COM_INPUT, LISTEN_INPUT))

    #start bot_listener process
    BOT_LISTENER.start()

    #infinite loop to keep checking the queue for information
    while(True):

        LISTEN_INPUT.put({
            'isDict': 'yes',
            'Q_DICT':Q_DICT})

        #get items from q until it's empty
        while not COM_INPUT.empty():

            #print item to console
            RESPONSE = COM_INPUT.get()

            #make sure the response is a list object
            if isinstance(RESPONSE, dict):
                
                #if the item in index 1 is a '0',
                #start a new bot_process
                #add the new process to the Q_DICT
                if RESPONSE['type'] == 'add':
                    
                    TO_MAIN.put({
                        'destination': 'TO_MAIN',
                        'origin': RESPONSE['origin'],
                        'type': 'added',
                        'message': 'the process was added'})

                    NEW_Q = Queue()

                    #start new process if the serial port is not already open
                    BOT_PROCESS = Process(target=process_main, args=(RESPONSE['origin'], COM_INPUT, NEW_Q))
                    BOT_PROCESS.start()
                    

                    Q_DICT[RESPONSE['origin']] = NEW_Q
                    TO_MOVEMENT.put(RESPONSE)
                    
                    #comment out later
                    TO_MAIN.put(RESPONSE)

                #if the item in index 1 is a '1', remove the
                #process from the Q_DICT
                elif RESPONSE['type'] == 'failure':
                    del Q_DICT[RESPONSE['origin']]
                    TO_MOVEMENT.put(RESPONSE)

                    #comment out later
                    TO_MAIN.put(RESPONSE)
                    
                #relay message to destination
                else:
                    RELAY_TO = Q_DICT[RESPONSE['destination']]

                    RELAY_TO.put(RESPONSE)


            #un-handled message
            else:

                #send this un-handled message to main
                #for raw output to the screen
                TO_MAIN.put(RESPONSE)

        #sleep so that this is not constantly eating processing time
        sleep(1)
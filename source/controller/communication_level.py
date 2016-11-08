'''
This file contains the code for the connunication level.

Created on Nov 1, 2016
View the full repository here https://github.com/car-chase/amoebots
'''
#from multiprocessing import Process, Queue, Lock as l
#from bot_listener import listener_main
#from time import sleep
import serial.tools.list_ports

baud = '9600'

if __name__ == '__main__':
    #q = Queue()
    #bot_listener = Process(target=listener_main, args=(q,l,baud))
    

    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print (p[0]) 
    print('Finished')
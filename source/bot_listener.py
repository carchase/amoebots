'''
This file contains the code for the bot listener.  This process scans for new 
controller connections and spins off new processes to handle them.

Created on Nov 1, 2016
View the full repository here https://github.com/car-chase/amoebots
'''
from time import sleep
import serial
import serial.tools.list_ports

def listener_main(q,l,baud):
    
    while(True):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print (p[0])
        print('Finished')
        sleep(5) 
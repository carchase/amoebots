'''
Created on Nov 1, 2016

@author: Trevor
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
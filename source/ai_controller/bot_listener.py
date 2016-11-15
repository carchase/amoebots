'''
Created on Nov 1, 2016

@author: Trevor
'''
from multiprocessing import Process
from time import sleep
from bot_process import process_main
import serial.tools.list_ports as ports_list

port_list = ()

#checks that a port isn't already open
def exists(addr):
    
    #checks for the current port in the port list
    if addr in port_list:
        return True;
    else:
        return False;
    
def listener_main(q, a):
    port_list = a
    
    #main process loop
    while(True):
               
        q.put('bot_listener is running')
    
        #grab a list of open serial ports
        ports = list(ports_list.comports())
                
        q.put('\tPorts:\t' + ', '.join(port_list) + ']')
        #for each loop through all the open serial ports
        for p in ports:
            addr = p[0]
            
            #check that the port hasn't already been opened
            if not exists(addr):
                q.put('a new port is open')
                
                #start new process if the serial port is not already open
                bot_process = Process(target=process_main, args=(addr,q))
                bot_process.start()
                
        #sleep so that this is not constantly eating processing time
        sleep(5)
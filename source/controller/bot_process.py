'''
Created on Nov 1, 2016

@author: Trevor
'''
from multiprocessing import Queue
from time import sleep
import serial

baud = '9600'

def process_main(addr, q):
    q2 = Queue()
    q.put([addr,'-1', 'process_main is running', q2])
    try:
        with serial.Serial(addr, baud) as port:
        
            q.put([addr,'0'])
        
            while(True):
                            
                x = port.readline()
                
                s = bytes.decode(x)
            
                q.put(s)
                
                port.write(str.encode(addr + " hello"))
            
                sleep(2)
    except:
        q.put([addr,'1', 'exited process_main'], q2)
    return 0
'''
Created on Sep 7, 2016

@author: Trevor 
'''
import serial

addr = 'COM5'
baud = '9600'
fname = 'my_test.dat'
fmode = 'w'
reps = 100
bufferVal = 256

with serial.Serial(addr,baud) as port, open(fname,fmode, bufferVal) as outf:
    print(port)
    print(outf)
#    header = "Is it writing to file?\n"
#    outf.write(header)
    for i in range(reps):
        x = port.readline()
        s = bytes.decode(x)
        print(s)
        outf.write(s)
        outf.write('\n')
        outf.flush()
        port.write(str.encode("hello"))
import serial
from time import sleep

port = "COM6"
ser = serial.Serial(port, 38400, timeout=0)

while True:
    data = ser.read(9999)
    if len(data) > 0:
        print 'Got:', data

    sleep(1)
    print 'not blocked'

ser.close()
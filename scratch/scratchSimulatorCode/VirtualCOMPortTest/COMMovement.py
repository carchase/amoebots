import serial


#Open up a port
port = "COM6"
ser = serial.Serial(port, 38400, timeout=0)

ser.write()
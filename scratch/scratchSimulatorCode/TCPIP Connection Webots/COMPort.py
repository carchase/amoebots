import serial

port = 'COM6'
ser = serial.Serial(port, 38400)

ser.write('Hello, there, COM Port!')

ser.close()
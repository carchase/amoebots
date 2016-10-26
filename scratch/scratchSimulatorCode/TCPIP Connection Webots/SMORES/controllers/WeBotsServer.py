#This is going to be the test for communicating over TCP/IP from a server to webots
#in a client/server relationship.
#Server Side

import socket
from controller import *

TCP_IP = '10.100.242.182'
TCP_Port = 4999
BufferSize = 20

initialize_controller()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_Port))
s.listen(5)

conn, addr = s.accept()
print('Connection Address: ', addr)
while 1:
    data = conn.recv(BufferSize)
    if not data:
        break
    print('received data: ', data)
    conn.send(data) #echo
conn.close()
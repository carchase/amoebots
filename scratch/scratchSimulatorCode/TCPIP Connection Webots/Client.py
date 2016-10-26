import socket

HOST_IP = '192.168.2.80'
PORT = 4999
BufferSize = 24
Message = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST_IP, PORT))
s.send(Message)
data = s.recv(BufferSize)

s.shutdown
s.close()

print "receive data: ", data



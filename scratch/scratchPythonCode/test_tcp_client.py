import socket

HOST_IP = 'localhost'
PORT = 5000
BufferSize = 24
Message = b'{\"type\": \"SMORES\",\"id\": \"robot-1\"}'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST_IP, PORT))
s.send(Message)
data = s.recv(BufferSize)

s.shutdown
s.close()

print ("receive data: ", data)



import socket
import socketserver
from time import sleep

class TCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		self.data = None
		while self.data != 'QUIT':
			self.data = self.request.recv(1024).strip().upper()
			if self.data == '':
				sleep(1)
			else:
				self.request.send(self.data)

HOST_IP = socket.gethostbyname(socket.gethostname())
PORT = 5000
BufferSize = 1024
Message = b'{\"type\": \"SMORES\",\"id\": \"robot-1\", \"ip\": \"' + bytes(HOST_IP, 'utf-8') + b'\"}'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST_IP, PORT))
s.send(Message)
data = s.recv(1024).strip().decode()
host = data.split(' ')

print("receive data: ", data)

s.shutdown
s.close()

server = socketserver.TCPServer((host[0], int(host[1])), TCPHandler)
server.handle_request()
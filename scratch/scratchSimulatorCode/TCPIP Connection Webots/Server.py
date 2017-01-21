import socket
#from controller import *
import sys

#The program should scan for a host if there is no IP address provided.
#This is the client which will be receiving info from the server.
HOST = '10.100.242.182'
PORT = 8000

#Open a socket.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

#Listen for connection.
server_socket.listen(5)
print "Listening on Socket."

while True:
    try:
        (client_socket, address) = server_socket.accept()
        print "Connected to: ", address, "\n"
    except socket.error as e:
        print "Error establishing connection: " + str(e)
        pass
    client_socket.settimeout(1)

    timeout_hit = False

    while not timeout_hit:
        try:
            message = client_socket(1024)
        except socket.error:
            print "Something bwoke!"
            timeout_hit = True
            server_socket.close()
            break

client_socket.close()
server_socket.close()

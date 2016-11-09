import socket
import time

host, port = '10.100.231.123', 5000
#data = 'My ID is: 1'.join(sys.argv[1:])
data = 'My ID is: 1'

while True:
    #create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connect to the server and send data
    sock.connect((host, port))
    sock.send(data + '\n')

    #receive data from the server and shut down.
    received = str(sock.recv(1024))

    print 'Sent:        {}'.format(data)
    print 'Received:    {}'.format(received)
    time.sleep(3)
import socket
import time

host, port = '10.100.231.123', 5000
#data = 'My ID is: 2'.join(sys.argv[1:])
data = 'My ID is: 2'

while True:
    #create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #connect to the server and send data
        sock.connect((host, port))
        sock.send(bytes(data + '\n', 'utf-8'))

        #receive data from the server and shut down.
        received = str(sock.recv(1024), 'utf-8')

    print('Sent:        {}'.format(data))
    print('Received:    {}'.format(received))
    time.sleep(3)
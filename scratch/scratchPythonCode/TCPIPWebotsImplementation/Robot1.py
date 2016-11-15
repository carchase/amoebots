import socket

def main():
    host, port = 'localhost', 5000
    # data = 'My ID is: 1'.join(sys.argv[1:])
    data = 'My ID is: 1'

    # create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server and send data
    sock.connect((host, port))
    sock.send(data + '\n')

    # receive data from the server and shut down.
    received = str(sock.recv(1024)).split()

    print 'Sent:        {}'.format(data)
    print 'Received:    {}'.format(received[0] + ', ' + received[1])

    hostport = SetupNewHostPort(received)

    StartServer(hostport[0], hostport[1])

def SetupNewHostPort(hostport):
    host = hostport[0]
    port = int(hostport[1])
    return host, port


def StartServer(host, port):
    BufferSize = 24
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    print 'Ready to fulfill requests. \n Listening on port: ', port
    server.listen(5)

    while True:
        #This is an attempt to accept the request to the client socket.
        try:
            (client, address) = server.accept()
            print'connected to: ', address, '\n'
        except socket.error as e:
            print 'There was an error establishing a connection to', client, ': ' + e.message
            pass
        #make sure that the client doesn't timeout.
        client.settimeout(1)
        #currently, there is not a timeout with the client.
        timeout_hit = False
        #So while there isn't a timeout with the client, receive the message from the client.
        while not timeout_hit:
            try:
                #Here is the received message.
                message = client(1024)
                #The message is then passed to the APICommand function where there control of the robots will happen.
                APICommand(message)
            except socket.error:
                print 'There was a problem receiving the message from the client. \n' \
                      'Closing the server connection now...'
                timeout_hit = True
                server.close()



def APICommand(command):
    print'This is a command that will be sent to the API.', command


main()
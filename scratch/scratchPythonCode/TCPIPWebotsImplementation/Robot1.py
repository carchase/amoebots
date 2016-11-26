import socket
import SocketServer

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

class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #Make calls to the API here. This should handle all the commands.
        #Here are some fake commands for now.
        if(self.data == 'Forward'):
            print 'Forward'
        elif(self.data == 'Left'):
            print 'Left'
        elif(self.data == 'Right'):
            print 'Right'
        elif(self.data == 'Backward'):
            print 'Backward'



def StartServer(host, port):
    # create the server, binding the localhost to the assigned port
    server = SocketServer.TCPServer((host, port), TCPHandler)
    print 'Opening Port on: ', port, '...\n'
    # activate the server and keep it running until told not to.
    server.serve_forever()

    # BufferSize = 24
    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.bind((host, port))
    # print 'Ready to fulfill requests. \n Listening on port: ', port
    # server.listen(5)
    #
    # #There needs to be a function that receives messages.
    # while True:
    #     #This is an attempt to accept the request to the client socket.
    #     try:
    #         (client, address) = server.accept()
    #         print'connected to: ', address, '\n'
    #     except:
    #         print 'There was an error establishing a connection to', client, ': '
    #         pass
    #     #make sure that the client doesn't timeout.
    #     client.settimeout(1)
    #     #currently, there is not a timeout with the client.
    #     timeout_hit = False
    #     #So while there isn't a timeout with the client, receive the message from the client.
    #     while not timeout_hit:
    #         try:
    #             #Here is the received message.
    #
    #             message = client(1024)
    #             if (message != None):
    #                 print 'jhey'
    #             else:
    #                 print 'you dun goofed'
    #                 server.close()
    #             #The message is then passed to the APICommand function where there control of the robots will happen.
    #             APICommand(message)
    #         except:
    #             print 'There was a problem receiving the message from the client. \n' \
    #                   'Closing the server connection now...'
    #             timeout_hit = True
    #             server.close()



def APICommand(command):
    print'This is a command that will be sent to the API.', command


main()
import SocketServer

class TCPHandler(SocketServer.BaseRequestHandler):
    '''
    The request handler.

    This is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the client.
    '''
    # def __init__(self, *args, **kw):
    #     self.clients = {}
    #     super().__init__(*args, **kw)

    def handle(self):
        # data = str(self.request[0].strip(), 'utf-8')
        # addr = self.client_address[0]
        # if not addr in self.clients:
        #     print(data, "joined!")
        #     self.clients[addr] = data
        # else:
        #     print(self.clients[addr], 'wrote:', data)
        # socket.sendall(data.upper(), self.client_address)


        #self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print '{} wrote:'.format(self.client_address)
        print(self.data)
        #just send back the same data, but upper cased
        #self.request.sendall('Acknowledged the connection of: {}'.format(self.clients))
        self.request.sendall(self.data.upper())

if __name__ == '__main__':
    host, port = '10.100.231.123', 5000

    #create the server, binding the local host to 5000
    server = SocketServer.TCPServer((host, port), TCPHandler)
    print('Opening Port...')
    #activate the server and keep it running until told not to.
    server.serve_forever()
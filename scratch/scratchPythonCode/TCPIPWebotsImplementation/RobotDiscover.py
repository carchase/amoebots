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
        #self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #this prints out which client sent the data
        print '{} wrote:'.format(self.client_address)
        #this prints out what the client sent.
        print(self.data)
        #This sends the same info the client sent, back to the client.
        self.request.sendall('localhost 4500')

if __name__ == '__main__':
    host, port = '192.168.2.81', 5000

    #create the server, binding the local host to 5000
    server = SocketServer.TCPServer((host, port), TCPHandler)
    print('Opening Port...')
    #activate the server and keep it running until told not to.
    server.serve_forever()
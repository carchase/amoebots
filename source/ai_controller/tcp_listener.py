'''
Created on Nov 1, 2016

@author: Trevor
'''
import socketserver
import json

SERVER_HOST = 'localhost'
SERVER_PORT = 5000

'''
The data should be an encided dictionary of the following
b'{\"type\": \"SMORES\",\"id\": \"robot-1\"}'
'''

class TCPHandler(socketserver.BaseRequestHandler):
    nextPort = 10000

    def handle(self):
        # self.request is the TCP socket connected to the client
        # data should be a byte string containing an encoded dictionary
        self.data = self.request.recv(1024).strip().decode("utf-8")
        
        # attempt to load the dictionary
        try:
            self.data = json.loads(self.data)

            # check if it is a supported model
            if(self.data.get("type") == "SMORES"):
                # assign the robot a port and inform the com level
                self.request.send(bytes('{"port": ' + str(TCPHandler.nextPort) + '}', "utf-8"))
                TCPHandler.nextPort = TCPHandler.nextPort + 1

            else:
                self.request.send(bytes("Unsupported robot type", "utf-8"))
        
        except:
            # exception occurred, must be unsupported data
            self.request.send(bytes("Unsupported data type", "utf-8"))
        
        finally:
            # close the socket
            self.request.close()
        

def tcp_listener_main(COM_INPUT, PROCESS_QUEUE):    
    COM_INPUT.put({
        'destination': 'MAIN_INPUT',
        'origin': 'TCP_LISTENER',
        'type': 'info',
        'message': 'tcp_listener is running'})

    # create the server, binding the localhost to the assigned port.
    server = socketserver.TCPServer((SERVER_HOST, SERVER_PORT), TCPHandler)

    while True:
        while not PROCESS_QUEUE.empty():
            COM_INPUT.put(AI_INPUT.get())

        server.handle_request()
"""TCPIPController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, LED, DistanceSensor
from controller import Robot
import socket
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  led = robot.getLED('ledname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  led.set(1)
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

        print ('Sent:        {}'.format(data))
        print ('Received:    {}'.format(received[0] + ', ' + received[1]))

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
        print ('Ready to fulfill requests. \n Listening on port: ', port)
        server.listen(5)

    while True:
        #This is an attempt to accept the request to the client socket.
        try:
            (client, address) = server.accept()
            print('connected to: ', address, '\n')
        except socket.error as e:
            print ('There was an error establishing a connection to', client, ': ' + e.message)
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
                print ('There was a problem receiving the message from the client. \n' \
            'Closing the server connection now...')
timeout_hit = True
server.close()



def APICommand(command):
    print ('This is a command that will be sent to the API.', command)


main()
pass

# Enter here exit cleanup code.

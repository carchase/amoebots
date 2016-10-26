from controller import *
import socket
import sys

HOST = ''
PORT = 8888
class MyRobot (Robot):

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((HOST, PORT))
        except(socket.error, msg):
            print('Bind failed. Error Code: ' + str(msg[0]) + 'Message ' + msg[1])
            sys.exit()

        print('Socket bind complete')

        s.listen(10)
        print('Socket now listening')

        conn, addr - s.accept()

        print('Connected with ') + addr[0] + ':' + str(addr[1])

        conn.close()
        s.close()

controller = MyRobot()
controller.run()
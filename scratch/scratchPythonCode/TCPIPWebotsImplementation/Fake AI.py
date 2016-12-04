import socket
import time
def main():
    while 1:
        host, port = '10.100.231.123', 10000
        data = '2 1'

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(data)
        sock.recv(1024)
        time.sleep(1)
main()
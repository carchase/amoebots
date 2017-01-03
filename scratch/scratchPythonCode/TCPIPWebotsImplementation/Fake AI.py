import socket
import time
def main():
    while 1:
        host, port = '192.168.2.82', 1500
        data = '2 100'

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(data)
        sock.recv(1024)
        time.sleep(1)
main()
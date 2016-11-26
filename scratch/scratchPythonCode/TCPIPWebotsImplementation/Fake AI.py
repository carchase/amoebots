import socket

def main():
    host, port = 'localhost', 1500
    data = 'Forward'

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(data + '\n')

main()
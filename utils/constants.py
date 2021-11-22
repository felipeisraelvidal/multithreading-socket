import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5000
ADDR = (IP, PORT)

SIZE = 1024
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = ':q'

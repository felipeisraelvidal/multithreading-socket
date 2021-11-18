# socket library
import socket

# Thread module
from _thread import *
import threading

from bcolors import *

print_lock = threading.Lock()

def threaded(connection, client):
    while True:
        msg = connection.recv(1024)
        if not msg:
            break
        
        decoded_msg = msg.decode('utf-8');
        print(f'{bcolors.OKCYAN}{client[0]}:{client[1]}: {decoded_msg}{bcolors.ENDC}')

        connection.send(decoded_msg.encode('utf-8'))

    print(f'{bcolors.FAIL}Closing connection: {client[0]}:{client[1]}{bcolors.ENDC}')
    connection.close()

def main():
    host = ''
    port = 5000

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (host, port)
    tcp.bind(orig)
    tcp.listen(1)
    print('🔥 Server is listening (waiting for connections)')

    # Forever loop until client closes connection
    while True:
        connection, client = tcp.accept()
        print(f'{bcolors.OKGREEN}Connected to {client[0]} on port {client[1]}{bcolors.ENDC}')

        start_new_thread(threaded, tuple([connection, client]))
    
    tcp.close()

if __name__ == '__main__':
    main()

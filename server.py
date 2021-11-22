import socket
from bcolors import bcolors
from utils import constants
import multiprocessing

def handle_client(connection, client):
    username = f'{client[0]}:{client[1]}'
    print(f'{bcolors.OKGREEN}[NEW CONNECTION] {username} connected{bcolors.ENDC}')

    connected = True
    while connected:
        msg = connection.recv(constants.SIZE).decode(constants.FORMAT)

        if msg == constants.DISCONNECT_MESSAGE:
            connected = False
        else:
            print(f'{bcolors.OKCYAN}{username}: {msg}{bcolors.ENDC}')

            # Send message to client
            enconded_msg = msg.encode(constants.FORMAT)
            connection.send(enconded_msg)

    connection.close()
    print(f'{bcolors.FAIL}[DISCONNECTED] {username} disconnected{bcolors.ENDC}')

def main():
    print('[STARTING] Server is starting...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(constants.ADDR)
    server.listen()
    print(f'[LISTENING] 🔥 Server is listening on {constants.IP}:{constants.PORT}')

    while True:
        connection, client = server.accept()

        proc = multiprocessing.Process(target=handle_client, args=(connection, client))
        proc.start()
        
        # thread = threading.Thread(target=handle_client, args=(connection, client))
        # thread.start()

if __name__ == '__main__':
    main()

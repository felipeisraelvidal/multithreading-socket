import socket
from bcolors import bcolors
from utils import constants
import concurrent.futures
import signal

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def exit_gracefully(*args):
    print("Terminando numa boa", args)
    server.close()
    exit(0)

def setup_exit_signals(server=None):
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

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
    setup_exit_signals()
    
    print('[STARTING] Server is starting...')
    server.bind(constants.ADDR)
    server.listen()
    print(f'[LISTENING] 🔥 Server is listening on {constants.IP}:{constants.PORT}')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []    
        
        while True:
            connection, client = server.accept()# espera
            thread = executor.submit(handle_client, connection=connection, client=client)
            thread.add_done_callback(lambda *args: print("Thread Finished!"))
            futures.append(thread)
            # proc = multiprocessing.Process(target=handle_client, args=(connection, client))
            # proc.start()
            
            # thread = BaseThread(target=handle_client, args=(connection, client))
            # thread.start() #libera

if __name__ == '__main__':
    main()

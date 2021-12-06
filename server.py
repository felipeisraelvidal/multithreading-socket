import socket
from utils.bcolors import bcolors
from utils import constants
import concurrent.futures
import signal
import re

class SocketServer:
    _server = None
    _connections = []
    
    def __init__(self):
        self._server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.setup_exit_signals()
    
    def bind_and_listen(self):
        print("[STARTING] Server is starting...")
        self._server.bind(constants.ADDR)
        self._server.listen()
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"[LISTENING] 🔥 Server is listening on {ip_address}:{constants.PORT}")
    
    def handle_client(self, connection, client):
        username = f"{client[0]}:{client[1]}"
        print(f"{bcolors.OKGREEN}[NEW CONNECTION] {username} connected{bcolors.ENDC}")
        print(f'{bcolors.HEADER}[CONNECTIONS] {len(self._connections)}{bcolors.ENDC}')
        
        connected = True
        while connected:
            msg = connection.recv(constants.SIZE).decode(constants.FORMAT)

            if msg:
                if msg.startswith('echo '):
                    msg = re.sub('^echo\s+', '', msg)

                    print(f"{bcolors.OKCYAN}{username}: {msg}{bcolors.ENDC}")
                
                    # Send message to client
                    enconded_msg = msg.encode(constants.FORMAT)
                    connection.send(enconded_msg)
                elif msg == constants.DISCONNECT_MESSAGE:
                    connected = False
        
        connection.close()    
        print(f'{bcolors.FAIL}[DISCONNECTED] {username} disconnected{bcolors.ENDC}')

        if connection in self._connections:
            self._connections.remove(connection)

        print(f'[CONNECTIONS] {len(self._connections)}')
    
    def accept_connections(self, executor):
        connection, client = self._server.accept()
        self._connections.append(connection)
        thread = executor.submit(
            self.handle_client, connection=connection, client=client
        )
        thread.add_done_callback(lambda *args: {})
    
    def exit_gracefully(self, *args):
        # print("Terminando numa boa", args)
        
        connections_count = len(self._connections)
        if connections_count > 0:
            if connections_count == 1:
                print(f'\n{bcolors.FAIL}Closing 1 connection{bcolors.ENDC}')
            else:
                print(f'\n{bcolors.FAIL}Closing {connections_count} connections{bcolors.ENDC}')
        
        for conn in self._connections:
            try:
                conn.close()
            except Exception:
                print("Could not close connection")
        exit(0)
    
    def setup_exit_signals(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

def main():
    socket_server = SocketServer()
    socket_server.bind_and_listen()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            socket_server.accept_connections(executor)

if __name__ == "__main__":
    main()

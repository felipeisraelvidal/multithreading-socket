import socket
from bcolors import bcolors
from utils import constants
import concurrent.futures
import signal

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
        print(f"[LISTENING] 🔥 Server is listening on {constants.IP}:{constants.PORT}")
    
    @staticmethod
    def handle_client(connection, client):
        username = f"{client[0]}:{client[1]}"
        print(f"{bcolors.OKGREEN}[NEW CONNECTION] {username} connected{bcolors.ENDC}")
        
        connected = True
        while connected:
            msg = connection.recv(constants.SIZE).decode(constants.FORMAT)
            
            if msg == constants.DISCONNECT_MESSAGE:
                connected = False
            else:
                print(f"{bcolors.OKCYAN}{username}: {msg}{bcolors.ENDC}")
                
                # Send message to client
                enconded_msg = msg.encode(constants.FORMAT)
                connection.send(enconded_msg)
        
        connection.close()
        print(f'{bcolors.FAIL}[DISCONNECTED] {username} disconnected{bcolors.ENDC}')
    
    def accept_connections(self, executor):
        connection, client = self._server.accept()
        self._connections.append(connection)
        thread = executor.submit(
            SocketServer.handle_client, connection=connection, client=client
        )
        thread.add_done_callback(lambda *args: print("Thread Finished!"))
    
    def exit_gracefully(self, *args):
        # print("Terminando numa boa", args)
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

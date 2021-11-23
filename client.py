import socket
from bcolors import bcolors
from utils import constants
import signal
import os

class SocketClient:
    _client = None
    _connected = False
    _name = None
    _host = None
    _port = None

    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setup_exit_signals()

    def _print_help(self):
        print(f'{bcolors.BOLD}-> Type your message and press enter to send it')
        print(f'-> Type ":q" or Control+C to exit')
        print(f'-> If you need some help, type "{constants.HELP_MESSAGE}"{bcolors.ENDC}')

    def _quit(self, send_message=True):
        if send_message:
            self._client.send(constants.DISCONNECT_MESSAGE.encode(constants.FORMAT))

        self._connected = False
        
        print(f'{bcolors.FAIL}[DISCONNECTED] Disconnected from server{bcolors.ENDC}')

    def ask_connection(self):
        # Get host
        self._host = input('Host: ')
        
        while not self._host:
            self._host = input('Host: ')
        
        # Get port
        while True:
            try:
                self._port = int(input('Port: '))
                break
            except:
                print('Port must be a number')
        
        # Get server name (optional)
        self._name = input('Name: ')

        if not self._name:
            self._name = 'SERVER'

        os.system('cls||clear')

        # Start connection
        self._start()

    def _start(self):
        self._client.connect((self._host, int(self._port)))
        
        server_host = f'{constants.IP}:{constants.PORT}'
        print(f'{bcolors.OKGREEN}[CONNECTECD] Connected to server at {server_host}{bcolors.ENDC}')
        
        print(f'{bcolors.BOLD}Welcome to the Echo Server{bcolors.ENDC}')
        self._print_help()

        self._connected = True
        while self._connected:
            msg = input(f'{bcolors.BOLD}>{bcolors.ENDC} ')

            if msg:
                if msg == constants.HELP_MESSAGE:
                    self._print_help()
                else:
                    self._client.send(msg.encode(constants.FORMAT))

                    if msg == constants.DISCONNECT_MESSAGE:
                        self._quit(send_message=False)
                    else:
                        # Receive response from server
                        msg = self._client.recv(constants.SIZE).decode(constants.FORMAT)
                        print(f'{bcolors.OKCYAN}[{self._name}] {msg}{bcolors.ENDC}')
    
    def exit_gracefully(self, *args):
        # print("Terminando numa boa", args)
        self._quit(send_message=True)
        exit(0)
    
    def setup_exit_signals(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

def main():
    client = SocketClient()
    client.ask_connection()

if __name__ == '__main__':
    main()

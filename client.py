import socket
from bcolors import bcolors
from utils import constants
import signal
import os
import re

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
        print(f'{bcolors.BOLD}Valid commands:')
        print(f'  -> echo <msg> \tEnviar mensagem para o servidor')
        print(f'  -> quit \t\tEncerra conexão com o servidor')
        print(f'  -> {constants.HELP_MESSAGE} \t\tMostrar ajuda{bcolors.ENDC}')

    def _encode_message(self, msg):
        return msg.encode(constants.FORMAT)

    def _echo(self, msg):
        encoded_message = self._encode_message(msg)
        self._client.send(encoded_message)

    def _quit(self, send_message=True):
        if send_message:
            encoded_message = self._encode_message(constants.DISCONNECT_MESSAGE)
            self._client.send(encoded_message)

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
                msg = msg.strip(' ').strip('\t')
                
                if msg.startswith('echo '):
                    msg = re.sub('^echo\s+', '', msg)
                    
                    # Send message to the server
                    self._client.send(msg.encode(constants.FORMAT))

                    # Receive response from server
                    msg = self._client.recv(constants.SIZE).decode(constants.FORMAT)
                    print(f'{bcolors.OKCYAN}[{self._name}] {msg}{bcolors.ENDC}')
                elif msg == constants.HELP_MESSAGE:
                    self._print_help()
                elif msg == constants.DISCONNECT_MESSAGE:
                    self._quit(send_message=True)
                else:
                    # print('Invalid command')
                    print('server: invalid command. Type \'help\'')
    
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

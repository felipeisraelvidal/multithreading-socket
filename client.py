import socket
from bcolors import bcolors
from utils import constants

def print_help():
    print(f'{bcolors.BOLD}-> Type your message and press enter to send it')
    print(f'-> Type ":q" to exit')
    print(f'-> If you need some help, type "help"{bcolors.ENDC}')

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(constants.ADDR)
    
    server_host = f'{constants.IP}:{constants.PORT}'
    print(f'{bcolors.OKGREEN}[CONNECTECD] Connected to server at {server_host}{bcolors.ENDC}')
    
    print(f'{bcolors.BOLD}Welcome to the Echo Server{bcolors.ENDC}')
    print_help()

    connected = True
    while connected:
        msg = input(f'{bcolors.BOLD}>{bcolors.ENDC} ')

        if msg:
            if msg == 'help':
                print_help()
            else:
                client.send(msg.encode(constants.FORMAT))

                if msg == ':q':
                    connected = False
                else:
                    # Receive response from server
                    msg = client.recv(constants.SIZE).decode(constants.FORMAT)
                    print(f'{bcolors.OKCYAN}[SERVER] {msg}{bcolors.ENDC}')


if __name__ == '__main__':
    main()

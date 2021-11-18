import socket
from bcolors import *

def main():
    host = '127.0.0.1'
    port = 5000

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (host, port)
    tcp.connect(dest)
    print('Connected to server')

    msg = input(f'{bcolors.BOLD}Send message (Command+X to exit):{bcolors.ENDC} ')
    while msg != '\x18':
        # Send message
        enconded_msg = msg.encode('utf-8')
        tcp.send(enconded_msg)
        
        # Receive message
        received_msg = tcp.recv(1024)
        if not received_msg:
            print(f'{bcolors.FAIL}Invalid Server Response{bcolors.ENDC}')
            break

        decoded_msg = received_msg.decode('utf-8');
        print(f'{bcolors.OKCYAN}-> Server Response: {decoded_msg}{bcolors.ENDC}')

        # Get message to send
        msg = input(f'{bcolors.BOLD}Send message (Command+X to exit):{bcolors.ENDC} ')

    tcp.close()

if __name__ == '__main__':
    main()

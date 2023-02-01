# -*- coding: utf-8 -*-

import argparse, sys
import socket


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--host', required=False, default="127.0.0.1", help='Socket host 지정 (default=127.0.0.1)')
    parser.add_argument('--port', required=False, default=9999, help='Connect port default=9999)')

    args = parser.parse_args()
    port = int(args.port)
    host = args.host

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:

        message = input('Enter the IP(192.168.60.191) of the registered API. or quit : ')
        if message == 'quit' or message == 'exit':
            break

        client_socket.send(message.encode())
        data = client_socket.recv(10240)

        print('Received from the server :', repr(data.decode()))

    client_socket.close()


if __name__ == "__main__":
    main(sys.argv)

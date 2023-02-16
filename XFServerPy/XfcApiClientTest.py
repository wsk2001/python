# -*- coding: utf-8 -*-

import argparse, sys
import socket


def main(argv):
    parser = argparse.ArgumentParser(description='XFC API Client Test App 옵션 지정 방법')
    parser.add_argument('--host', required=False, default="127.0.0.1", help='Socket host 지정 (default=127.0.0.1)')
    parser.add_argument('--port', required=False, default=9999, help='Connect port default=9999)')
    parser.add_argument('--func', required=False, default='api_policy', help='function api_policy/la_policy/sa_policy')
    parser.add_argument('--ip', required=True, help='등록된 client ip')
    parser.add_argument('--policy', required=False, default=None, help='등록된 정책명')

    args = parser.parse_args()
    port = int(args.port)
    host = args.host
    func = args.func
    ip = args.ip
    policy = args.policy

    json_str = "{"
    json_str += "\"policyType\":" + "\"" + func + "\""
    json_str += ",\"ip\":" + "\"" + ip + "\""
    if policy is not None:
        json_str += ",\"policy\":" + "\"" + policy + "\""
    json_str += "}"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.send(json_str.encode())
    data = client_socket.recv(10240)

    print('Received from the server :', repr(data.decode()))

    client_socket.close()


if __name__ == "__main__":
    main(sys.argv)

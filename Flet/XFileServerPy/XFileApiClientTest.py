# -*- coding: utf-8 -*-

import argparse, sys
import socket
import json


# API --policy=api_policy --key=192.168.60.190
#  LA --policy=la_policy --key=192.168.60.190 --subkey=LA001
#  SA --policy=sa_policy --key=192.168.60.190 --subkey=SA001
#  RA --policy=ra_policy --key=192.168.60.190
def main(argv):
    parser = argparse.ArgumentParser(description='XFC API Client Test App 옵션 지정 방법')
    parser.add_argument('--host', required=False, default="127.0.0.1", help='Socket host 지정 (default=127.0.0.1)')
    parser.add_argument('--port', required=False, default=9999, help='Connect port default=9999)')
    parser.add_argument('--policy', required=True, default='api_policy',
                        help='policy type: api_policy/la_policy/sa_policy/ra_policy')
    parser.add_argument('--key', required=True, help='요청 Key (주로 IP)')
    parser.add_argument('--subkey', required=False, default=None, help='sub key (주로 정책명: LA001')

    args = parser.parse_args()
    port = int(args.port)
    host = args.host
    policy = args.policy
    key = args.key
    subkey = args.subkey

    json_str = "{"
    json_str += "\"policyType\":" + "\"" + policy + "\""
    json_str += ",\"key\":" + "\"" + key + "\""
    if subkey is not None:
        json_str += ",\"subKey\":" + "\"" + subkey + "\""
    json_str += "}"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.send(json_str.encode())
    data = client_socket.recv(10240)
    client_socket.close()

    json_str = repr(data.decode())

    print('Received from the server :', json_str)


if __name__ == "__main__":
    main(sys.argv)

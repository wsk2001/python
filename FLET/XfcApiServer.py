# -*- coding: utf-8 -*-

import argparse, sys
import socket
from _thread import *
import sqlite3
import pandas as pd

database_name = './dbms/xfc_policy.db'


# Code that runs in a thread.
def threaded(client_socket, addr):
    print('Connected by :', addr[0], ':', addr[1])

    # Repeat until the client disconnects.
    while True:

        try:
            # 데이터 수신
            data = client_socket.recv(1024)

            if not data:
                print('Disconnected by ' + addr[0], ':', addr[1])
                break

            else:
                query = \
                    "select * from api_policy where ipAddr = \'" + data.decode() + "\';"
                conn = sqlite3.connect(database_name)
                df = pd.read_sql_query(query, conn)
                conn.close()
                value_list = df.values.tolist()

                json_str = "{"
                for v in value_list:
                    json_str += "\"platform\":" + "\"" + v[4] + "\""
                    json_str += ",\"providerName\":" + "\"" + v[5] + "\""
                    json_str += ",\"process\":" + "\"" + v[6] + "\""
                    json_str += ",\"ipAddr\":" + "\"" + v[7] + "\""
                    json_str += ",\"macAddr\":" + "\"" + v[8] + "\""
                    json_str += ",\"modifiedDate\":" + v[9]
                    json_str += ",\"domainKeyId\":" + "\"" + v[10] + "\""
                    json_str += ",\"domainAlgorithm\":" + "\"" + v[11] + "\""
                    json_str += ",\"domainKeyLength\":" + v[12]
                    json_str += ",\"modulus\":" + v[13]
                    json_str += ",\"publicExponent\":" + v[14]
                    json_str += ",\"privateExponent\":" + v[15]
                    json_str += ",\"domainCode\":" + "\"" + v[16] + "\""
                    json_str += ",\"attributeKeyId\":" + "\"" + v[17] + "\""
                    json_str += ",\"attributeIv\":" + "\"" + v[18] + "\""
                    json_str += ",\"attributeAlgorithm\":" + "\"" + v[19] + "\""
                    json_str += ",\"attributeKeyLength\":" + v[20]
                    json_str += ",\"attributeChiperMode\":" + "\"" + v[21] + "\""
                    json_str += ",\"attributePaddingMethod\":" + "\"" + v[22] + "\""
                    json_str += ",\"attributeKeyMaterial\":" + "\"" + v[23] + "\""
                    json_str += ",\"contentsAlgorithm\":" + "\"" + v[24] + "\""
                    json_str += ",\"contentsKeyLength\":" + v[25]
                    json_str += ",\"readChk\":" + "\"" + v[26] + "\""
                    json_str += ",\"writeChk\":" + "\"" + v[27] + "\""
                    json_str += ",\"excuteChk\":" + "\"" + v[28] + "\""
                    json_str += ",\"syncPeriod\":" + v[29]
                    json_str += ",\"logPeriod\":" + v[30]
                    json_str += ",\"excludeExts\":" + "\"" + v[31] + "\""
                    json_str += ",\"decFileSize\":" + v[32]
                    json_str += ",\"encErrorCode\":" + "\"" + v[33] + "\""
                    json_str += ",\"decErrorCode\":" + "\"" + v[34] + "\""

                    break
                json_str += "}"
                client_socket.send(json_str.encode())

        except ConnectionResetError as e:

            print('Disconnected by ' + addr[0], ':', addr[1])
            break

    client_socket.close()


def main(argv):
    parser = argparse.ArgumentParser(description='이 App 은 XFC API 정책을 배포 하는 TCP Server 입니다.')
    parser.add_argument('--host', required=False, default="127.0.0.1", help='Socket host 지정 (default=127.0.0.1)')
    parser.add_argument('--port', required=False, default=9999, help='Connect port default=9999)')

    args = parser.parse_args()
    port = int(args.port)
    host = args.host

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print('server start')

    # When a client connects, the accept function returns a new socket.
    # A new thread communicates using that socket.
    while True:
        print('wait')

        client_socket, addr = server_socket.accept()
        start_new_thread(threaded, (client_socket, addr))

    server_socket.close()


if __name__ == "__main__":
    main(sys.argv)

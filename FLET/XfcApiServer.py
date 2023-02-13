# -*- coding: utf-8 -*-

import argparse, sys
import socket
from _thread import *
import sqlite3
import pandas as pd
import json


database_name = './dbms/xfc_policy.db'


def parse_json(json_str):
    json_dict = json.loads(json_str)

    func_type = None
    str_ip = None
    str_policy = None

    for key, val in json_dict.items():
        if "policyType" in key:
            func_type = val
        elif "ip" in key:
            str_ip = val
        elif "policy" in key:
            str_policy = val
        else:
            continue

    return func_type, str_ip, str_policy

# data 요청 format
# { "policyType": "api_policy/la_policy/sa_policy", "ip": "192.168.60.190", "policy": "la-001" }

def select_api_policy(ip):
    query = \
        "select * from api_policy where ipAddr = \'" + ip + "\';"
    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, conn)
    conn.close()
    value_list = df.values.tolist()

    json_str = ""
    for v in value_list:
        json_str += "{"
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

    if 0 < len(json_str):
        json_str += "}"

    return json_str


def select_la_policy(ip=None, policy=None):
    if ip is None or policy is None:
        return None

    query = \
        "select * from la_policy where ip = \'" + ip + "\' and policy = \'" + policy + "\';"

    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, conn)
    conn.close()
    value_list = df.values.tolist()
    if len(value_list) == 0:
        return None

    json_str = ""
    for v in value_list:
        json_str += "{"
        json_str += "\"ip\":" + "\"" + v[0] + "\""
        json_str += ",\"policy\":" + "\"" + v[1] + "\""
        json_str += ",\"description\":" + "\"" + v[2] + "\""
        json_str += ",\"base_path\":" + "\"" + v[3] + "\""
        json_str += ",\"dir\":" + "\"" + v[4] + "\""
        json_str += ",\"mode\":" + "\"" + v[5] + "\""
        json_str += ",\"time_limit\":" + "\"" + v[6] + "\""
        json_str += ",\"check_file_closed\":" + "\"" + v[7] + "\""
        json_str += ",\"use_file_filter\":" + "\"" + v[8] + "\""
        json_str += ",\"file_filter_type\":" + "\"" + v[9] + "\""
        json_str += ",\"file_filter_exts\":" + "\"" + v[10] + "\""
        json_str += ",\"check_cycle\":" + "\"" + v[11] + "\""
        json_str += ",\"thread_count\":" + "\"" + v[12] + "\""
        json_str += ",\"use_backup\":" + "\"" + v[13] + "\""
        json_str += ",\"backup_path\":" + "\"" + v[14] + "\""
        json_str += ",\"temp_path\":" + "\"" + v[15] + "\""
        json_str += ",\"dir_depth\":" + "\"" + v[16] + "\""
        json_str += ",\"dir_format\":" + "\"" + v[17] + "\""
        json_str += ",\"ymd_offset\":" + "\"" + v[18] + "\""
        json_str += ",\"use_trigger_file\":" + "\"" + v[19] + "\""
        json_str += ",\"trigger_ext\":" + "\"" + v[20] + "\""
        json_str += ",\"trigger_target\":" + "\"" + v[21] + "\""

        break
    json_str += "}"

    return json_str


def select_sa_policy(ip=None, policy=None):
    query = None

    if ip is None:
        return None

    if ip is not None and policy is None:
        query = \
            "select * from sa_policy where ip = \'" + ip + "\';"
    elif ip is not None and policy is not None:
        query = \
            "select * from sa_policy where ip = \'" + ip + "\' and policy = \'" + policy + "\';"
    else:
        return None

    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, conn)
    conn.close()
    value_list = df.values.tolist()
    if len(value_list) == 0:
        return None

    json_str = "["
    first_flag = True
    for v in value_list:
        if first_flag:
            json_str += "{"
            first_flag = False
        else:
            json_str += ",{"

        json_str += "\"ip\":" + "\"" + v[0] + "\""
        json_str += ",\"policy\":" + "\"" + v[1] + "\""
        json_str += ",\"description\":" + "\"" + v[2] + "\""
        json_str += ",\"file_path\":" + "\"" + v[3] + "\""
        json_str += ",\"mode\":" + "\"" + v[4] + "\""
        json_str += ",\"time_limit\":" + "\"" + v[5] + "\""
        json_str += ",\"repeat\":" + "\"" + v[6] + "\""
        json_str += ",\"dir_format\":" + "\"" + v[7] + "\""
        json_str += ",\"ymd_offset\":" + "\"" + v[8] + "\""
        json_str += ",\"dir_depth\":" + "\"" + v[9] + "\""
        json_str += ",\"use_weekday\":" + "\"" + v[10] + "\""
        json_str += ",\"weekdays\":" + "\"" + v[11] + "\""

        if v[12] is not None:
            json_str += ",\"day\":" + "\"" + v[12] + "\""
        else:
            json_str += ",\"day\":" + "\"\""

        if v[13] is not None:
            json_str += ",\"hh\":" + "\"" + v[13] + "\""
        else:
            json_str += ",\"hh\":" + "\"\""

        if v[14] is not None:
            json_str += ",\"mm\":" + "\"" + v[14] + "\""
        else:
            json_str += ",\"mm\":" + "\"\""

        if v[15] is not None:
            json_str += ",\"ss\":" + "\"" + v[15] + "\""
        else:
            json_str += ",\"ss\":" + "\"\""

        json_str += ",\"use_file_filter\":" + "\"" + v[16] + "\""
        json_str += ",\"file_filter_type\":" + "\"" + v[17] + "\""
        json_str += ",\"file_filter_exts\":" + "\"" + v[18] + "\""
        json_str += ",\"check_file_closed\":" + "\"" + v[19] + "\""
        json_str += ",\"thread_count\":" + "\"" + v[20] + "\""
        json_str += ",\"use_backup\":" + "\"" + v[21] + "\""
        json_str += ",\"backup_path\":" + "\"" + v[22] + "\""
        json_str += ",\"temp_path\":" + "\"" + v[23] + "\""
        json_str += ",\"check_cycle\":" + "\"" + v[24] + "\""
        json_str += "}"

    json_str += "]"

    return json_str


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
                rcv_data = data.decode()
                func_type, str_ip, str_policy = parse_json(rcv_data)

                print('receive data: ' + rcv_data)
                if func_type.startswith('api_policy'):
                    json_str = select_api_policy(str_ip)
                elif func_type.startswith('la_policy'):
                    json_str = select_la_policy(str_ip, str_policy if 0 < len(str_policy) else None)
                elif func_type.startswith('sa_policy'):
                    json_str = select_sa_policy(str_ip, str_policy if 0 < len(str_policy) else None)
                else:
                    print('Unknown policy type')
                    break

                print('send data: ' + json_str)
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
        # print('wait')

        client_socket, addr = server_socket.accept()
        start_new_thread(threaded, (client_socket, addr))


    server_socket.close()


if __name__ == "__main__":
    main(sys.argv)

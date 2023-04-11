# -*- coding: utf-8 -*-

import argparse, sys
import socket
from _thread import *
import sqlite3
import pandas as pd
import json

database_name = './dbms/xfc_policy.db'


def parse_json(json_str: str):
    json_dict = json.loads(json_str)

    policy_type = None
    key_val = None
    subkey_val = None

    for key, val in json_dict.items():
        if "policytype" == str(key).lower():
            policy_type = val
        elif "key" == str(key).lower():
            key_val = val
        elif "subkey" == str(key).lower():
            subkey_val = val
        else:
            continue

    return policy_type, key_val, subkey_val


def select_client_(client_name: str):
    if client_name is None:
        return None

    query = \
        "select id, client_name, mac_addr, description, create_date, creator, client_status, client_platform, " \
        "platformver from client " \
        "where client_name = \'" + client_name + "\';"

    print('query: ' + query)

    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, conn)
    conn.close()
    value_list = df.values.tolist()
    if len(value_list) == 0:
        return None

    json_str = ""
    for v in value_list:
        json_str += "{"
        json_str += "\"id\":" + "\"" + v[0] + "\""
        json_str += ",\"client_name\":" + "\"" + v[1] + "\""
        json_str += ",\"mac_addr\":" + "\"" + v[2] + "\""
        json_str += ",\"description\":" + "\"" + v[3] + "\""
        json_str += ",\"create_date\":" + "\"" + str(int(v[4])) + "\""
        json_str += ",\"creator\":" + "\"" + v[5] + "\""
        json_str += ",\"client_status\":" + "\"" + v[6] + "\""
        json_str += ",\"client_platform\":" + "\"" + v[7] + "\""
        json_str += ",\"platformver\":" + "\"" + v[8] + "\""

        break
    json_str += "}"

    json_object = json.loads(json_str)

    json_formatted_str = json.dumps(json_object, indent=2)

    return json_formatted_str


def select_client(client_name: str):
    if client_name is None:
        return None

    query = \
        "select id, client_name, mac_addr, description, create_date, creator, client_status, client_platform, " \
        "platformver from client " \
        "where client_name = \'" + client_name + "\';"

    print('query: ' + query)

    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


def select_agent_policy(client_id: str):
    if client_id is None:
        return None

    query = \
        "select id, policy_type, protocol, sync_period, log_period, creator, create_date, modified_date, " \
        "client_id, enc_id, policy_status, description  from agent_policy " \
        "where client_id = \'" + client_id + "\';"

    print('query: ' + query)

    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


def select_encpolicy(policy_name: str):
    if policy_name is None:
        return None

    query = \
        "select id, policy_name, policy_type, description, algorithm, key_length, share_range, back_migration, " \
        "create_date, modified_date, creator from enc_policy " \
        "where policy_name = \'" + policy_name + "\';"

    print('query: ' + query)

    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def select_target_path(ap_id: str):
    if ap_id is None:
        return None

    query = \
        "select id, tp_path, tp_mode, exclude_exts, tp_uid, tp_gid, ap_id " \
        "from target_path " \
        "where ap_id = \'" + ap_id + "\';"

    print('query: ' + query)

    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def select_access_control(tp_id: str):
    '''
    "\'aaa\', \'bbb\'" 형태로 넘어와야 함
    '''
    if tp_id is None:
        return None

    query = \
        "select id, access_ip, access_sip, access_eip, access_uid, access_gid, access_account, access_passwd, " \
        "access_process, tp_id, access_mac, access_type " \
        "from access_control " \
        "where tp_id in (" + tp_id + ");"

    print('query: ' + query)

    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def select_permission(p_id: str):
    '''
    "\'aaa\', \'bbb\'" 형태로 넘어와야 함
    '''
    if p_id is None:
        return None

    query = \
        "select id, read_chk, write_chk, excute_chk, perm_type, p_id " \
        "from permission " \
        "where p_id in (" + p_id + ");"

    print('query: ' + query)

    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


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
                agent_type, key, subkey = parse_json(rcv_data)

                print('receive data: ' + rcv_data)
                print('******************************************')
                if agent_type:
                    print('agent_type: ' + agent_type)
                if key:
                    print('key       : ' + key)
                if subkey:
                    print('subkey    : ' + subkey)
                print('******************************************')

                if agent_type.startswith('ra_policy'):
                    print('ra_policy, key=' + key)
                    df = select_client(key)
                    id = df[0]["id"]
                    client_name = df[0]["client_name"]
                    mac_addr = df[0]["mac_addr"]
                    description = df[0]["description"]
                    create_date = df[0]["create_date"]
                    creator = df[0]["creator"]
                    client_status = df[0]["client_status"]
                    client_platform = df[0]["client_platform"]
                    platformver = df[0]["platformver"]

                    json_client = "\'client\': {"
                    json_client += "\"id\":" + "\"" + id + "\""
                    json_client += "\",client_name\":" + "\"" + client_name + "\""
                    json_client += "\",mac_addr\":" + "\"" + mac_addr + "\""
                    json_client += "\",description\":" + "\"" + description + "\""
                    json_client += "\",create_date\":" + "\"" + create_date + "\""
                    json_client += "\",creator\":" + "\"" + creator + "\""
                    json_client += "\",client_status\":" + "\"" + client_status + "\""
                    json_client += "\",client_platform\":" + "\"" + client_platform + "\""
                    json_client += "\",platformver\":" + "\"" + platformver + "\""
                    json_client = "}"

                    json_str = json_client

                    df = select_agent_policy(id)


                else:
                    print('Unknown policy type')
                    break

                if json_str is not None:
                    print('send data: ' + json_str)
                    print()
                    client_socket.send(json_str.encode())
                else:
                    print('Data not found!!')
                    break

        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0], ':', addr[1])
            break

    client_socket.close()


def main(argv):
    parser = argparse.ArgumentParser(description='이 App 은 XFC API 정책을 배포 하는 TCP Server 입니다.')
    parser.add_argument('--host', required=False, default="0.0.0.0", help='Socket host 지정 (default=127.0.0.1)')
    parser.add_argument('--port', required=False, default=9999, help='Connect port default=9999)')

    args = parser.parse_args()
    port = int(args.port)

    # 127.0.0.1 로 하면 localhost 에서만 접근 할 수 있다. (loopback, 테스트 또는 보안을 위해 사용시)
    host = args.host

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print('Start XFServer')

    # When a client connects, the accept function returns a new socket.
    # A new thread communicates using that socket.
    while True:
        client_socket, addr = server_socket.accept()
        start_new_thread(threaded, (client_socket, addr))

    server_socket.close()


if __name__ == "__main__":
    main(sys.argv)

'''
[RA 관련 Table]

-- access_control   : 

## client			: ip 를 이용해 client_id 구함.
-- id: c2e1291c-2518-4245-9c11-6aac4be267c9
select * from client 
where 1=1
and client_name = '192.168.60.190'


## agent_policy		: client_id 를 이용해 RA 설정 정보 및 암호화 정책 id(enc_id -> enc_policy id) 구함
-- id: 96261197-cc23-4ae7-9bcc-5d35cb3909cf, 
-- client_id: c2e1291c-2518-4245-9c11-6aac4be267c9
-- enc_id: d9546ee9-f8da-40ff-bbed-9911bf2ec80c
select * from agent_policy 
where client_id = 'c2e1291c-2518-4245-9c11-6aac4be267c9'
and policy_type = 'C'

## enc_policy		: 암호화 정책 조회 (enc_id 사용)
select * from enc_policy 
where id = 'd9546ee9-f8da-40ff-bbed-9911bf2ec80c'

## target_path		: agent_policy id 를 이용해 등록된 경로별 전역 설정 정보 조회 (target_path id => tp_id 포함)
-- id: f6c17db2-06a0-43fc-ac93-2b18daf61ca7, 6a9a1bc6-cda9-46b5-8bfd-83a9ef259a03
select * from target_path 
where ap_id = '96261197-cc23-4ae7-9bcc-5d35cb3909cf'

## access_control : tp_id 를 이용해 상세 접근제어 목록 조회
select * from access_control
where tp_id in ( 'f6c17db2-06a0-43fc-ac93-2b18daf61ca7', '6a9a1bc6-cda9-46b5-8bfd-83a9ef259a03')


## permission : 퍼미션 조회
select * from permission
where p_id in ( 'f6c17db2-06a0-43fc-ac93-2b18daf61ca7', '6a9a1bc6-cda9-46b5-8bfd-83a9ef259a03')
'''

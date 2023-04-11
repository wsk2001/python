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


# data 요청 format
# { "policyType": "api_policy/la_policy/sa_policy", "ip": "192.168.60.190", "policy": "la-001" }

def select_api_policy(ip: str):
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
        json_str += ",\"modulus\":" + "\"" + v[13] + "\""
        json_str += ",\"publicExponent\":" + "\"" + v[14] + "\""
        json_str += ",\"privateExponent\":" + "\"" + v[15] + "\""
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

    json_object = json.loads(json_str)

    json_formatted_str = json.dumps(json_object, indent=2)

    return json_formatted_str


def select_la_policy(ip: str = None, policy: str = None):
    if ip is None or policy is None:
        return None

    if ip is not None and policy is not None:
        query = \
            "select * from la_policy where ip = \'" + ip + "\' and policy = \'" + policy + "\';"
    elif ip is not None and policy is None:
        query = \
            "select * from la_policy where ip = \'" + ip + "\';"
    else:
        return None

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

    json_object = json.loads(json_str)

    json_formatted_str = json.dumps(json_object, indent=2)

    return json_formatted_str


def select_sa_policy(ip: str = None, policy: str = None):
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

    json_str = ""
    first_flag = True
    for v in value_list:
        if first_flag:
            json_str = "["
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

    json_object = json.loads(json_str)

    json_formatted_str = json.dumps(json_object, indent=2)

    return json_formatted_str
    # return json_str


def select_ra_policy(endpoint: str):
    if endpoint is None:
        return None

    query = \
        "select * from ra_policy where endpoint = \'" + endpoint + "\';"

    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, conn)
    conn.close()
    value_list = df.values.tolist()
    if len(value_list) == 0:
        return None

    json_str = ""
    '''
    {
	"response": {
		"header": {
			"resultCode": "00",
			"resultMsg": "NORMAL SERVICE."
		},
		"body": {
			"items": {
				"item": [{
					"airline": "아시아나항공",
					"airport": "마닐라",
					"airportCode": "MNL",
					"carousel": 19,
					"cityCode": "MNL",
					"elapsetime": "0316",
					"estimatedDateTime": "0359",
					"exitnumber": "E",
					"flightId": "OZ704",
					"gatenumber": 32,
					"remark": "도착",
					"scheduleDateTime": "0500",
					"terminalId": "P01"
				}, {
					"airline": "대한항공",
					"airport": "마닐라",
					"airportCode": "MNL",
					"carousel": 10,
					"cityCode": "MNL",
					"elapsetime": "0322",
					"estimatedDateTime": "0410",
					"exitnumber": "B",
					"flightId": "KE624",
					"gatenumber": 251,
					"remark": "도착",
					"scheduleDateTime": "0500",
					"terminalId": "P03"
				}]
			}
		}
	}
}
    계층을 main 에서 한번 더 씌워야 한다.
    '''
    for v in value_list:
        json_str += "{"
        json_str += "\"main\":{"

        json_str += "\"id\":" + "\"" + v[0] + "\""
        json_str += ",\"agent_type\":" + "\"" + v[1] + "\""
        json_str += ",\"share_protocol\":" + "\"" + v[2] + "\""
        json_str += ",\"endpoint\":" + "\"" + v[3] + "\""
        json_str += ",\"encpolicy\":" + "\"" + v[4] + "\""
        json_str += ",\"policyPollingPeriod\":" + "\"" + str(v[5]) + "\""
        json_str += ",\"logSendPollingPeriod\":" + "\"" + str(v[6]) + "\""
        json_str += ",\"targetPath\":" + "\"" + v[7].replace('\n', ',') + "\""
        json_str += ",\"description\":" + "\"" + v[8] + "\""
        json_str += "}"

        # json_str += ",\"clientDto\":" + "\"" + select_client(v[3]) + "\""
        # json_str += ",\"encPolicyDto\":" + "\"" + select_encpolicy(v[4]) + "\""

        json_str += ",\"client_dto\":" + select_client(v[3])
        json_str += ",\"enc_policy_dto\":" + select_encpolicy(v[4])

        json_str += ",\"acls\":" + select_ra_acl(v[0])

        json_str += "}"
        break

    print("json: " + json_str + "\n");

    json_object = json.loads(json_str)

    json_formatted_str = json.dumps(json_object, indent=2)

    return json_formatted_str


def select_ra_acl(ra_id: str):
    query = None

    if ra_id is None:
        return None

    query = \
        "select * from ra_acl where ra_id = \'" + ra_id + "\';"

    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, conn)
    conn.close()
    value_list = df.values.tolist()
    if len(value_list) == 0:
        return None

    json_str = ""
    first_flag = True
    for v in value_list:
        if first_flag :
            json_str += "["
            first_flag = False
        else:
            json_str += ","
        json_str += "{"
        json_str += "\"id\":" + "\"" + v[0] + "\""
        json_str += ",\"ra_id\":" + "\"" + v[1] + "\""
        json_str += ",\"path\":" + "\"" + v[2] + "\""
        json_str += ",\"exclude_exts\":" + "\"" + v[3] + "\""
        json_str += ",\"comm_enc\":" + "\"" + v[4] + "\""
        json_str += ",\"comm_dec\":" + "\"" + v[5] + "\""
        json_str += ",\"ip\":" + "\"" + v[6] + "\""
        json_str += ",\"start_ip\":" + "\"" + v[7] + "\""
        json_str += ",\"end_ip\":" + "\"" + v[8] + "\""
        json_str += ",\"uid\":" + "\"" + str(v[9]) + "\""
        json_str += ",\"gid\":" + "\"" + str(v[10]) + "\""
        json_str += ",\"enc\":" + "\"" + v[11] + "\""
        json_str += ",\"dec\":" + "\"" + v[12] + "\""
        json_str += "}"

    if len(json_str):
        json_str += "]"

    json_object = json.loads(json_str)

    json_formatted_str = json.dumps(json_object, indent=2)

    return json_formatted_str


def select_key_material(key_id: str):
    if key_id is None:
        return None

    query = \
        "select * from key_material where key_id = \'" + key_id + "\';"

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
        json_str += "\"key_id\":" + "\"" + v[0] + "\""
        json_str += ",\"key_material\":" + "\"" + v[1] + "\""
        json_str += ",\"key_iv\":" + "\"" + v[2] + "\""
        json_str += ",\"key_activeyn\":" + "\"" + v[3] + "\""

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
    value_list = df.values.tolist()
    if len(value_list) == 0:
        return None

    json_str = ""
    for v in value_list:
        json_str += "{"
        json_str += "\"id\":" + "\"" + v[0] + "\""
        json_str += ",\"policy_name\":" + "\"" + v[1] + "\""
        json_str += ",\"policy_type\":" + "\"" + v[2] + "\""
        json_str += ",\"description\":" + "\"" + v[3] + "\""
        json_str += ",\"algorithm\":" + "\"" + v[4] + "\""
        json_str += ",\"key_length\":" + "\"" + str(int(v[5])) + "\""
        json_str += ",\"share_range\":" + "\"" + v[6] + "\""
        json_str += ",\"back_migration\":" + "\"" + str(int(v[7])) + "\""
        json_str += ",\"create_date\":" + "\"" + str(int(v[8])) + "\""
        json_str += ",\"modified_date\":" + "\"" + str(int(v[9])) + "\""
        json_str += ",\"creator\":" + "\"" + v[10] + "\""

        break
    json_str += "}"

    json_object = json.loads(json_str)

    json_formatted_str = json.dumps(json_object, indent=2)

    return json_formatted_str

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

                if agent_type.startswith('api_policy'):
                    json_str = select_api_policy(key)
                elif agent_type.startswith('la_policy'):
                    json_str = select_la_policy(key, subkey)
                elif agent_type.startswith('sa_policy'):
                    json_str = select_sa_policy(key, subkey)
                elif agent_type.startswith('ra_policy'):
                    print('ra_policy, key=' + key)
                    json_str = select_ra_policy(key)
                elif agent_type.startswith('key_material'):
                    json_str = select_key_material(key)
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
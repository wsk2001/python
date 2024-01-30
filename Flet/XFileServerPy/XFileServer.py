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

    for key, val in json_dict.items():
        if "policytype" == str(key).lower():
            policy_type = val
        elif "key" == str(key).lower():
            key_val = val
        else:
            continue

    return policy_type, key_val


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
    if ip is None:
        return None

    if policy is not None:
        if len(policy) <= 0:
            policy = None

    if policy is not None:
        query = \
            "select * from la_policy where ip = \'" + ip + "\' and policy = \'" + policy + "\';"
    else:
        query = \
            "select * from la_policy where ip = \'" + ip + "\';"

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


def select_sa_policy(ip, policy=None):
    query = None

    if ip is None:
        return None

    if policy is not None:
        if len(policy) <= 0:
            policy = None

    if policy is not None:
        print('ip: ' + ip + ', policy: [' + policy + ']')
        query = \
            "select * from sa_policy where ip = \'" + ip + "\' and policy = \'" + policy + "\';"
    else:
        query = \
            "select * from sa_policy where ip = \'" + ip + "\';"

    print("query: " + query)

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


def select_encpolicy(enc_id: str):
    if enc_id is None:
        return None

    query = \
        "select id, policy_name, policy_type, description, algorithm, key_length, share_range, back_migration, " \
        "create_date, modified_date, creator from enc_policy " \
        "where id = \'" + enc_id + "\';"

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


def get_ra_policy(ip):
    json_str = ""
    df = select_client(ip)
    vlist = df.values.tolist()

    key_id = ''
    json_tmp = ''
    for v in vlist:
        key_id = v[0]
        json_tmp = "\"client\": {"
        json_tmp += "\"client_id\":" + "\"" + v[0] + "\""
        json_tmp += ",\"client_name\":" + "\"" + v[1] + "\""  # endpoint id
        json_tmp += ",\"mac_addr\":" + "\"" + v[2] + "\""
        json_tmp += ",\"description\":" + "\"" + v[3] + "\""
        json_tmp += ",\"create_date\":" + "\"" + str(int(v[4])) + "\""
        json_tmp += ",\"creator\":" + "\"" + v[5] + "\""
        json_tmp += ",\"client_status\":" + "\"" + v[6] + "\""
        json_tmp += ",\"client_platform\":" + "\"" + v[7] + "\""
        json_tmp += ",\"platformver\":" + "\"" + v[8] + "\""
        json_tmp += "}"
        break

    json_str = json_tmp

    df = select_agent_policy(key_id)
    vlist = df.values.tolist()
    ap_id = ''
    for v in vlist:
        json_tmp = ",\"agent_policy\": {"
        json_tmp += "\"ag_id\":" + "\"" + v[0] + "\""
        json_tmp += ",\"agent_type\":" + "\"" + v[1] + "\""
        json_tmp += ",\"protocol\":" + "\"" + v[2] + "\""
        json_tmp += ",\"sync_period\":" + "\"" + str(int(v[3])) + "\""
        json_tmp += ",\"log_period\":" + "\"" + str(int(v[4])) + "\""
        json_tmp += ",\"creator\":" + "\"" + v[5] + "\""
        json_tmp += ",\"create_date\":" + "\"" + str(int(v[6])) + "\""
        json_tmp += ",\"modified_date\":" + "\"" + str(int(v[7])) + "\""
        json_tmp += ",\"p_clientid\":" + "\"" + v[8] + "\""
        json_tmp += ",\"p_encid\":" + "\"" + v[9] + "\""
        json_tmp += ",\"policy_status\":" + "\"" + v[10] + "\""
        json_tmp += ",\"description\":" + "\"" + v[11] + "\""
        json_tmp += "}"
        key_id = v[9]
        ap_id = v[0]
        break

    json_str += "\n" + json_tmp

    df = select_encpolicy(key_id)
    vlist = df.values.tolist()
    for v in vlist:
        json_tmp = ",\"enc_policy\": {"
        json_tmp += "\"enc_id\":" + "\"" + v[0] + "\""
        json_tmp += ",\"policy_name\":" + "\"" + v[1] + "\""
        json_tmp += ",\"policy_type\":" + "\"" + v[2] + "\""
        json_tmp += ",\"description\":" + "\"" + v[3] + "\""
        json_tmp += ",\"algorithm\":" + "\"" + v[4] + "\""
        json_tmp += ",\"key_length\":" + "\"" + str(int(v[5])) + "\""
        json_tmp += ",\"share_range\":" + "\"" + v[6] + "\""
        json_tmp += ",\"back_migration\":" + "\"" + str(int(v[7])) + "\""
        json_tmp += ",\"create_date\":" + "\"" + str(int(v[8])) + "\""
        json_tmp += ",\"modified_date\":" + "\"" + str(int(v[9])) + "\""
        json_tmp += ",\"creator\":" + "\"" + v[10] + "\""
        json_tmp += "}"
        key_id = v[0]
        break

    json_str += "\n" + json_tmp

    df = select_target_path(ap_id)
    vlist = df.values.tolist()
    fst_flag = True
    json_tmp = ''
    tp_id_list = []
    tp_id_list.clear()
    for v in vlist:
        if fst_flag is True:
            json_tmp = ",\"target_path\": [\n"
            json_tmp += "{"
            fst_flag = False
        else:
            json_tmp += ",{"

        tp_id_list.append(v[0])
        json_tmp += "\"tp_id\":" + "\"" + v[0] + "\""
        json_tmp += ",\"tp_path\":" + "\"" + v[1] + "\""
        json_tmp += ",\"tp_mode\":" + "\"" + (v[2] if v[2] is not None else '') + "\""
        json_tmp += ",\"exclude_exts\":" + "\"" + (v[3] if v[3] is not None else '') + "\""
        json_tmp += ",\"tp_uid\":" + "\"" + (str(int(v[4])) if v[4] is not None else '') + "\""
        json_tmp += ",\"tp_gid\":" + "\"" + (str(int(v[5])) if v[5] is not None else '') + "\""
        json_tmp += ",\"p_ag_id\":" + "\"" + v[6] + "\""
        json_tmp += "}"

    if 0 < len(json_tmp):
        json_tmp += "]"
        json_str += "\n" + json_tmp

    if 0 < len(tp_id_list):
        tp_id_str = ''
        fst_flag = True
        for tp_id in tp_id_list:
            if fst_flag is True:
                tp_id_str = "\"" + tp_id + "\""
                fst_flag = False
            else:
                tp_id_str += ",\"" + tp_id + "\""

        df = select_access_control(tp_id_str)
        vlist = df.values.tolist()
        fst_flag = True
        acl_id_list = []
        acl_id_list.clear()
        for v in vlist:
            if fst_flag is True:
                json_tmp = ",\"access_control\": [\n"
                json_tmp += "{"
                fst_flag = False
            else:
                json_tmp += ",{"
            acl_id_list.append(v[0])
            json_tmp += "\"ac_id\":" + "\"" + v[0] + "\""
            json_tmp += ",\"access_ip\":" + "\"" + (v[1] if v[1] is not None else '') + "\""
            json_tmp += ",\"access_sip\":" + "\"" + (v[2] if v[2] is not None else '') + "\""
            json_tmp += ",\"access_eip\":" + "\"" + (v[3] if v[3] is not None else '') + "\""
            json_tmp += ",\"access_uid\":" + "\"" + (str(int(v[4])) if v[4] is not None else '') + "\""
            json_tmp += ",\"access_gid\":" + "\"" + (str(int(v[5])) if v[5] is not None else '') + "\""
            json_tmp += ",\"access_account\":" + "\"" + (v[6] if v[6] is not None else '') + "\""
            json_tmp += ",\"access_passwd\":" + "\"" + (v[7] if v[7] is not None else '') + "\""
            json_tmp += ",\"access_process\":" + "\"" + (v[8] if v[8] is not None else '') + "\""
            json_tmp += ",\"p_tp_id\":" + "\"" + v[9] + "\""
            json_tmp += ",\"access_mac\":" + "\"" + (v[10] if v[10] is not None else '') + "\""
            json_tmp += ",\"access_type\":" + "\"" + (v[11] if v[11] is not None else '') + "\""
            json_tmp += "}"

    if 0 < len(json_tmp):
        json_tmp += "]"
        json_str += "\n" + json_tmp

    if 0 < len(tp_id_list):
        tp_id_str = ''
        fst_flag = True
        for tp_id in tp_id_list:
            if fst_flag is True:
                tp_id_str = "\"" + tp_id + "\""
                fst_flag = False
            else:
                tp_id_str += ",\"" + tp_id + "\""

        df = select_permission(tp_id_str)
        vlist = df.values.tolist()
        fst_flag = True
        for v in vlist:
            if fst_flag is True:
                json_tmp = ",\"common_permission\": [\n"
                json_tmp += "{"
                fst_flag = False
            else:
                json_tmp += ",{"
            json_tmp += "\"cp_id\":" + "\"" + v[0] + "\""
            json_tmp += ",\"read_chk\":" + "\"" + (v[1] if v[1] is not None else '') + "\""
            json_tmp += ",\"write_chk\":" + "\"" + (v[2] if v[2] is not None else '') + "\""
            json_tmp += ",\"excute_chk\":" + "\"" + (v[3] if v[3] is not None else '') + "\""
            json_tmp += ",\"perm_type\":" + "\"" + (v[4] if v[4] is not None else '') + "\""
            json_tmp += ",\"p_tp_id\":" + "\"" + v[5] + "\""
            json_tmp += "}"
    if 0 < len(json_tmp):
        json_tmp += "]"
        json_str += "\n" + json_tmp

    if 0 < len(acl_id_list):
        acl_id_str = ''
        fst_flag = True
        for acl_id in acl_id_list:
            if fst_flag is True:
                acl_id_str = "\"" + acl_id + "\""
                fst_flag = False
            else:
                acl_id_str += ",\"" + acl_id + "\""

        df = select_permission(acl_id_str)
        vlist = df.values.tolist()
        fst_flag = True
        for v in vlist:
            if fst_flag is True:
                json_tmp = ",\"acl_permission\": [\n"
                json_tmp += "{"
                fst_flag = False
            else:
                json_tmp += ",{"
            json_tmp += "\"ap_id\":" + "\"" + v[0] + "\""
            json_tmp += ",\"read_chk\":" + "\"" + (v[1] if v[1] is not None else '') + "\""
            json_tmp += ",\"write_chk\":" + "\"" + (v[2] if v[2] is not None else '') + "\""
            json_tmp += ",\"excute_chk\":" + "\"" + (v[3] if v[3] is not None else '') + "\""
            json_tmp += ",\"perm_type\":" + "\"" + (v[4] if v[4] is not None else '') + "\""
            json_tmp += ",\"p_ac_id\":" + "\"" + v[5] + "\""
            json_tmp += "}"
    if 0 < len(json_tmp):
        json_tmp += "]"
        json_str += "\n" + json_tmp

    json_str = '{\n' + json_str + '\n}'

    json_object = json.loads(json_str)

    json_formatted_str = json.dumps(json_object, indent=2)

    print()
    print(json_formatted_str)
    print()

    return json_formatted_str


# Code that runs in a thread.
def threaded(client_socket, addr):
    client_ipaddr = addr[0]
    client_port = addr[1]
    print('Connected by :', client_ipaddr, ':', client_port)

    # Repeat until the client disconnects.
    while True:

        try:
            # 데이터 수신
            data = client_socket.recv(1024)

            if not data:
                print('Disconnected by ' + client_ipaddr, ':', client_port)
                break

            else:
                rcv_data = data.decode()
                agent_type, key = parse_json(rcv_data)

                print('receive data: ' + rcv_data)
                print('******************************************')
                if agent_type:
                    print('agent_type: ' + agent_type)
                if key:
                    print('key       : ' + key)
                # test key 를 무조건 배포
                client_ipaddr = "192.168.60.190"
                print('******************************************')

                if agent_type.startswith('api_policy'):
                    json_str = select_api_policy(client_ipaddr)
                elif agent_type.startswith('la_policy'):
                    json_str = select_la_policy(client_ipaddr, key)
                elif agent_type.startswith('sa_policy'):
                    json_str = select_sa_policy(client_ipaddr, key)
                elif agent_type.startswith('ra_policy'):
                    json_str = get_ra_policy(client_ipaddr)
                elif agent_type.startswith('key_material'):
                    json_str = select_key_material(client_ipaddr)
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
            print('Disconnected by ' + client_ipaddr, ':', client_port)
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
실행 방법: py XFileServer
'''

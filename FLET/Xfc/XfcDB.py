# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd


class XfcDB:
    def __init__(self):
        self.database_name = './dbms/xfc_policy.db'

    def create_api_policy_table(self):
        conn = sqlite3.connect(self.database_name)
        conn.execute(
            'CREATE TABLE IF NOT EXISTS api_policy(id TEXT, remark TEXT, createTime TEXT, updateTime TEXT, ' +
            'platform TEXT, providerName TEXT, process TEXT, ipAddr TEXT, macAddr TEXT, modifiedDate TEXT, ' +
            'domainKeyId TEXT, domainAlgorithm TEXT, domainKeyLength TEXT, modulus TEXT, publicExponent TEXT, ' +
            'privateExponent TEXT, domainCode TEXT, attributeKeyId TEXT, attributeIv TEXT, attributeAlgorithm TEXT, ' +
            'attributeKeyLength TEXT, attributeChiperMode TEXT, attributePaddingMethod TEXT, ' +
            'attributeKeyMaterial TEXT, contentsAlgorithm TEXT, contentsKeyLength TEXT, readChk TEXT, writeChk TEXT, ' +
            'excuteChk TEXT, syncPeriod TEXT, logPeriod TEXT, excludeExts TEXT, decFileSize TEXT, encErrorCode TEXT, ' +
            'decErrorCode TEXT )'
        )
        conn.close()

    def create_la_policy_table(self):
        conn = sqlite3.connect(self.database_name)
        conn.execute('CREATE TABLE IF NOT EXISTS la_policy( ' +
                     'ip TEXT, ' +
                     'policy TEXT, ' +
                     'description TEXT, ' +
                     'base_path TEXT, ' +
                     'dir TEXT, ' +
                     'mode TEXT, ' +
                     'time_limit TEXT, ' +
                     'check_file_closed TEXT, ' +
                     'use_file_filter TEXT, ' +
                     'file_filter_type TEXT, ' +
                     'file_filter_exts TEXT, ' +
                     'check_cycle TEXT, ' +
                     'thread_count TEXT, ' +
                     'use_backup TEXT, ' +
                     'backup_path TEXT, ' +
                     'temp_path TEXT, ' +
                     'dir_depth TEXT, ' +
                     'dir_format TEXT, ' +
                     'ymd_offset TEXT, ' +
                     'use_trigger_file TEXT, ' +
                     'trigger_ext TEXT, ' +
                     'trigger_target  TEXT )'
                     )
        conn.close()

    def create_sa_policy_table(self):
        conn = sqlite3.connect(self.database_name)
        conn.execute('CREATE TABLE IF NOT EXISTS sa_policy( ' +
                     'ip TEXT, ' +
                     'policy TEXT, ' +
                     'description TEXT, ' +
                     'file_path TEXT, ' +
                     'mode TEXT, ' +
                     'time_limit TEXT, ' +
                     'repeat TEXT, ' +
                     'dir_format TEXT, ' +
                     'ymd_offset TEXT, ' +
                     'dir_depth TEXT, ' +
                     'use_weekday TEXT, ' +
                     'weekdays TEXT, ' +
                     'day TEXT, ' +
                     'hh TEXT, ' +
                     'mm TEXT, ' +
                     'ss TEXT, ' +
                     'use_file_filter TEXT, ' +
                     'file_filter_type TEXT, ' +
                     'file_filter_exts TEXT, ' +
                     'check_file_closed TEXT, ' +
                     'thread_count TEXT, ' +
                     'use_backup TEXT, ' +
                     'backup_path TEXT, ' +
                     'temp_path TEXT, ' +
                     'check_cycle TEXT )'
                     )
        conn.close()

    def get_api_policy_list(self, key_id=None):
        query = ""
        if key_id is None:
            query = \
                "select id, ipAddr, Remark, createTime, updateTime, platform, domainKeyId from api_policy order by id;"
        else:
            query = \
                "select id, ipAddr, Remark, createTime, updateTime, platform, domainKeyId from api_policy " \
                "where id like '%" + key_id + "%' order by id;"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df

    def get_api_policy(self, api, api_id):
        query = \
            "select * from api_policy where id = \'" + api_id + "\';"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()
        value_list = df.values.tolist()

        for v in value_list:
            api.id.value = v[0]
            api.remark.value = v[1]
            api.createTime.value = v[2]
            api.updateTime.value = v[3]
            api.platform.value = v[4]
            api.providerName.value = v[5]
            api.process.value = v[6]
            api.ipAddr.value = v[7]
            api.macAddr.value = v[8]
            api.modifiedDate.value = v[9]
            api.domainKeyId.value = v[10]
            api.domainAlgorithm.value = v[11]
            api.domainKeyLength.value = v[12]
            api.modulus.value = v[13]
            api.publicExponent.value = v[14]
            api.privateExponent.value = v[15]
            api.domainCode.value = v[16]
            api.attributeKeyId.value = v[17]
            api.attributeIv.value = v[18]
            api.attributeAlgorithm.value = v[19]
            api.attributeKeyLength.value = v[20]
            api.attributeChiperMode.value = v[21]
            api.attributePaddingMethod.value = v[22]
            api.attributeKeyMaterial.value = v[23]
            api.contentsAlgorithm.value = v[24]
            api.contentsKeyLength.value = v[25]
            api.readChk.value = v[26]
            api.writeChk.value = v[27]
            api.excuteChk.value = v[28]
            api.syncPeriod.value = v[29]
            api.logPeriod.value = v[30]
            api.excludeExts.value = v[31]
            api.decFileSize.value = v[32]
            api.encErrorCode.value = v[33]
            api.decErrorCode.value = v[34]
            break

    def delete_api_policy(self, ipaddr: str):
        conn = sqlite3.connect(self.database_name)
        conn.execute('delete from api_policy where id = ' + '\'' + ipaddr + '\';')
        conn.commit()
        conn.close()

    def delete_la_policy(self, ip: str, policy: str):
        conn = sqlite3.connect(self.database_name)
        conn.execute('delete from la_policy where ip = ' + '\'' + ip + '\' and policy = ' + '\'' + policy + '\';')
        conn.commit()
        conn.close()

    def delete_sa_policy(self, ip: str, policy: str):
        conn = sqlite3.connect(self.database_name)
        conn.execute('delete from sa_policy where ip = ' + '\'' + ip + '\' and policy = ' + '\'' + policy + '\';')
        conn.commit()
        conn.close()

    def insert_api_policy(self, c):
        self.delete_api_policy(c.id.value)
        conn = sqlite3.connect(self.database_name)
        conn.execute(
            "INSERT INTO api_policy VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
            (c.id.value,
             c.remark.value,
             c.createTime.value,
             c.updateTime.value,
             c.platform.value,
             c.providerName.value,
             c.process.value,
             c.ipAddr.value,
             c.macAddr.value,
             str(c.modifiedDate.value),
             c.domainKeyId.value,
             c.domainAlgorithm.value,
             str(c.domainKeyLength.value),
             str(c.modulus.value),
             str(c.publicExponent.value),
             str(c.privateExponent.value),
             c.domainCode.value,
             c.attributeKeyId.value,
             c.attributeIv.value,
             c.attributeAlgorithm.value,
             str(c.attributeKeyLength.value),
             c.attributeChiperMode.value,
             c.attributePaddingMethod.value,
             c.attributeKeyMaterial.value,
             c.contentsAlgorithm.value,
             str(c.contentsKeyLength.value),
             c.readChk.value,
             c.writeChk.value,
             c.excuteChk.value,
             str(c.syncPeriod.value),
             str(c.logPeriod.value),
             c.excludeExts.value,
             str(c.decFileSize.value),
             c.encErrorCode.value,
             c.decErrorCode.value)
        )
        conn.commit()
        conn.close()

    def insert_la_policy(self, c):
        self.delete_la_policy(c.ip.value, c.policy.value)
        conn = sqlite3.connect(self.database_name)
        conn.execute("INSERT INTO la_policy VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                     (
                         c.ip.value,
                         c.policy.value,
                         c.description.value,
                         c.base_path.value,
                         c.dir.value,
                         c.mode.value,
                         c.time_limit.value,
                         'Y' if c.check_file_closed.value is True else 'N',
                         'Y' if c.use_file_filter.value is True else 'N',
                         c.file_filter_type.value[0:1],
                         c.file_filter_exts.value,
                         c.check_cycle.value,
                         c.thread_count.value,
                         'Y' if c.use_backup.value is True else 'N',
                         c.backup_path.value,
                         c.temp_path.value,
                         c.dir_depth.value,
                         c.dir_format.value,
                         c.ymd_offset.value,
                         'Y' if c.use_trigger_file.value is True else 'N',
                         c.trigger_ext.value,
                         c.trigger_target.value )
                     )

        conn.commit()
        conn.close()

    def insert_sa_policy(self, c):
        self.delete_sa_policy(c.ip.value, c.policy.value)
        conn = sqlite3.connect(self.database_name)

        wday_list = []
        wday_list.clear()

        # dict, list, map 등을 이용하여 간단하게 처리 할 수 있도록 수정 필요.
        if c.mon.value is True:
            wday_list.append('1')

        if c.tue.value is True:
            wday_list.append('2')

        if c.wed.value is True:
            wday_list.append('3')

        if c.thu.value is True:
            wday_list.append('4')

        if c.fri.value is True:
            wday_list.append('5')

        if c.sat.value is True:
            wday_list.append('6')

        if c.sun.value is True:
            wday_list.append('7')

        c.weekdays.value = ""
        for v in wday_list:
            if 0 < len(c.weekdays.value):
                c.weekdays.value = c.weekdays.value + ', ' + v
            else:
                c.weekdays.value = v

        conn.execute("INSERT INTO sa_policy VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                     (
                         c.ip.value,
                         c.policy.value,
                         c.description.value,
                         c.file_path.value,
                         c.mode.value,
                         c.time_limit.value,
                         'Y' if c.repeat.value is True else 'N',
                         c.dir_format.value,
                         c.ymd_offset.value,
                         c.dir_depth.value,
                         'Y' if c.use_weekday.value is True else 'N',
                         c.weekdays.value,
                         c.day.value,
                         c.hh.value,
                         c.mm.value,
                         c.ss.value,
                         'Y' if c.use_file_filter.value is True else 'N',
                         c.file_filter_type.value[0:1],
                         c.file_filter_exts.value,
                         'Y' if c.check_file_closed.value is True else 'N',
                         c.thread_count.value,
                         'Y' if c.use_backup.value is True else 'N',
                         c.backup_path.value,
                         c.temp_path.value,
                         c.check_cycle.value)
                     )

        conn.commit()
        conn.close()

    def get_la_policy_list(self, ip=None, policy=None):
        query = ""
        if ip is None:
            query = \
                "select ip, policy, description, base_path, dir, mode, temp_path " \
                "from la_policy order by ip, policy;"
        elif ip is not None and policy is not None:
            query = \
                "select ip, policy, description, base_path, dir, mode, temp_path from la_policy " \
                "where ip = '" + ip + "' and policy = '" + policy + "' order by ip, policy;"
        elif ip is not None:
            query = \
                "select ip, policy, description, base_path, dir, mode, temp_path from la_policy " \
                "where ip = '" + ip + "' order by ip, policy;"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df

    def get_sa_policy_list(self, ip=None, policy=None):
        query = ""
        if ip is None:
            query = \
                "select ip, policy, description, file_path, mode, repeat, day, hh, mm, ss " \
                "from sa_policy order by ip, policy;"
        elif ip is not None and policy is not None:
            query = \
                "select ip, policy, description, file_path, mode, repeat, day, hh, mm, ss from sa_policy " \
                "where ip = '" + ip + "' and policy = '" + policy + "' order by ip, policy;"
        elif ip is not None:
            query = \
                "select ip, policy, description, file_path, mode, repeat, day, hh, mm, ss from sa_policy " \
                "where ip = '" + ip + "' order by ip, policy;"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df

    def get_la_policy(self, la, ip=None, policy=None):
        query = ""

        if ip is None:
            query = \
                "select * from la_policy;"
        elif policy is None:
            query = \
                "select * from la_policy where ip = \'" + ip + "\';"
        else:
            query = \
                "select * from la_policy where ip = \'" + ip + "\' and policy = \'" + policy + "\';"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        value_list = df.values.tolist()

        for v in value_list:
            la.ip.value = v[0]
            la.policy.value = v[1]
            la.description.value = v[2]
            la.base_path.value = v[3]
            la.dir.value = v[4]
            la.mode.value = v[5]  # "E"
            la.time_limit.value = v[6]
            la.check_file_closed.value = True if v[7] == 'Y' else False
            la.use_file_filter.value = True if v[8] == 'Y' else False
            la.file_filter_type.value = 'I (필터 타입 포함)' if v[9][0] == 'I' else 'E (필터 타입 제외)'
            la.file_filter_exts.value = v[10]
            la.check_cycle.value = v[11]
            la.thread_count.value = v[12]
            la.use_backup.value = True if v[13] == 'Y' else False
            la.backup_path.value = v[14]
            la.temp_path.value = v[15]
            la.dir_depth.value = v[16]
            la.dir_format.value = v[17]
            la.ymd_offset.value = v[18]
            la.use_trigger_file.value = True if v[19] == 'Y' else False
            la.trigger_ext.value = v[20]
            la.trigger_target.value = v[21]

            if la.use_file_filter.value is True:
                la.file_filter_type.visible = True
                la.file_filter_exts.visible = True
            else:
                la.file_filter_type.visible = False
                la.file_filter_exts.visible = False

            if la.use_backup.value is True:
                la.backup_path.visible = True
            else:
                la.backup_path.visible = True

            if la.use_trigger_file.value is True:
                la.trigger_ext.visible = True
                la.trigger_target.visible = True
            else:
                la.trigger_ext.visible = False
                la.trigger_target.visible = False

            break

    def get_sa_policy(self, sa, ip=None, policy=None):
        query = ""

        if ip is None:
            query = \
                "select * from sa_policy;"
        elif policy is None:
            query = \
                "select * from sa_policy where ip = \'" + ip + "\';"
        else:
            query = \
                "select * from sa_policy where ip = \'" + ip + "\' and policy = \'" + policy + "\';"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        value_list = df.values.tolist()

        for v in value_list:
            sa.ip.value = v[0]
            sa.policy.value = v[1]

            sa.description.value = v[2]
            sa.file_path.value = v[3]
            sa.mode.value = v[4]
            sa.time_limit.value = v[5]
            sa.repeat.value = True if v[6] == 'Y' else False
            sa.dir_format.value = v[7]
            sa.ymd_offset.value = v[8]
            sa.dir_depth.value = v[9]
            sa.use_weekday.value = True if v[10] == 'Y' else False
            sa.weekdays.value = v[11]
            sa.day.value = v[12]
            sa.hh.value = v[13]
            sa.mm.value = v[14]
            sa.ss.value = v[15]
            sa.use_file_filter.value = True if v[16] == 'Y' else False
            sa.file_filter_type.value = v[17]
            sa.file_filter_exts.value = v[18]
            sa.check_file_closed.value = True if v[19] == 'Y' else False
            sa.thread_count.value = v[20]
            sa.use_backup.value = True if v[21] == 'Y' else False
            sa.backup_path.value = v[22]
            sa.temp_path.value = v[23]
            sa.check_cycle.value = v[24]

            if sa.use_file_filter.value:
                sa.file_filter_type.visible = True
                sa.file_filter_exts.visible = True
            else:
                sa.file_filter_type.visible = False
                sa.file_filter_exts.visible = False

            if sa.use_backup.value:
                sa.backup_path.visible = True
            else:
                sa.backup_path.visible = False

            break

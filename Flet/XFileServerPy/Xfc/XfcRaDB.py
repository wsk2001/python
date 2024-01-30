# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd

class XfcRaDB:
    def __init__(self):
        self.database_name = './dbms/xfc_policy.db'

    def create_ra_policy(self):
        conn = sqlite3.connect(self.database_name)
        conn.execute(
            'CREATE TABLE IF NOT EXISTS ra_policy(id TEXT, agent_type TEXT, share_protocol TEXT, endpoint TEXT, ' +
            'encpolicy TEXT, policyPollingPeriod INTEGER, logSendPollingPeriod INTEGER, targetPath TEXT, ' +
            'description TEXT )'
        )
        conn.close()

    def create_ra_acls(self):
        conn = sqlite3.connect(self.database_name)
        conn.execute(
            'CREATE TABLE IF NOT EXISTS ra_acls(id TEXT, ra_id TEXT, path TEXT, exclude_exts TEXT, ' +
            'base_enc TEXT, base_decT EXT )'
        )
        conn.close()

    def create_ra_detail_acls(self):
        conn = sqlite3.connect(self.database_name)
        conn.execute(
            'CREATE TABLE IF NOT EXISTS ra_detail_acls(id TEXT, ra_acls_id TEXT, ip TEXT, start_ip TEXT, ' +
            'end_ip TEXT, uid TEXT, gid TEXT, enc TEXT, dec TEXT )'
        )
        conn.close()

    def insert_ra_policy(self, v1, v2, v3, v4, v5, v6, v7, v8, v9):
        self.delete_ra_policy(v1)
        conn = sqlite3.connect(self.database_name)
        conn.execute("INSERT INTO ra_policy VALUES(?,?,?,?,?,?,?,?,?);",
                     (v1, v2, v3, v4, v5, v6, v7, v8, v9)
                     )

        conn.commit()
        conn.close()

    def delete_ra_policy(self, id):
        conn = sqlite3.connect(self.database_name)
        conn.execute('delete from ra_policy where id = ' + '\'' + id + '\';')
        conn.commit()
        conn.close()

    def list_ra_policy(self, id=None):
        query = ""
        if id is None:
            query = \
                "select id, agent_type, share_protocol, endpoint, encpolicy, policyPollingPeriod, " \
                "logSendPollingPeriod, targetPath, description from ra_policy order by id;"
        else:
            query = \
                "select id, agent_type, share_protocol, endpoint, encpolicy, policyPollingPeriod, " \
                "logSendPollingPeriod, targetPath, description from ra_policy " \
                "where id like '%" + id + "%' order by id;"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df

    def insert_ra_acl(self, v1, v2, v3, v4, v5, v6):
        self.delete_ra_acl(v1)
        conn = sqlite3.connect(self.database_name)
        conn.execute("INSERT INTO ra_acls VALUES(?,?,?,?,?,?);",
                     (v1, v2, v3, v4, v5, v6)
                     )

        conn.commit()
        conn.close()

    def delete_ra_acl(self,id=None):
        conn = sqlite3.connect(self.database_name)
        conn.execute('delete from ra_acls where id = ' + '\'' + id + '\';')
        conn.commit()
        conn.close()

    def list_ra_acl(self, id=None):
        query = ""
        if id is None:
            query = \
                "select id, ra_id, path, exclude_exts, base_enc, base_dec from ra_acls order by id;"
        else:
            query = \
                "select id, ra_id, path, exclude_exts, base_enc, base_dec from ra_acls " \
                "where id like '%" + id + "%' order by id;"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df

    def insert_ra_detail_acl(self, v1, v2, v3, v4, v5, v6, v7, v8, v9):
        self.delete_ra_detail_acl(v1)
        conn = sqlite3.connect(self.database_name)
        conn.execute("INSERT INTO ra_detail_acls VALUES(?,?,?,?,?,?,?,?,?);",
                     (v1, v2, v3, v4, v5, v6, v7, v8, v9)
                     )

        conn.commit()
        conn.close()

    def delete_ra_detail_acl(self, id):
        conn = sqlite3.connect(self.database_name)
        conn.execute('delete from ra_detail_acls where id = ' + '\'' + id + '\';')
        conn.commit()
        conn.close()

    def list_ra_detail_acl(self, id=None):
        query = ""
        if id is None:
            query = \
                "select id, ra_acls_id, ip, start_ip, end_ip, uid, gid, enc, dec from ra_detail_acls order by id;"
        else:
            query = \
                "select id, ra_acls_id, ip, start_ip, end_ip, uid, gid, enc, dec from ra_detail_acls " \
                "where id like '%" + id + "%' order by id;"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df

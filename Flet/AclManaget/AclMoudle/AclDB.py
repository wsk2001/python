# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd


class AclDB:
    def __init__(self):
        self.database_name = './dbms/xdb_acl.db3'

    def create_watch_path_table(self):
        conn = sqlite3.connect(self.database_name)
        conn.execute(
            'CREATE TABLE IF NOT EXISTS watch_path( ' + 
            'seq INTEGER PRIMARY KEY AUTOINCREMENT, ' + 
            'ip TEXT NOT NULL, ' + 
            'watch_path TEXT NOT NULL, ' +
            'ad TEXT NOT NULL, ' + 
            'save_log TEXT, ' + 
            'allow_start TEXT, ' + 
            'allow_end TEXT )'
        )
        conn.close()


    def create_access_control_table(self):
        conn = sqlite3.connect(self.database_name)
        conn.execute('CREATE TABLE IF NOT EXISTS access_control( ' +
                     'seq INTEGER PRIMARY KEY AUTOINCREMENT, ' + 
                     'ip TEXT NOT NULL, ' +
                     'watch_path TEXT NOT NULL, ' +
                     'ad TEXT NOT NULL, ' +
                     'owner TEXT, ' +
                     'app TEXT, ' +
                     'save_log TEXT, ' +
                     'allow_start TEXT, ' +
                     'allow_end  TEXT )'
                     )
        conn.close()


    def watch_path_list(self, ip=None, watch_path=None):
        query = ""
        if ip is None and watch_path is None:
            query = \
                "select seq, ip, watch_path, ad, save_log, allow_start, allow_end from watch_path;"
        elif ip is None:
            query = \
                "select seq, ip, watch_path, ad, save_log, allow_start, allow_end from watch_path " \
                "where watch_path = '" + watch_path + "';"
        elif watch_path is None:
            query = \
                "select seq, ip, watch_path, ad, save_log, allow_start, allow_end from watch_path " \
                "where ip = '" + ip + "';"
        else:
            query = \
                "select seq, ip, watch_path, ad, save_log, allow_start, allow_end from watch_path " \
                "where ip = '" + ip + "' and watch_path = '" + watch_path + "';"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df


    def access_control_list(self, ip=None, watch_path=None):
        query = ""
        if ip is None and watch_path is None:
            query = \
                "select seq, ip, watch_path, ad, owner, app, save_log, allow_start, allow_end from access_control;"
        elif ip is None:
            query = \
                "select seq, ip, watch_path, ad, owner, app, save_log, allow_start, allow_end from access_control " \
                "where watch_path = '" + watch_path + "';"
        elif watch_path is None:
            query = \
                "select seq, ip, watch_path, ad, owner, app, save_log, allow_start, allow_end from access_control " \
                "where ip = '" + ip + "';"
        else:
            query = \
                "select seq, ip, watch_path, ad, owner, app, save_log, allow_start, allow_end from access_control " \
                "where ip = '" + ip + "' and watch_path = '" + watch_path + "';"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df


    def get_watch_path(self, seq):
        if seq is None:
            return None
        
        query = \
            "select seq, ip, watch_path, ad, save_log, allow_start, allow_end from watch_path " \
            "where seq = " + seq + ";"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df

    def get_access_control(self, seq):
        if seq is None:
            return None
        
        query = \
            "select seq, ip, watch_path, ad, owner, app, save_log, allow_start, allow_end from access_control " \
            "where seq = " + seq + ";"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df


    def delete_watch_path(self, seq):
        if seq is None:
            return
        
        conn = sqlite3.connect(self.database_name)
        conn.execute('delete from watch_path where seq = ' + seq + ';')
        conn.commit()
        conn.close()

    def delete_access_control(self, seq):
        if seq is None:
            return
        
        conn = sqlite3.connect(self.database_name)
        conn.execute('delete from access_control where seq = ' + seq + ';')
        conn.commit()
        conn.close()

    def create_watch_path(self, ip, watch_path, ad, save_log, allow_start, allow_end):
        conn = sqlite3.connect(self.database_name)

        sql = """
            INSERT INTO watch_path (ip, watch_path, ad, save_log, allow_start, allow_end)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        values = (ip, watch_path, ad, save_log, allow_start, allow_end)
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        conn.close()


    def create_access_control(self, ip, watch_path, ad, owner, app, save_log, allow_start, allow_end):
        conn = sqlite3.connect(self.database_name)

        sql = """
            INSERT INTO access_control (ip, watch_path, ad, owner, app, save_log, allow_start, allow_end)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        values = (ip, watch_path, ad, owner, app, save_log, allow_start, allow_end)
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
    
    
    def update_watch_path(self, seq, ip, watch_path, ad, save_log, allow_start, allow_end):
        conn = sqlite3.connect(self.database_name)
        sql = """
            UPDATE watch_path
            SET
            ip=?,
            watch_path=?,
            ad=?,
            save_log=?,
            allow_start=?,
            allow_end=?
            WHERE seq=?
        """

        values = []
        values.append(ip)
        values.append(watch_path)
        values.append(ad)
        values.append(save_log)
        values.append(allow_start)
        values.append(allow_end)
        values.append(seq)

        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()

        return cursor.rowcount == 1    

    def update_access_control(self, seq, ip, watch_path, ad, owner, app, save_log, allow_start, allow_end):
        conn = sqlite3.connect(self.database_name)
        sql = """
            UPDATE access_control
            SET
            ip=?,
            watch_path=?,
            ad=?,
            owner=?,
            app=?,
            save_log=?,
            allow_start=?,
            allow_end=?
            WHERE seq=?
        """

        values = []
        values.append(ip)
        values.append(watch_path)
        values.append(ad)
        values.append(owner)
        values.append(app)
        values.append(save_log)
        values.append(allow_start)
        values.append(allow_end)
        values.append(seq)

        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()

        return cursor.rowcount == 1    

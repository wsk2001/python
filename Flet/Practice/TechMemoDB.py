# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd


class TechMemoDB:
    def __init__(self):
        self.database_name = './dbms/tech_memo.db'

    def create_tech_memo(self):
        conn = sqlite3.connect(self.database_name)
        conn.execute(
            'CREATE TABLE IF NOT EXISTS tech_memo(title TEXT, category TEXT, createTime TEXT, updateTime TEXT, ' +
            'author TEXT, memo TEXT )'
        )
        conn.close()

    def list_all(self, title=None):
        query = ""
        if title is None:
            query = \
                "select title, category, createTime, updateTime, updateTime, author from tech_memo order by createTime;"
        else:
            query = \
                "select title, category, createTime, updateTime, updateTime, author from tech_memo " \
                "where title like '%" + title + "%' order by createTime;"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df

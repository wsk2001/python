# -*- coding: utf-8 -*-

"""
상관계수 작성을 위한 App
"""

import sqlite3
import pandas as pd
from collections import defaultdict

database_name = './dbms/virtual_asset.db'


def corr():
    query = \
        "select symbol, close from day_candle " \
        "where date >= '2022-05-19' " \
        "and symbol not in ('APT', 'WEMIX') " \
        "order by symbol, date "

    con = sqlite3.connect(database_name)
    vals = pd.read_sql_query(query, con).values.tolist()

    dict_symbol_close = defaultdict(list)
    dict_symbol_close.clear()

    for v in vals:
        dict_symbol_close[v[0]].append(v[1])

    con.close()

    return dict_symbol_close


def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    dic_data = pd.DataFrame(corr())
    print(dic_data.corr(method='pearson').to_markdown())


if __name__ == "__main__":
    main()

# to_markdown() : pip install tabulate
# py corr.py > aa.txt

# -*- coding: utf-8 -*-

"""
상관계수 작성을 위한 App
모든 종목에 동일한 개수의 data 가 존재 하여야 한다.
중간에 상폐 또는 추가된 종목은 제거 하여야 한다.
"""

import sqlite3
import pandas as pd
from collections import defaultdict

database_name = './dbms/virtual_asset.db'


# 460 => 2022-01-01 ~ 2023-04-05
def corr():
    date_str = "'2022-01-01'"

    sub_query = \
        "SELECT A.symbol from ( " \
        "select symbol, count(*) as cnt from day_candle " \
        "where date >= " + date_str + " " \
        "group by symbol " \
        "HAVING cnt >= 460 " \
        ") A "

    query = \
        "select symbol, hearn from day_candle " \
        "where date >= " + date_str + " " \
        "and symbol in ( " + sub_query + " ) " \
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
    print(dic_data.corr(method='pearson').round(2).to_markdown())


if __name__ == "__main__":
    main()

# to_markdown() : pip install tabulate
# py corr.py > aa.txt

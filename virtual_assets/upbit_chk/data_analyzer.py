# -*- coding: utf-8 -*-

"""
연관성 분석 App
특정 종목이 주어진 % 이상 상승 했을때 전/후로 특정% 이상 상승한 종목을 이용해 연관성 분석.
1. 지정 옵션: symbol, 기간 10,000일, earn(원본 종목의 상승%), comp earn(비교하 종목들의 상승%)
2. 모든 종목들의 일간 상승률 저장 plus 인 경우만 저장. (일자, 상승%, symbol)
3.
"""

import time
import pyupbit
from datetime import datetime, date
from common.themes import get_themes, get_all_themes
from common.utils import get_idx_values, get_tickers
import argparse
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
from ast import literal_eval
import pandas as pd
import ccxt

database_name = './dbms/virtual_asset.db'

list_theme = ['AVAX','BINANCE','BITCOIN','CHINA','DAO','DEFI','DEX','DID','DOT','FAN','KAKAO','KIMCHI','KLAY','LAYER2',
              'MAJOR','MATIC','MEDICAL','META', 'MIM','NFT','P2E','PAYMENT','PLATFORM','SECURITY','SOL','STORAGE','WEB3']

# 상승, 하락률 계산 함수
def calc_earn(open_price, close_price):
    res = ((close_price / open_price) - 1.0) * 100.0
    return res


# 거래소 table 의 data 를 동기화 한다.
def theme_updata(market):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    lst = get_tickers(market.upper())

    for v in lst:
        t = v
        if market.upper().startswith('USDT'):
            t = v[5:]
        else:
            t = v[4:]

        sql = " UPDATE coin_theme SET MARKET = ? WHERE SYMBOL = ?"
        data = ('UPBIT_' + market.upper(), t)

        print(sql, data)

        cur.execute(sql, data)
        conn.commit()

    cur.close()
    conn.close()


# 마켓코드조회
def market_code():
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails": "false"}
    response = requests.request("GET", url, params=querystring)

    # 코인이름 - 마켓코드 매핑
    r_str = response.text
    r_str = r_str.lstrip('[')  # 첫 문자 제거
    r_str = r_str.rstrip(']')  # 마지막 문자 제거
    r_list = r_str.split("}")  # str를 }기준으로 쪼개어 리스트로 변환

    # name to code
    ntc = {}
    # code to name
    ctn = {}
    # code list
    cl = []

    for i in range(len(r_list) - 1):
        r_list[i] += "}"
        if i != 0:
            r_list[i] = r_list[i].lstrip(',')
        r_dict = literal_eval(r_list[i])  # element to dict

        temp_dict = {r_dict["market"]: r_dict["korean_name"]}
        ctn.update(temp_dict)  # 코드 - 코인이름 매핑
        temp_dict = {r_dict["korean_name"]: r_dict["market"]}
        ntc.update(temp_dict)  # 코인이름 - 코드 매핑
        cl.append(r_dict["market"])  # 코드 리스트

    return cl, ntc, ctn


def create_table():
    global database_name

    conn = sqlite3.connect(database_name)
    conn.execute(
        'CREATE TABLE month_candle(ym TEXT, symbol TEXT, o REAL, h REAL, l REAL, c REAL, v REAL)')
    conn.close()


def make_month_table():
    lst = get_tickers('KRW')

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    for v in lst:
        ticker = v
        if not ticker.upper().startswith('KRW-'):
            ticker = 'KRW-' + v.upper()
        print(ticker)

        df = pyupbit.get_ohlcv(ticker, count=200, interval='month', period=1)
        for ind, row in df.iterrows():
            rdate = ind.strftime('%Y-%m-%d')

            cur.execute("INSERT INTO month_candle VALUES(?,?,?,?,?,?,?);",
                        (rdate[:7], v[4:], row["open"], row["high"], row["low"],
                         row["close"], round(row["volume"], 2)))

        time.sleep(0.2)

    conn.commit()
    conn.close()

def make_market_value():
    _, nct, _ = market_code()

    file = open("market_value.csv", "r", encoding='UTF8')
    lines = file.readlines()

    create_table()

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    for l in lines:
        if len(l.strip()) <= 0:
            continue
        no, ko, price = l.strip().split(',')
        ticker = nct[ko]
        if ticker.startswith('BTC-'):
            ticker = ticker[4:]
        if ticker.startswith('KRW-'):
            ticker = ticker[4:]
        if ticker.startswith('USDT-'):
            ticker = ticker[5:]
        print( no, ticker, ko, price)

        cur.execute("INSERT INTO market_value VALUES(?,?,?,?);",
                    (no, ticker, ko, price))
        conn.commit()

    conn.close()



def Quadruple_Witching_Day():
    query = \
        "select date, symbol, hearn as high, learn as low, earn as close,  hearn-learn as variable from day_candle " \
        "where date in ('2021-03-11', '2021-06-10', '2021-09-09', '2021-12-09', '2022-03-10', '2022-06-09') " \
        "order by symbol, date; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()
    idxs = df.index.tolist()

    print(f'종목, 일자, 고가%, 저가%, 종가%, 변동률%')

    for indexs, v in zip(idxs, vals):
        print(f'{v[1]}, {v[0]}, {v[2]:.2f}%, {v[3]:.2f}%, {v[4]:.2f}%, {v[5]:.2f}%')

    con.close()


# Theme 에 등록되어 있는 모든 ticker 를 조회 한다.
def get_theme_in_tickers(theme):
    query = \
        "select symbol from coin_theme " \
        "where MARKET = 'UPBIT_KRW' " \
        "and THEME = '" + theme.upper() + "'; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()

    lst = []
    lst.clear()

    for v in vals:
        lst.append(v)

    con.close()

    return lst


# fst_date: 각 년도의 시작 지정 (2023-01-01), last_date: 실적을 분석할 일자.
def get_theme_earn_ymd(fst_date, last_date):
    query = \
        "SELECT  F.theme,  A.symbol, A.open as O, D.high as H, C.low as L, B.close as C, " \
"round((((B.close / A.open) -1) * 100),2) as E  FROM                             " \
"(                                                                               " \
"       (                                                                        " \
"               select symbol, open from day_candle                              " \
"               where date = '" + fst_date + "' " \
"               group by symbol                                                  " \
"       ) A,                                                                     " \
"       (                                                                        " \
"               select symbol, close from day_candle                             " \
"               where date = '" + last_date + "' " \
"               group by symbol                                                  " \
"       ) B,                                                                     " \
"       (                                                                        " \
"               select symbol, min(close) low from day_candle                    " \
"               where date like '2023-%'                                         " \
"               group by symbol                                                  " \
"       ) C,                                                                     " \
"       (                                                                        " \
"               select symbol, max(close) high from day_candle                   " \
"               where date like '2023-%'                                         " \
"               group by symbol                                                  " \
"       ) D,                                                                     " \
"       (                                                                        " \
"               select symbol, theme from coin_theme                             " \
"               where market = 'UPBIT_KRW'                                       " \
"       ) F                                                                      " \
")                                                                               " \
"WHERE A.symbol = B.symbol                                                       " \
"AND A.symbol = C.symbol                                                         " \
"AND A.symbol = D.symbol                                                         " \
"AND A.symbol = F.symbol                                                         " \
"order by F.theme, A.symbol;                                                     "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()

    con.close()

    return vals



#########################################
# 등락 통계
# 진행 방향(등락)이 바뀌는 일자 통계
#########################################
def pivot_check(ticker):
    query = \
        "select date, symbol, earn, open, close from day_candle " \
        "where symbol = '" + ticker.upper() + "' order by date; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)
    vals = df.values.tolist()
    idxs = df.index.tolist()

    lst = []
    lst.clear()

    start_date = ''
    end_date = ''
    flag = 0
    count = 0
    open_price = 0
    close_price = 0

    for indexs, v in zip(idxs, vals):
        fearn = float(v[2])
        if count == 0:
            if 0.0 < fearn:
                flag = 1
            elif fearn < 0.0:
                flag = -1
            count += 1
            start_date = v[0]
            end_date = v[0]
            open_price = float(v[3])
            close_price = float(v[4])
            continue
        else:
            if flag == 1:
                if 0.0 < fearn:
                    count += 1
                    end_date = v[0]
                    close_price = float(v[4])
                    continue
                elif fearn < 0.0:
                    cearn = calc_earn(open_price, close_price)
                    lst.append([start_date, end_date, count, cearn])
                    count = 1
                    flag = -1
                    start_date = v[0]
                    end_date = v[0]
                    open_price = float(v[3])
                    close_price = float(v[4])
            elif flag == -1:
                if 0.0 < fearn:
                    cearn = calc_earn(open_price, close_price)
                    lst.append([start_date, end_date, -1 * count, cearn])
                    count = 1
                    flag = 1
                    start_date = v[0]
                    end_date = v[0]
                    open_price = float(v[3])
                    close_price = float(v[4])
                elif fearn < 0.0:
                    count += 1
                    end_date = v[0]
                    close_price = float(v[4])
                    continue
            else:
                end_date = v[0]
                close_price = float(v[4])
                continue

    cearn = calc_earn(open_price, close_price)
    if flag == -1:
        lst.append([start_date, end_date, -1 * count, cearn])
    else:
        lst.append([start_date, end_date, count, cearn])

    pv_cnt = 0
    for l in lst:
        print(f'{l[0]} ~ {l[1]}, {l[2]}, {round(l[3],2)}%')
        pv_cnt += 1

    print()
    print(f'{ticker.upper()} pivot({pv_cnt}) / total({len(vals)}), avg dura:{round(len(vals)/pv_cnt, 2)}')

    con.close()



def get_binance_ohlcv(ticker, count=1):
    binance = ccxt.binance()
    parameters = {
        'start': '1',
        'limit': '1',
        'convert': 'USD'
    }

    # 2017-08-17
    start_date = '2017-01-01'
    start = int(time.mktime(datetime.strptime(start_date + ' 00:00', '%Y-%m-%d %H:%M').timetuple())) * 1000

    ohlcv = binance.fetch_ohlcv(ticker.upper()+'/USDT', timeframe='1d', limit=count, since=start)
    df = pd.DataFrame(ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    print(df)


# 2023년 테마별 실적 평균 (1월 1일 ~ 지정 일자)
def get_theme_earn(fst_date, last_date):
    datas = get_theme_earn_ymd(fst_date, last_date)

    theme = ''
    total = 0.0
    cnt = 0

    lst_grouping = []
    lst_grouping.clear()
    for v in datas:
        if theme != v[0]:
            if len(theme) == 0:
                theme = v[0]
                total = float(v[6])
                cnt = 1
                continue
            else:
                lst_grouping.append([theme, round(total/cnt, 2) ])
                theme = v[0]
                total = float(v[6])
                cnt = 1
                continue
        else:
            total += float(v[6])
            cnt += 1

    lst_grouping.append([theme, round(total / cnt, 2)])

    return lst_grouping


def delete_db(day):
    lst = get_tickers('KRW')

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    sql = "DELETE FROM theme_summry WHERE ymd" + ">= '" + day + "';"
    cur.execute(sql)

    conn.commit()
    conn.close()


def insert_theme_summary(l):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("INSERT INTO theme_summry VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                (l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8], l[9], l[10], l[11], l[12], l[13],
                 l[14], l[15], l[16], l[17], l[18], l[19], l[20], l[21], l[22], l[23], l[24], l[25], l[26], l[27], l[28]))

    conn.commit()
    conn.close()



def main():
    # Quadruple_Witching_Day()

    #create_table()
    #make_month_table()

    ##create_minute_table()
    #get_date('BTC', 30000, 'minute5')

    #get_binance_ohlcv('BTC', 10000)


    #pivot_check('btc')

    # for theme in list_theme:
    #     tikers = get_theme_in_tickers(theme)
    #     print()
    #     print(theme)
    #     print(tikers)

    days = [
         '2023-01-27','2023-01-28','2023-01-29','2023-01-30','2023-01-31'
    ]


    themes = ['YMD','AVAX','BINANCE','BITCOIN','CHINA','DAO','DEFI','DEX','DID','DOT','FAN','KAKAO','KIMCHI','KLAY',
              'LAYER2','MAJOR','MATIC','MEDICAL', 'METAVERSE', 'MIM','NFT','P2E','PAYMENT','PLATFORM','SECURITY',
              'SOL','STORAGE', 'WEB3','ALL']

    print(themes)

    for day in days:
        theme_group = get_theme_earn('2023-01-01', day)

        cnt = 0
        earn = 0.0
        lst = []
        lst.clear()
        lst.append(day)
        for t in theme_group:
            cnt += 1
            earn += float(t[1])
            lst.append(float(t[1]))
        lst.append(round(earn/cnt, 2))

        delete_db(day)
        insert_theme_summary(lst)

        print(lst)
        print()

    # theme_updata('USDT')
    # theme_updata('BTC')
    # theme_updata('KRW')


if __name__ == "__main__":
    main()


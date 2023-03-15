# importing package
import matplotlib.pyplot as plt
import time, sys, getopt
import datetime
import sqlite3
import pandas as pd
import numpy as np
from datetime import date, timedelta

# 한글 폰트 사용을 위해서 세팅 (아래 4줄)
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

database_name = './dbms/virtual_asset.db'


def select_ytd():
    query = \
        "select ymd, earn_btc, earn_all from ytd; "

    con = sqlite3.connect(database_name)
    df = pd.read_sql_query(query, con)

    con.close()

    return df


def main(argv):
    df = select_ytd()

    x = df['ymd'].values.tolist()
    btc = df['earn_btc'].values.tolist()
    all = df['earn_all'].values.tolist()

    plt.xticks(np.arange(0, len(x), step=10))

    plt.title('UPBIT 원화 마켓 YTD(Year To Date): ' + x[0] + ' ~ ' + x[-1] )
    plt.grid(True)

    plt.plot(x, btc, label="btc", color="red", marker='o', markersize=4)
    plt.plot(x, all, label="all", color="blue", marker='o', markersize=4)

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main(sys.argv)

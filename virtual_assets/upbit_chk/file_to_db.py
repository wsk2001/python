import time
import datetime
import sys, getopt
import pyupbit
from pandas import Series, DataFrame
import requests
import sqlite3

# CREATE TABLE "stat" (
# 	"ticker"	TEXT NOT NULL,
# 	"date"	TEXT NOT NULL,
# 	"week_day"	TEXT NOT NULL,
# 	"open"	REAL NOT NULL,
# 	"high"	REAL NOT NULL,
# 	"low"	REAL NOT NULL,
# 	"close"	REAL NOT NULL,
# 	"volume"	REAL NOT NULL,
# 	"value"	REAL NOT NULL,
# 	"profit"	REAL NOT NULL,
# 	"inc" 	REAL NOT NULL,
# 	PRIMARY KEY("ticker","date")
# );

database = "./db/upbit.db3"
table = "stat"
cols = ("ticker", "date", "week_day", "open", "high", "low", "close", "volume", "value", "profit", "inc")

def week_day_stat(t, limit):
    p = [0, 0, 0, 0, 0, 0, 0]
    m = [0, 0, 0, 0, 0, 0, 0]

    conn = sqlite3.connect(database, isolation_level=None)
    c = conn.cursor()

    param3 = (table, t, limit)
    for row in c.execute("SELECT DATE, OPEN, HIGH, LOW, CLOSE, WEEK_DAY\
                          FROM %s\
                          WHERE ticker='%s' \
                          ORDER by DATE DESC \
                          LIMIT %s" % param3):
        d, o, h, l, c, w = row

        if o < c:
            p[int(w)-1] = p[int(w)-1] + 1
        else:
            m[int(w)-1] = m[int(w)-1] + 1

    print(t, p[0], m[0], p[1], m[1], p[2], m[2], p[3], m[3], p[4], m[4], p[5], m[5], p[6], m[6])

def write_db(v, d, wd, o, h, low, close, volume, value, p, inc):
    conn = sqlite3.connect(database, isolation_level=None)
    c = conn.cursor()
    c.execute("INSERT INTO stat VALUES('" + v + '\',\'' + str(d) + '\',\'' + str(wd) + '\',\'' +\
              str(o) + '\',\'' + str(h) + '\',\'' + str(low) + '\',\'' + str(close) + '\',\''\
              + str(volume) + '\',\''\
              + str(value) + '\',\''\
              + str(f'{p:3.2f}') + '\',\''\
              + str(inc) + '\' )')
    conn.close()

def write_data(v, d, _o, _h, _l, _c, _volume, _value, p, inc):
    o = float(_o)
    h = float(_h)
    l = float(_l)
    c = float(_c)
    volume = float(_volume)
    value = float(_value)

    year, month, day = (int(x) for x in d.split('-'))
    wd = datetime.date(year, month, day).isoweekday()

    print(f'{v[4:]} {d} {wd} {o} {h} {l} {c} {volume} {value} {p:3.2f} {inc}')
    write_db(v[4:], d, wd, o, h, l, c, volume, value, p, inc)

def read_file(fname):
    f = open(fname, "r")
    lines = f.readlines()
    i = 0
    ticker_name = ''
    inc = 0
    for l in lines:
        line = l.strip()
        if i == 0:
            ticker_name = line
            i += 1
            continue

        if i == 1:
            i += 1
            continue

        s = line.split()
        if 8 == len(s):
            o = float(s[2])
            c = float(s[5])
            p = ((c / o) - 1.0) * 100.0
            if inc == 0:
                if o < c:
                    inc += 1
                elif c < o:
                    inc -= 1
            elif 0 < inc:
                if o < c:
                    inc += 1
                elif c < o:
                    inc = -1
            else:
                if o < c:
                    inc = 1
                elif c < o:
                    inc -= 1

            write_data(ticker_name, s[0], s[2], s[3], s[4], s[5], s[6], s[7], p, inc)

        i += 0

def main(argv):
    f = open("files.txt", "r")
    lines = f.readlines()

    for l in lines:
        fname = l.strip()
        if not fname:
            continue
        read_file(fname)

    f.close()


if __name__ == "__main__":
    # week_day_stat('ADA', 60)
    main(sys.argv)


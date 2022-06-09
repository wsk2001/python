import time
import datetime
import sys, getopt
import pyupbit
from time import sleep

open_posi = 0
close_posi = 3

def earning(t, str_date):
    if not t.upper().startswith('KRW-'):
        t = 'KRW-' + t

    arr_dt = ['00:00:00' for i in range(144)]
    arr_ud = [0 for i in range(144)]

    try:
        base_dt = str_date + "  23:51:10"
        dfs = pyupbit.get_ohlcv(t, interval='day', count=2, period=1, to=str_date.strip())
        dft = pyupbit.get_ohlcv(t, interval='minute10', count=144, period=1, to=base_dt)

        # ohlcv
        vs = dfs.values.tolist()
        vt = dft.values.tolist()
        sv_1 = vs[0][open_posi]
        sv_2 = vs[1][open_posi]
        indexs = dft.index.tolist()

        for i in range(len(vt)):
            s_idx = str(indexs[i])[11:]
            arr_dt[i] = s_idx
            cmp_v = 0.0

            if '09:00:00' <= s_idx:
                cmp_v = sv_2
            else:
                cmp_v = sv_1

            if cmp_v < vt[i][close_posi]:
                arr_ud[i] = 1
            elif cmp_v > vt[i][close_posi]:
                arr_ud[i] = -1
    except:
        print('data getering error')
    finally:
        return t, arr_dt, arr_ud

def get_ticker_list():
    return pyupbit.get_tickers(fiat="KRW")


def main(argv):
    str_date = "2022-01-01"

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hd:"
                                       , ["help", "date="])

    except getopt.GetoptError:
        print(argv[0], '-d <date>')
        print('ex) python', f'{argv[0]}', '-d 2022-06-05')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-d <date>')
            print('ex) python', f'{argv[0]}', '-d 2022-06-05')
            print('ex) python', f'{argv[0]}', '--date 2022-06-03')
            sys.exit()

        elif opt in ("-d", "--date"):  # ticker symbol
            str_date = arg

    lst = get_ticker_list()

    arr_dt = ['00:00:00' for i in range(144)]
    arr_up = [0 for i in range(144)]
    arr_down = [0 for i in range(144)]
    flag_start = 0

    for ticker in lst:
        print(ticker[4:],  'chaecking... ')
        if flag_start == 0 :
            _, arr_dt, arr_ud = earning(ticker, str_date)
            flag_start = 1
        else:
            _, _, arr_ud = earning(ticker, str_date)

        for i in range(len(arr_ud)):
            if arr_ud[i] < 0 :
                arr_down[i] = arr_down[i] + 1
            if 0 < arr_ud[i] :
                arr_up[i] = arr_up[i] + 1
        sleep(0.2)

    print("\n")
    print("업비트 원화 마켓 종목수 : " + str(len(lst)) + " 일자: " + str_date )
    print("시간, 상승, 하락")

    for i in range(len(arr_ud)):
        print(arr_dt[i]+',', str(arr_up[i])+',', arr_down[i] )

if __name__ == "__main__":
    main(sys.argv)

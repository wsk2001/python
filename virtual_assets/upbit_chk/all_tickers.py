import time, sys, getopt
import pyupbit


def calc_earn(v):
    try:
        df = pyupbit.get_ohlcv(v, count=1)
        o = df['open'][0]
        c = df['close'][0]
        p = ((c / o) - 1.0) * 100.0

        return v[4:], o, c, p
    except:
        return None, None, None, None


def main(argv):
    lst = pyupbit.get_tickers(fiat="KRW")
    earns = [[]]

    earns.clear()

    for v in lst:
        arr = calc_earn(v)
        if arr is not None:
            earns.append(list(arr))
        time.sleep(0.2)

    earns = sorted(earns, key=lambda x: x[3], reverse=True)

    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    print('ticker, open, close, earning')

    for e in earns:
        print(f'{e[0]},', f'{e[1]},', f'{e[2]},', f'{e[3]:.2f}%')


if __name__ == "__main__":
    main(sys.argv)

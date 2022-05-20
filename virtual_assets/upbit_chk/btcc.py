from time import sleep
import requests
import sys, getopt, datetime

ep = 'https://api.binance.com'
ping = '/api/v1/ping'
ticker24h = '/api/v1/ticker/24hr'


def get_ohlc_binance(t):
    params = {'symbol': t + 'USDT'}
    r1 = requests.get(ep+ping)
    r2 = requests.get(ep+ticker24h, params=params)
    # print(r2.json())

    return float(r2.json()['openPrice']), float(r2.json()['lastPrice']), float(r2.json()['priceChangePercent'])


def main(argv):

    file = open("btcc.txt", "r")
    lines = file.readlines()
    position = 'LONG'
    base_amt = 30000.0
    base_str = '30000.0'
    sleep_sec = 10

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hs:", ["sleep="])

    except getopt.GetoptError:
        print(argv[0], '-s <sleep seconds>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-s <sleep seconds>')
            sys.exit()

        elif opt in ("-s", "--sleep"):  # upbit item symbol
            sleep_sec = int(arg.strip())

    for l in lines:
        line = l.strip()
        if not line:
            continue

        if line.startswith("#") or line.startswith("//"):
            continue

        if len(line) <= 0:
            continue

        strLine = line.split()
        base_str = strLine[2]
        base_amt = float(base_str)

        position = strLine[0]

    tickers = ['BTC']

    while 1:
        cur = datetime.datetime.now().strftime('%H:%M:%S')

        for t in tickers:
            open_price, last_price, chang_per = get_ohlc_binance(t)
            earn = ((last_price / base_amt) - 1.0) * 100.0
            if position.startswith('SHORT'):
                earn = earn * -1.0
            print(cur, t, position, '(' + base_str + ')', open_price, last_price, f'{chang_per:.2f}%', f'{earn:.2f}%')

        sleep(sleep_sec)


if __name__ == "__main__":
    main(sys.argv)

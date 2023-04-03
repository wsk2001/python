import time
import datetime
import sys, getopt, signal
from common.utils import get_binance_btc, get_fng
from common.utils import upbit_get_usd_krw
from common.dominance import aoa_position
import requests
from win10toast import ToastNotifier
import pyupbit

item_list = []

stop_loss = -1.0
take_profit = 1.0


class Item:
    def __init__(self, ticker, enter, count, pay_off, magn):
        self.ticker = ticker
        self.enter = enter
        self.count = count
        self.pay_off = pay_off
        self.magn = magn


def exit_gracefully(signal, frame):
    sys.exit(0)


def rate(v):
    df = pyupbit.get_ohlcv(v, count=1)
    open_price = df['open'][0]
    close_price = df['close'][0]
    res = ((close_price / open_price) - 1.0) * 100.0
    return res, close_price

def get_binance_btc_json(ticker, enter, count, pay_off, magn):
    ep = 'https://api.binance.com'
    ping = '/api/v1/ping'
    ticker24h = '/api/v1/ticker/24hr'

    params = {'symbol': ticker + 'USDT'}
    requests.get(ep + ping)
    r2 = requests.get(ep + ticker24h, params=params)

    cur = datetime.datetime.now().strftime('%H:%M:%S')
    close_price = float(r2.json()['lastPrice'])
    price_change = float(r2.json()['priceChangePercent'])

    # count 에는 이미 magn 이 반영 되어 있음.
    cur_rate = ((close_price / enter) - 1.0) * 100.0 * count
    cur_tot = (close_price - enter) * count

    # If short
    posi_short = False
    if enter < pay_off:
        cur_rate *= -1.0
        cur_tot *= -1.0
        posi_short = True

    posi_txt = ''
    if posi_short:
        posi_txt = ' Short'
    else:
        posi_txt = ' Long'

    btc_rate, _ = rate('KRW-BTC')

    print(cur + f' ({btc_rate:.2f}%) ' + f' {ticker}' + posi_txt + f' x{int(magn)},  {count:6.3f}' + ', ' +
          f'{enter:6.5f}' + ', ' + f'{close_price:6.5f}' + ', ' + f'SL {pay_off:6.5f}' + ', ' +
          f'{cur_tot:4.3f}')

    if cur_tot < stop_loss:
        toaster = ToastNotifier()
        toaster.show_toast("Toast Notifier", f' {ticker:<6}' + ' Stop Loss. ' + f'{cur_tot:4.2f}')

    if take_profit < cur_tot:
        toaster = ToastNotifier()
        toaster.show_toast("Toast Notifier", f' {ticker:<6}' + ' Take profit. ' + f'{cur_tot:4.2f}')


def main(argv):
    global stop_loss, take_profit
    inv_amt = 0.0
    sleep_sec = 5
    view_binance = False
    trader_posi = aoa_position()

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

    file = open("futures.txt", "r")
    lines = file.readlines()
    ticker_count = 0
    for l in lines:
        line = l.strip()
        if not line:
            continue

        if line.startswith("#") or line.startswith("//"):
            continue

        if len(line) <= 0:
            continue

        if line.upper().startswith("STOP_LOSE"):
            s = line.split()
            stop_loss = float(s[1])
            continue

        if line.upper().startswith("TAKE_PROFIT"):
            s = line.split()
            take_profit = float(s[1])
            continue

        s = line.split()
        item_list.append(Item(s[0], float(s[1]), float(s[2]), float(s[3]), float(s[4][1:])))
        ticker_count += 1

    file.close()

    if ticker_count <= 0:
        print('No tickers to monitoring.')
        print('Check the futures.txt file.')
        exit(0)

    i = 0
    chg_posi = False
    disp_cnt = 0
    while True:
        i = 0
        for itm in item_list:
            get_binance_btc_json(itm.ticker, itm.enter, itm.count, itm.pay_off, itm.magn)
            i += 1
            time.sleep(0.1)

        time.sleep(sleep_sec)
        tmp_posi = aoa_position()
        if not tmp_posi.startswith(trader_posi):
            trader_posi = tmp_posi
            chg_posi = True

        if 0 < chg_posi:
            toaster = ToastNotifier()
            toaster.show_toast("Position change:", trader_posi)
            disp_cnt += 1
            if 10 < disp_cnt:
                chg_posi = False
                disp_cnt = 0

        if 1 < i:
            print()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_gracefully)
    main(sys.argv)

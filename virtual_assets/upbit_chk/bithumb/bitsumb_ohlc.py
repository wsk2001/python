import datetime
import getopt
import sys
import time
import pybithumb

def get_amt(ticker):
    print(ticker)
    res = pybithumb.Bithumb.get_ohlc(ticker)
    print(type(res))
    o = res.get(ticker)[0]
    h = res.get(ticker)[1]
    l = res.get(ticker)[2]
    c = res.get(ticker)[3]
    e = (c - o) / o * 100.0
    print('{}: open={}, high={}, low={}, current={}, earning={:0.3f}%'
          .format(ticker, o, h, l, c, e))

def usage(app):
    print('python ', app, '-t <ticker symbol>')
    print('ex: ', 'python ', app, '-t AWT')
    print('    ', 'python ', app, '-t BTT')
    sys.exit(2)

def main(argv):
    ticker = 'AWT'

    try:
        opts, etc_args = getopt.getopt(argv[1:], "ht:", ["help", "ticker="])

    except getopt.GetoptError:
        usage(argv[0])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(argv[0])
        elif opt in ("-t", "--ticker"):  # airdrop list 가 저장되어 있는 파일 (list.xlsx)
            ticker = arg

    get_amt(ticker)

if __name__ == "__main__":
    main(sys.argv)

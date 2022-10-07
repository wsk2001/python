# -*- coding: utf-8 -*-

import plotly.graph_objects as go
import sys
import pyupbit
import argparse


# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
#
# fig = go.Figure(data=go.Ohlc(x=df['Date'],
#                     open=df['AAPL.Open'],
#                     high=df['AAPL.High'],
#                     low=df['AAPL.Low'],
#                     close=df['AAPL.Close']))
# fig.show()

def view_chart(ticker, cnt, interval='day'):

    if not ticker.startswith('KRW-') and not ticker.startswith('BTC-') and not ticker.startswith('USDT-'):
        ticker = 'KRW-' + ticker

    df = pyupbit.get_ohlcv(ticker, interval=interval, count=cnt, period=1)

    fig = go.Figure(data=go.Ohlc(x=df.index,
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close'], increasing_line_color='cyan', decreasing_line_color='gray'))

    # fig.update_layout(
    #     title='The Great Recession', yaxis_title=ticker)

    fig.show()


def main(argv):
    parser = argparse.ArgumentParser(description='옵션 지정 방법')
    parser.add_argument('--symbol', required=False, default='ada', help='심볼 (BTC, ETH, ADA, ...)')
    parser.add_argument('--count', required=False, default=200, help='data gettering size (default=90)')
    parser.add_argument('--interval', required=False, default='day',
                        help='candle 종류 (day, week, month, minute1, ...)')

    args = parser.parse_args()
    symbol = args.symbol
    count = int(args.count)
    interval = args.interval

    view_chart(symbol, count, interval)


if __name__ == "__main__":
    main(sys.argv)

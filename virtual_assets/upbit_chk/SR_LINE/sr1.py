# https://raw.githubusercontent.com/WestXu/support_resistance_line/master/tests/test_support_resistance_line.py
import pandas as pd
import time
import datetime
import sys, getopt

from support_resistance_line import SupportResistanceLine

import pyupbit
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

def test(v):

    df = pd.DataFrame(pyupbit.get_ohlcv(v, interval='days', count=100, period=1), columns=['close'])
    my_series = df.squeeze()

    SupportResistanceLine(my_series).plot_both(show=True)



def main(argv):
    test('KRW-LINK')

if __name__ == "__main__":
    main(sys.argv)

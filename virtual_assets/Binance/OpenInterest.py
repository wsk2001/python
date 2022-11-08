import time, sys
import datetime as dt

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

funding_history_before_btc = 0
funding_history_before_usdt = 0
long_history_before_btc = 0
short_history_before_btc = 0
btcusdt = 0


def longshort_ratio_func():
    try:
        output_text_return = ""
        global funding_history_before_btc
        global funding_history_before_usdt
        global long_history_before_btc
        global short_history_before_btc

        funding_history_raw = urlopen("https://www.binance.com/futures/data/openInterestHist?symbol=FTTUSDT&period=5m")
        funding_history_parser = BeautifulSoup(funding_history_raw, "html.parser")
        Interest_Datas = str(funding_history_parser)
        Interest_Datas = json.loads(Interest_Datas)

        sumOpenInterest = round(float(Interest_Datas[29]['sumOpenInterest']), 3)
        sumOpenInterestValue = int(round(float(Interest_Datas[29]['sumOpenInterestValue']), 0))

        if (funding_history_before_btc == 0):
            output_text_return += "{:0,.3f}".format(sumOpenInterest) + " FTT ( - ), "

        else:
            if (sumOpenInterest - funding_history_before_btc > 0):
                output_text_return += "{:0,.3f}".format(sumOpenInterest) + " FTT (+" + "{:0,.3f}".format(
                    sumOpenInterest - funding_history_before_btc) + "), "

            else:
                output_text_return += "{:0,.3f}".format(sumOpenInterest) + " FTT (" + "{:0,.3f}".format(
                    sumOpenInterest - funding_history_before_btc) + "), "

        if (funding_history_before_usdt == 0):
            output_text_return += "{:0,.0f}".format(sumOpenInterestValue) + " USDT ( - ), "

        else:
            if (sumOpenInterestValue - funding_history_before_usdt > 0):
                output_text_return += "{:0,.0f}".format(sumOpenInterestValue) + " USDT (+" + "{:0,.0f}".format(
                    sumOpenInterestValue - funding_history_before_usdt) + "), "

            else:
                output_text_return += "{:0,.0f}".format(sumOpenInterestValue) + " USDT (" + "{:0,.0f}".format(
                    sumOpenInterestValue - funding_history_before_usdt) + "), "

        if (sumOpenInterest == funding_history_before_btc):
            output_text_return = ""
            return output_text_return

        funding_history_before_btc = sumOpenInterest
        funding_history_before_usdt = sumOpenInterestValue

        longshort_ratio_raw = urlopen(
            "https://www.binance.com/futures/data/globalLongShortAccountRatio?symbol=FTTUSDT&period=5m")

        longshort_ratio_parser = BeautifulSoup(longshort_ratio_raw, "html.parser")
        longshort_ratio_datas = str(longshort_ratio_parser)
        longshort_ratio_datas = json.loads(longshort_ratio_datas)

        longshort_ratio_longAccount = float("{:0,.2f}".format(float(longshort_ratio_datas[29]['longAccount']) * 100))
        longshort_ratio_shortAccount = float("{:0,.2f}".format(float(longshort_ratio_datas[29]['shortAccount']) * 100))

        if (long_history_before_btc == 0):
            output_text_return += str(longshort_ratio_longAccount) + "% ( - ), "

        else:
            if (longshort_ratio_longAccount - long_history_before_btc >= 0):
                output_text_return += str(longshort_ratio_longAccount) + "% (+" + str(
                    "{:0,.2f}".format(longshort_ratio_longAccount - long_history_before_btc)) + "), "

            else:
                output_text_return += str(longshort_ratio_longAccount) + "% (" + str(
                    "{:0,.2f}".format(longshort_ratio_longAccount - long_history_before_btc)) + "), "

        if (short_history_before_btc == 0):
            output_text_return += str(longshort_ratio_shortAccount) + "% ( - )"

        else:
            if (longshort_ratio_shortAccount - short_history_before_btc >= 0):
                output_text_return += str(longshort_ratio_shortAccount) + "% (+" + str(
                    "{:0,.2f}".format(longshort_ratio_shortAccount - short_history_before_btc)) + ")"

            else:
                output_text_return += str(longshort_ratio_shortAccount) + "% (" + str(
                    "{:0,.2f}".format(longshort_ratio_shortAccount - short_history_before_btc)) + ")"

        long_history_before_btc = longshort_ratio_longAccount
        short_history_before_btc = longshort_ratio_shortAccount

        return output_text_return

    except:
        return ''


def main(argv):
    print("시각,  미결제 약정,  미결제 약정의 명목 가치,   Long,   Short")

    while True:
        now = dt.datetime.now().strftime('%H:%M:%S')
        print(now, longshort_ratio_func())
        time.sleep(5 * 60)


if __name__ == "__main__":
    main(sys.argv)

# https://raw.githubusercontent.com/beomsun0829/Open_Interest_Telegram_Alerts/main/Open_Interest_Telegram_Alerts.py

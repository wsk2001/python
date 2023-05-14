# -*- coding: utf-8 -*-

from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup as bs
import time, datetime
import sys, getopt, signal
from win10toast import ToastNotifier
import numpy as np

position = 'Neutral'
old_posi = 'Neutral'
list_up_count = []


def exit_gracefully(signal, frame):
    sys.exit(0)


def ma5():
    return int(np.average(list_up_count[-5:]))


async def get_data():
    global old_posi
    global position
    global list_up_count

    async with async_playwright() as pw:
        ## chromium, firefox, webkit
        browser = await pw.firefox.launch()
        page = await browser.new_page()
        await page.goto('https://coinness.com/market/ticker')
        # await page.goto('https://coinness.live/market/ticker')
        time.sleep(6)

        html = await page.content()
        soup = bs(html, 'html.parser').prettify()
        lines = soup.splitlines()

        list_str = []

        flag = False

        await browser.close()

        str_up = ''
        str_down = ''
        flag_up = False

        for line in lines:
            line = line.strip()

            if line.startswith('<'):
                continue

            if line.startswith('선물'):
                flag = True
                continue

            if 30 < len(line):
                continue

            if flag:
                if flag_up == False:
                    if line.startswith('코인이 상승중이네요!'):
                        flag_up = True
                        continue
                    str_up += line
                elif flag_up == True:
                    if line.startswith('코인이 하락중이네요!'):
                        break
                    str_down += line

        cur = datetime.datetime.now().strftime('%H:%M:%S')
        print(f'{cur} up={str_up}, down={str_down}')

async def main(argv):
    global position
    global list_up_count

    count_min = 1
    unit_min = 60

    list_up_count.clear()

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hs:", ["sleep="])

    except getopt.GetoptError:
        print(argv[0], '-s <sleep mins>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-s <sleep mins>')
            sys.exit()

        elif opt in ("-s", "--sleep"):
            count_min = int(arg.strip())

    while True:
        await get_data()
        time.sleep(count_min * unit_min)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_gracefully)
    asyncio.run(main(sys.argv))

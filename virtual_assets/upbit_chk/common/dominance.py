from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
import asyncio
from bs4 import BeautifulSoup as bs
import time


# 2022-10-26 sync 로 바꿈.
def btctools_get_dominance(site):
    with sync_playwright() as pw:
        browser = pw.webkit.launch()
        page = browser.new_page()
        page.goto(site)
        time.sleep(3)

        html = page.content()
        soup = bs(html, 'html.parser').prettify()
        lines = soup.splitlines()
        browser.close()

        list_str = []
        list_str.clear()
        fflag = False
        icount = 0
        rtn_value = ''

        for line in lines:
            line = line.strip()
            if line.startswith('<'):
                continue
            if line.startswith('비트 코인 시장 지배력'):
                fflag = True
                continue
            if fflag == False:
                continue
            rtn_value = line
            rtn_value = rtn_value.strip('%')
            break;
        return rtn_value


# 2022-10-26 sync 로 바꿈.
def get_dominance():
    try:
        coinness_schedule = 'https://btctools.io/kr/stats/dominance'
        dominance = btctools_get_dominance(coinness_schedule)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return dominance


# 워뇨띠 포지션
def aoa_position():
    # sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    # sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

    r = requests.get('https://www.bitsignal.me/indexw.php');

    soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
    str0 = soup.prettify()
    idx = str0.find('<td class="one">')
    str1 = str0[idx:idx + 300]
    strs = str1.splitlines()

    str_out = ''
    for s in strs:
        if s.strip().startswith('<'):
            continue
        else:
            str_out = str_out + ' ' + s.strip()

    return str_out.strip()


if __name__ == "__main__":
    print(get_dominance())
    print(aoa_position())

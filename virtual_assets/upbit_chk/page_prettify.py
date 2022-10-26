from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup as bs
import time
import datetime
import re


async def get_dominance(site):
    async with async_playwright() as pw:
        # browser = await pw.chromium.launch()
        browser = await pw.webkit.launch()
        page = await browser.new_page()
        await page.goto(site)
        time.sleep(3)

        html = await page.content()
        soup = bs(html, 'html.parser').prettify()
        lines = soup.splitlines()

        await browser.close()

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
            print(line)
            rtn_value = line
            rtn_value = rtn_value.strip('%')
            break;
        return rtn_value

async def get_data(site):
    async with async_playwright() as pw:
        # browser = await pw.chromium.launch()
        browser = await pw.webkit.launch()
        page = await browser.new_page()
        await page.goto(site)
        time.sleep(6)

        html = await page.content()
        soup = bs(html, 'html.parser').prettify()
        lines = soup.splitlines()

        await browser.close()

        list_str = []
        list_str.clear()
        fflag = False
        icount = 0

        for line in lines:
            line = line.strip()
            if line.startswith('<'):
                continue
            print(line)


async def get_kimpga_liquidation(site):
    async with async_playwright() as pw:
        # browser = await pw.chromium.launch()
        browser = await pw.webkit.launch()
        page = await browser.new_page()
        await page.goto(site)
        time.sleep(6)

        html = await page.content()
        soup = bs(html, 'html.parser').prettify()
        lines = soup.splitlines()

        await browser.close()

        list_str = []
        list_str.clear()
        fflag = False
        icount = 0

        for line in lines:
            line = line.strip()
            if line.startswith('<'):
                continue
            if line.startswith('전체 (24H)'):
                fflag = True
                print('청산 비율 24H, 출처: 김프가')
                print('구분, 롱, 숏')
                list_str.append('전체')
                icount += 1
                continue
            if line.startswith('XRP'):
                break
            if fflag is False:
                continue
            list_str.append(line)
            icount += 1
            if 3 <= icount:
                print(f'{list_str[0]}, {list_str[1]}, {list_str[2]}')
                list_str.clear()
                icount = 0


async def get_coinness_schedule(site):
    async with async_playwright() as pw:
        # browser = await pw.chromium.launch()
        browser = await pw.webkit.launch()
        page = await browser.new_page()
        await page.goto(site)
        time.sleep(6)

        html = await page.content()
        soup = bs(html, 'html.parser').prettify()
        lines = soup.splitlines()

        await browser.close()

        list_str = []
        list_str.clear()
        fflag = False
        icount = 0

        for line in lines:
            line = line.strip()
            if line.startswith('<'):
                continue
            if line.startswith('가장빠르고'):
                break
            if line.count('년') and line.count('월'):
                fflag = True
                print(line, '일정, 출처: coinness')
                continue
            if fflag is False:
                continue
            list_str.append(line)
            icount += 1
            if 5 <= icount:
                print(list_str[0], list_str[1], list_str[2])
                icount = 0
                list_str.clear()

async def main():
    pages = ['https://www.binance.com/en/markets/coinInfo-Metaverse',
             'https://www.binance.com/en/markets/coinInfo-Gaming',
             'https://www.binance.com/en/markets/coinInfo-defi',
             'https://www.binance.com/en/markets/coinInfo-innovation-zone',
             'https://www.binance.com/en/markets/coinInfo-Layer1_Layer2',
             'https://www.binance.com/en/markets/coinInfo-fan_token',
             'https://www.binance.com/en/markets/coinInfo-NFT',
             'https://www.binance.com/en/markets/coinInfo-storage-zone',
             'https://www.binance.com/en/markets/coinInfo-Polkadot',
             'https://www.binance.com/en/markets/coinInfo-pos',
             'https://www.binance.com/en/markets/coinInfo-pow',
             'https://www.binance.com/en/markets/coinInfo-Launchpad',
             'https://www.binance.com/en/markets/coinInfo-Launchpool',
             'https://www.binance.com/en/markets/coinInfo-bnbchain',
             'https://www.binance.com/en/markets/coinInfo-ETF',
             'https://www.binance.com/en/markets/coinInfo-Infrastructure']

    coinness_schedule = 'https://btctools.io/kr/stats/dominance'
    dominance = await get_dominance(coinness_schedule)
    print(dominance)

    # coinness_schedule = 'https://coinness.live/market/schedule'
    # await get_coinness_schedule(coinness_schedule)

    #kimpga_liquidation = 'https://kimpga.com/statistics/liquidation'
    #await get_kimpga_liquidation(kimpga_liquidation)

if __name__ == '__main__':
    asyncio.run(main())

# <tbody> <tr> data </tr> </tbody>

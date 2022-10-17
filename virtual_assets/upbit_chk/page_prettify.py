from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup as bs
import time
import datetime
import re


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
        fflag = False

        for line in lines:
            print(line)


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

    lnk = 'https://kimpga.com/statistics/longshort'
    await get_data(lnk)
    # await get_data(pages[0])
    # await get_data('https://coinmarketcap.com/ko/exchanges/upbit/')
    # await get_data('https://upbit.com/exchange?code=CRIX.UPBIT.KRW-AERGO')


if __name__ == '__main__':
    asyncio.run(main())

# <tbody> <tr> data </tr> </tbody>

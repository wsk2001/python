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

    lnk = 'https://www.nanumtrading.com/fx-%EB%B0%B0%EC%9A%B0%EA%B8%B0/%EC%B0%A8%ED%8A%B8-%EB%B3%B4%EC%A1%B0%EC%A7%80%ED%91%9C-%EC%9D%B4%ED%95%B4/02-macd-2/'
    await get_data(lnk)
    # await get_data(pages[0])
    # await get_data('https://coinmarketcap.com/ko/exchanges/upbit/')
    # await get_data('https://upbit.com/exchange?code=CRIX.UPBIT.KRW-AERGO')


if __name__ == '__main__':
    asyncio.run(main())

# <tbody> <tr> data </tr> </tbody>

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
    await get_data('https://upbit.com/trends')
    # await get_data('https://coinmarketcap.com/ko/exchanges/upbit/')
    #await get_data('https://upbit.com/exchange?code=CRIX.UPBIT.KRW-AERGO')

if __name__ == '__main__':
    asyncio.run(main())

# <tbody> <tr> data </tr> </tbody>

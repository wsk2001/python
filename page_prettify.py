from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup as bs
import time
import datetime
import re
 
async def get_data():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://coinness.live/market/future/liquidations')
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
    await get_data()
 
if __name__ == '__main__':
    asyncio.run(main())

# <tbody> <tr> data </tr> </tbody>

from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup as bs
import time
from time import sleep
import datetime


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
        start_flag = False

        for line in lines:
            txt = line.strip()
            if txt.startswith('<'):
                continue
            if txt.startswith('-'):
                continue
            if txt.startswith('출처:'):
                break
            if txt.startswith('롱-숏 비율'):
                start_flag = True
            if start_flag is False:
                continue
            if txt.startswith('거래소'):
                break
            list_str.append(txt)
            #print(txt)

        ct = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #print(list_str[0], list_str[1], list_str[2], list_str[3], list_str[4] )
        print(ct, 'long-short', list_str[2], list_str[3], list_str[4])

async def main():
    lnk = 'https://kimpga.com/statistics/longshort'

    while 1:
        await get_data(lnk)
        sleep(120)

if __name__ == '__main__':
    asyncio.run(main())

# <tbody> <tr> data </tr> </tbody>

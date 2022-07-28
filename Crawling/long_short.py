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
        await page.goto('https://btctools.io/stats/leaderboard')
        time.sleep(6)

        html = await page.content()
        soup = bs(html, 'html.parser').prettify()
        lines = soup.splitlines()

        await browser.close()

        list_str = []
        fflag = False

        for str in lines:
            if fflag == False:
                idx = str.find('<tbody>')
                if 0 < idx:
                    list_str.append(str.strip())
                    fflag = True
                else:
                    continue
            else:
                list_str.append(str.strip())
                idx = str.find('</tbody>')
                if 0 < idx:
                    break

        join_str = ''
        join_cnt = 0
        for str in list_str:
            if str.strip().startswith('<'):
                continue

            join_cnt += 1
            if join_cnt <= 3:
                join_str = join_str + ' ' + str
            if 6 <= join_cnt:
                print(join_str)
                join_str = ''
                join_cnt = 0


async def main():
    await get_data()
 
if __name__ == '__main__':
    asyncio.run(main())

# <tbody> <tr> data </tr> </tbody>

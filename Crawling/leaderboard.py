from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup as bs
import time
import re
 
 
async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://coinness.live/market/ticker')
        time.sleep(6)

        html = await page.content()
        soup = bs(html, 'html.parser').prettify()
        lines = soup.splitlines()

        list_str = []
        fflag = False

        await browser.close()

        for str in lines:
            if fflag == False:
                idx = str.find('<span class="sc-fWPcWZ cOaPDR">')
                if 0 < idx:
                    list_str.append(str)
                    fflag = True
                else:
                    continue
            else:
                list_str.append(str)
                idx = str.find('</span>')
                if 0 < idx:
                    fflag = False

        txt = ''
        list_cnt = []
        for str in list_str:
            if 0 <= str.find('</span>'):
                list_cnt.append(int(txt))
                txt = ''
            
            if str.strip().startswith('<'):
                continue
            else:
                txt += str.strip()
 
        print(list_cnt[0], list_cnt[1])
 
if __name__ == '__main__':
    asyncio.run(main())


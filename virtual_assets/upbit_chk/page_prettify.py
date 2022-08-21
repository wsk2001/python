from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup as bs
import time
import datetime
import re
 
async def get_data(site):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
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

async def cryptoquant_summary():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://cryptoquant.com/ko/asset/btc/summary#overview')
        time.sleep(6)

        html = await page.content()
        soup = bs(html, 'html.parser').prettify()
        lines = soup.splitlines()

        await browser.close()

        list_str = []
        fflag = False

        for line in lines:
            line = line.strip()

            if 0 < len(line):
                if line.startswith('<'):
                    continue

                if line.startswith('(22/'):
                    print()
                    print('크립토퀀트 오늘의 요약', line)
                    print('◈ 주의 ◈')
                    print('데이터를 추출 하는 시점에 따라 값은 달라 질 수 있습니다.')
                    print('크립토퀀트(Basic)는 30분 단위로 값을 갱신 합니다.')
                    print('분석 결과 특히 코인베이스 프리미엄 은 값이 수시로 변합니다.')
                    print()

                if line.startswith('거래소'):
                    fflag = True

                if line.startswith('비트코인(BTC)이란?'):
                    fflag = False
                    continue

                if line.startswith('ⓘ'):
                    continue

                if fflag == True and line.startswith('데이터 분석'):
                    break

                if fflag:
                    if line.startswith('거래소 순출입금양') \
                            or line.startswith('온체인 지표') \
                            or line.startswith('바이너리 CDD') \
                            or line.startswith('SOPR 보정 값') \
                            or line.startswith('투자 심리') \
                            or line.startswith('코인베이스 프리미엄') \
                            or line.startswith('김치 프리미엄') \
                            or line.startswith('선물 시장') \
                            or line.startswith('미체결 약정') \
                            or line.startswith('기술적 분석') \
                            or line.startswith('스토캐스틱') \
                            or (line.startswith('채굴자') and (len(line) == len('채굴자'))):                        print()

                    print(line)


async def main():
    #await get_data('https://upbit.com/trends')
    # await get_data('https://coinmarketcap.com/ko/exchanges/upbit/')
    # await get_data('https://www.tokenpost.kr/blockchain')
    # await get_data('https://cryptoquant.com/ko/asset/btc/summary#overview')
    await cryptoquant_summary()
 
if __name__ == '__main__':
    asyncio.run(main())

# <tbody> <tr> data </tr> </tbody>

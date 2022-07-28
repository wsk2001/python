from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup as bs
import time, datetime
import sys, getopt, signal
from win10toast import ToastNotifier
import numpy as np

position = 'Neutral'
old_posi = 'Neutral'
list_up_count = []

def exit_gracefully(signal, frame):
    sys.exit(0)

def ma5():
    return int(np.average(list_up_count[-5:]))

async def get_data():
    global old_posi
    global position
    global list_up_count

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
 
        old_posi = position
        if 5 <= len(list_up_count):
            ma = ma5()
            if ma < list_cnt[0]:
                position = 'Long'
            elif list_cnt[0] < ma:
                position = 'Short'

        # change of direction
        cur = datetime.datetime.now().strftime('%H:%M:%S')
        print(cur, ' Up:', list_cnt[0], ', Down:', list_cnt[1], ', Direction:', position)
        list_up_count.append(list_cnt[0])

        if old_posi.startswith(position) == False:
            toaster = ToastNotifier()
            toaster.show_toast("Change of direction", old_posi + ' => ' + position)

 
async def main(argv):
    global position
    global list_up_count

    count_min = 1
    unit_min = 60

    list_up_count.clear()

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hs:", ["sleep="])

    except getopt.GetoptError:
        print(argv[0], '-s <sleep mins>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-s <sleep mins>')
            sys.exit()

        elif opt in ("-s", "--sleep"):
            count_min = int(arg.strip())


    while True:
        await get_data()
        time.sleep(count_min * unit_min)
 
if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_gracefully)
    asyncio.run(main(sys.argv))


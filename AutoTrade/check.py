import pyupbit
import time
from datetime import datetime
from pytz import timezone
import telegram
from dotenv import load_dotenv
import os
import pandas as pd

# �ʿ� API KEY load
load_dotenv()
#access = os.getenv('UPBIT_API_ACCESS_KEY')
#secret = os.getenv('UPBIT_API_SECRET_KEY')
access = os.getenv('UPBIT_API_ACCESS_KEY')
secret = os.getenv('UPBIT_API_SECRET_KEY')
upbit = pyupbit.Upbit(access, secret)
df = pd.read_csv('check_dataset.csv')

# �ʿ� ���� �ʱ�ȭ
coin_list = ["KRW-BTC", "KRW-ETH", "KRW-DOGE"]
n = len(coin_list)
prices_prev = [0]*(n)
prices_now = [0]*(n)
prices_high_5 = [0]*(n)
prices_high_15 = [0]*(n)
prices_low_5 = [0]*(n)
prices_low_15 = [0]*(n)
save = True
save_high = True
save_low = True
now = datetime.now(timezone('Asia/Seoul'))
prev_day = now.day

# �����ϸ� �ٷ� ������Ʈ 
# �ּ� ó�� �ϱ�
for i in range(n):
    prices_prev[i] = pyupbit.get_current_price(coin_list[i])
    prices_high_5[i] = prices_prev[i] + prices_prev[i] * 0.05
    prices_high_15[i] = prices_prev[i] + prices_prev[i] * 0.15
    prices_low_5[i] = prices_prev[i] - prices_prev[i] * 0.05
    prices_low_15[i] = prices_prev[i] - prices_prev[i] * 0.15
    
    df.loc[i,'prices_prev'] = prices_prev[i]
    df.loc[i,'prices_low_5'] = prices_low_5[i]
    df.loc[i,'prices_low_15'] = prices_low_15[i]
    df.loc[i,'prices_high_5'] = prices_high_5[i]
    df.loc[i,'prices_high_15'] = prices_high_15[i]
    time.sleep(0.1)
df.to_csv('check_dataset.csv', index=None)

# ���� ������ ������ ����
for i in range(n):
    prices_prev[i] = df.loc[i,'prices_prev']
    prices_high_5[i] = df.loc[i,'prices_high_5']
    prices_high_15[i] = df.loc[i,'prices_high_15']
    prices_low_5[i] = df.loc[i,'prices_low_5']
    prices_low_15[i] = df.loc[i,'prices_low_15']

while True:
    # ���� �ѱ� �ð�
    now = datetime.now(timezone('Asia/Seoul'))
    
    # �� �ð� ����
    msg = f'----------{now.strftime("%Y-%m-%d %H:%M:%S")}----------\n'
    for i in range(n):
        prices_now[i] = pyupbit.get_current_price(coin_list[i])
        msg += f'{"%10s"%coin_list[i]} {prices_now[i]}��\n'
        time.sleep(0.1)
    print(msg)

    # where the magic happens - main code
    for i in range(n):
        if prices_now[i] >= prices_high_5[i]:
            msg = f'{coin_list[i]} {prices_prev[i]}�� -> {prices_now[i]}�� ��. \n5���� �ö��� Ȯ�� �ٶ�\n'
            print(msg)
            bot.sendMessage(mc,msg)
            prices_prev[i] = prices_now[i]
            prices_high_5[i] = prices_now[i] + prices_now[i] * 0.05
            prices_low_5[i] = prices_now[i] - prices_now[i] * 0.05
        if prices_now[i] <= prices_low_5[i]:
            msg = f'@@@{coin_list[i]}@@@ {prices_prev[i]}�� -> {prices_now[i]}�� ��. \n5���� ������ Ȯ�� �ٶ�\n'
            print(msg)
            bot.sendMessage(mc,msg)
            prices_prev[i] = prices_now[i]
            prices_high_5[i] = prices_now[i] + prices_now[i] * 0.05
            prices_low_5[i] = prices_now[i] - prices_now[i] * 0.05
        if prices_now[i] >= prices_high_15[i] and save_high:
            save_high = False
            msg = f'!!!!!!!!!!{coin_list[i]} {prices_now[i]}��\n�ð� ��� 15���γ� �ö���!!!!!!!!!!\n'
            print(msg)
            bot.sendMessage(mc,msg)
        if prices_now[i] <= prices_low_15[i] and save_low:
            save_low = False
            msg = f'!!!!!!!!!!{coin_list[i]} {prices_now[i]}��\n�ð� ��� 15���γ� ��������!!!!!!!!!!\n'
            print(msg)
            bot.sendMessage(mc,msg)
    time.sleep(10) # �ʹ� ���� �� ������ �ȴٰ� �����ؼ� 10�� ������ �߰���
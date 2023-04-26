import pyupbit
import json


g_access = ''
g_secret = ''

def load_key():
    global g_access, g_secret
    with open("C:\\Temp\\ub_api_key.json") as f:
        setting_loaded = json.loads(f.read())

    # Upbit
    g_access = setting_loaded["access_key"]
    g_secret = setting_loaded["secret_key"]


load_key()
upbit = pyupbit.Upbit(g_access, g_secret)

krw = upbit.get_balance("KRW")
krw_btc = upbit.get_balance("KRW-BTC")
print(type(krw))
print(krw_btc)     # KRW-BTC 조회
print(krw)         # 보유 현금 조회

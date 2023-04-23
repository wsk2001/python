import pyupbit

access = "HqYyB1E6hAG8wqBeiquWdKdE8MBB5jzkGFesjvV2"          # 본인 값으로 변경
secret = "8U4AycjBcCuvSlY6kVRcwS39bpsyIDAjvD4O01nl"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-BTC"))     # KRW-BTC 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회
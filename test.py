import pyupbit
import config

access = config.access
secret = config.secret
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-ICX"))     # KRW-ICX 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회

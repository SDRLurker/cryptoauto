import time
import pyupbit
import datetime
import config
import sys
import traceback

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    # target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    target_price = df.iloc[1]['open'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("%s symb k" % sys.argv[0])
        sys.exit(-1)
    symb = sys.argv[1]
    k = float(sys.argv[2])
    cash, crypto = symb.split("-")
    access = config.access
    secret = config.secret
    print("symb = %s" % symb)
    print("k = %.2f" % k)

    # 로그인
    upbit = pyupbit.Upbit(access, secret)
    print("autotrade start")
    first = False

    # 자동매매 시작
    while True:
        try:
            now = datetime.datetime.now()
            start_time = get_start_time(symb)
            end_time = start_time + datetime.timedelta(days=1)

            # 9:00 < 현재 < 8:59:50
            if start_time < now < end_time - datetime.timedelta(seconds=10):
                target_price = get_target_price(symb, k)
                ma15 = get_ma15(symb)
                current_price = get_current_price(symb)
                if not first:
                    print("target_price = %.2f" % target_price)
                    print("ma15 = %.2f" % ma15)
                    print("current_price = %.2f" % current_price)
                    krw = get_balance(cash)
                    btc = get_balance(crypto)
                    print("krw = %.2f" % krw)
                    print("%s = %.2f" % (crypto,btc))
                    value_krw = krw + btc * current_price
                    print("평가금액 = %.2f" % value_krw)
                    first = True
                if target_price < current_price and ma15 < current_price:
                    krw = get_balance(cash)
                    if krw > 5000:
                        upbit.buy_market_order(symb, krw*0.9995)
                        print("buy(%s, %.2f), cur_price=%.2f" % (symb, krw*0.9995, current_price))
            else:
                btc = get_balance(crypto)
                if btc > 0.00008:
                    #upbit.sell_market_order("KRW-BTC", btc*0.9995)
                    upbit.sell_market_order(symb, btc)
                    print("sell(%s, %.2f), cur_price=%.2f" % (symb, btc*0.9995, cur_price))
                    first = False
            time.sleep(1)
        except Exception as e:
            #print(e)
            print(traceback.format_exc())
            time.sleep(1)

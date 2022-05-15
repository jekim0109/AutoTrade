from slacker import Slacker
import pybithumb
import datetime
import time
import requests


myToken = "xoxb-3517032741092-3508065951926-iSymljJBQZ9G1sCbfHH7puiD"

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)

def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    post_message(myToken,"#stock",strbuf)

def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']   
    unit = krw/float(sell_price)
    bithumb.buy_market_order(ticker, unit)
    return unit

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)
    return unit

with open("bithumb.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(key, secret)


now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

target_price = get_target_price("XRP")


while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.timedelta(seconds=10):
            target_price = get_target_price("XRP")
            now = datetime.datetime.now()
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            unit = sell_crypto_currency("XRP")
            dbgout("XRP 매도 : " + str(unit))
        
        current_price = pybithumb.get_current_price("XRP")
        if current_price > target_price:
            unit = buy_crypto_currency("XRP")
            dbgout("XRP 매수 : " + str(unit))

    except:
        dbgout("에러 발생")
        print("에러 발생")
        
    time.sleep(1)




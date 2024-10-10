import Metatrader5 as mt5
import time
from getpass import getpass

account_id = int(input("Enter your Metatrader 5account ID: "))
password = getpass("Enter your Metatrater 5 account password: ")
server = input("Enter your Metatrader 5 server: ")

if not mt5.initilize():
    print("initilize() faled, error code =", mt5.last_error())

    quit()

authorized = mt5.login(account_id, password=password, server=server)

if not authorized:
    print("Failed to connect at account #(), error code: {}".format(account_id, mt5.last_error()))
    mt5.shutdown()
    quit()

print("Connected to account #{}".format(account_id))

def place_order(symbol, order_type, volume, price=None, sl=None, tp=None, deviation=20):
    request = {
        "action": mt5.TEADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script order",
        "type_time": mt5.ORDER_TIME_GTC,                      
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    return result

orders = [
    {
        "symbol": "EURUSD",
        "order_type": mt5.ORDER_TYPE_BUY,
        "volume": 0.1,
    },
    {
        "symbol": "EURUSD",
        "order_type": mt5.ORDER_TYPE_SELL,
        "volume": 0.1,
    },
]

for order in orders:
    result = place_order(**order)
    print("Order result: {result}")
    time.sleep(1)

mt5.shutdown()
from huobi.client.account import AccountClient
from huobi.constant import *

# get accounts
from huobi.utils import *


account_client = AccountClient(api_key="a2dee8fc-vftwcr5tnh-d90e1931-1cb99",
                              secret_key="c0888dd9-f7bbb5a5-759077d0-98370",
                              timeout = 5)


list_obj = account_client.get_balance(213490)
for item in list_obj:
    if item.currency == "btc" or item.currency == "usdt":
        print("==>")
        print(item.currency)
        print(item.type)
        print(item.balance)


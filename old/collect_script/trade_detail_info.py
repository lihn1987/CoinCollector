
class TradeDetailInfo:
    def __init__(self):
        self.dir = 0 #0 buy 1 sell
        self.price=0
        self.amount=0
        self.trade_time=0
    def dumps(self):
        rtn = {}
        rtn["dir"]=self.dir
        rtn["price"]=self.price
        rtn["amount"]=self.amount
        rtn["trade_time"]=self.trade_time
        return rtn
    def dump(self):
        print('==================')
        print("dir:")
        print(self.dir)
        print("price:")
        print(self.price)
        print("amount:")
        print(self.amount)
        print("trade_time:")
        print(self.trade_time)
        

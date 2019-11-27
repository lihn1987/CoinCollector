
class DepthInfo:
    def __init__(self):
        self.up_time = 0
        self.forbuy=[]
        self.forsell=[]
        self.order_coin=''
        self.base_coin=''
        self.market = 0
    def dumps(self):
        rtn = {}
        rtn["up_time"]=self.up_time
        rtn["forbuy"]=self.forbuy
        rtn["forsell"]=self.forsell
        rtn["order_coin"]=self.order_coin
        rtn["base_coin"]=self.base_coin
        rtn["market"]=self.market
        return rtn
    def dump(self):
        print('==================')
        print("order_coin:")
        print(self.order_coin)
        print("base_coin:")
        print(self.base_coin)
        print("time:")
        print(self.up_time)
        print("forbuy:")
        print(self.forbuy)
        print("forsell:")
        print(self.forsell)
        

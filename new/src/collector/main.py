import huobi_info
import ok_info
import coin_info
from multiprocessing import Process

def process(coin_list):
    print(coin_list)
    huobi_info.StartCrwal(coin_list)
    ok_info.StartCrwal(coin_list)

if __name__ == "__main__":
    coin_list = coin_info.get_coin_list()
    print(coin_list)
    print(len(coin_list))
    print("=======")
    #huobi_info.StartCrwal(coin_list)
    #ok_info.StartCrwal(coin_list)
    for i in range(0, len(coin_list), 4):
        #start = i
        #end = i+4 if i+4 < len(coin_list) else len(coin_list) - 1
        #print(start, end)
        p = Process(target=process, args=(coin_list[i: i+4 if i+4 < len(coin_list) else len(coin_list) - 1],))
        p.start() 
        # if i*4+4 < len(coin_list):
        #     p = Process(target=process, args=(coin_list[i*4:i*4+4],))
        #     p.start() 
        # else:
        #     p = Process(target=process, args=(coin_list[i*4:len(coin_list) - 1]),)
        #     p.start() 
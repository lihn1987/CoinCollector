import huobi_info
import ok_info
import coin_info


if __name__ == "__main__":
    coin_list = coin_info.get_coin_list()
    huobi_info.StartCrwal(coin_list)
    ok_info.StartCrwal(coin_list)
import time
import depth_huobi
import depth_ok
import depth_binance
depth_huobi.StartCrwal()
depth_ok.StartCrwal()
depth_binance.StartCrwal()
while True:
    time.sleep(1)
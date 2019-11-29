import time
import depth_huobi
import depth_ok

depth_huobi.StartCrwal()
depth_ok.StartCrwal()
while True:
    time.sleep(1)
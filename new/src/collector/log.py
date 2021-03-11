"""
主要用于封装日志相关
@example:
import log
log.Init("log_name.log")
"""
import sys 
import io 
import os
import time

"""
封装一个类用于替换sys.stdout
"""
class _Logger(object):
    def __init__(self, filename="Default.log", path="./"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        self.terminal = sys.stdout
        self.log = open(os.path.join(path, filename), "a", encoding='utf8')

    def write(self, message):
        if message != "\n":
            self.terminal.write(self.get_local_time() + "=>" + message + "\n")
            self.log.write(self.get_local_time() + "=>" +message + "\n")
            self.terminal.flush()
            self.log.flush()
    
    def get_local_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def flush(self):
        pass
    
"""
初始化整个log模块，使之能用
"""
def init(file_name, path="./"):
    sys.stdout = _Logger(file_name, path=path)
    print("==========================> start")

if __name__=="__main__":
    init("out.log")
    print("test")
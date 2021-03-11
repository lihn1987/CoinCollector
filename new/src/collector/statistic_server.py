from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi
import time
import sys
from socketserver  import ThreadingMixIn
import os
#curl -d '{"login": "emma", "pass": "123"}' -H 'Content-Type: application/json' http://localhost:9939/get_status
host = ('0.0.0.0',9939)
def takeSecond(elem):
    return elem.keys[0]
class TodoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_error(415, 'Only post is supported')

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        rtn = {"result":-1, "data":None}
        print(ctype)
        if ctype == 'application/json':
            path = str(self.path)
            if path == '/get_status':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                length = int(self.headers['content-length'])  # 获取除头部后的请求参数的长度
                data = self.rfile.read(length) # 获取请求参数数据，请求数据为json字符串
                json_data = json.loads(data.decode())

                rtn = {}
                pstream = os.popen("ps -aux |grep huobi")
                lines = pstream.readlines()
                print("lines", lines)
                lines = lines[:-2]
                rtn["data"] = {"main":[], "sub":[]}
                for item in lines:
                    line_items = item.split(" ")
                    line_items = [x for x in line_items if x != '']
                    coin_name = line_items[13].split("=")[1]
                    key = line_items[14][:-1].split("=")[1]
                    rtn["data"][key].append(coin_name)
                
                print(rtn)
                self.wfile.write(json.dumps(rtn).encode()) 
            elif path == '/reset_trade':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                length = int(self.headers['content-length'])  # 获取除头部后的请求参数的长度
                data = self.rfile.read(length) # 获取请求参数数据，请求数据为json字符串
                json_data = json.loads(data.decode())

                coin_name = json_data["coin_name"]
                key = json_data["key"]
                rtn = {}
                #删除掉原进程
                pstream = os.popen("ps -aux |grep '%s --key=%s'"%(coin_name, key))
                lines = pstream.readlines()
                lines = lines[:-2]
                if len(lines) == 1:
                    line_items = lines[0].split(" ")
                    line_items = [x for x in line_items if x != '']
                    os.system("kill -9 %s"%line_items[1])
                #重启进程
                os.system("python3 huobi_contract1.py --cmd=clear --coin={coin} --key={key}".format(coin=coin_name, key=key))
                os.system("python3 huobi_contract1.py --cmd=start --coin={coin} --key={key} &".format(coin=coin_name, key=key))

                rtn = {}
                self.wfile.write(json.dumps(rtn).encode()) 
        else:
            self.send_error(415, "Only json data is supported.")

class ThreadingHttpServer ( ThreadingMixIn, HTTPServer  ):
     pass

def StartHttpServer():
    server = ThreadingHttpServer(host, TodoHandler)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()

if __name__ == "__main__":
    StartHttpServer()
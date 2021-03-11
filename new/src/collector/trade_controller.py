from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi
from socketserver  import ThreadingMixIn

host = ('0.0.0.0',8899)

class TodoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_error(415, 'Only post is supported')

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        rtn = {"result":-1, "data":None}
        print(ctype)
        if ctype == 'application/json':
            path = str(self.path)

            #同步整个mysql数据库的数据项到实时库
            if path == '/api/flush_data_def':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                length = int(self.headers['content-length'])  # 获取除头部后的请求参数的长度
                data = self.rfile.read(length) # 获取请求参数数据，请求数据为json字符串
                json_data = json.loads(data.decode())
                print(json_data)
                #rtn["result"] = process_post.UpdateDataDef(json_data)
                #print(rtn["result"])
                self.wfile.write(json.dumps(rtn).encode())
        else:
            self.send_error(415, "Only json data is supported.")

class ThreadingHttpServer ( ThreadingMixIn, HTTPServer  ):
     pass

def StartHttpServer():
    server = ThreadingHttpServer(host, TodoHandler)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()

if __name__ == '__main__':
    StartHttpServer()

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
import tornado.ioloop
import tornado.web

# @gen.coroutine
# def coroutine_visit():
#     http_client = AsyncHTTPClient()
#     response = yield http_client.fetch("www.baidu.com")
#     print(response.body)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

def main():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
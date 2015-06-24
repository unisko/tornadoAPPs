#!/usr/bin/env python
#coding=utf-8
'''
Created on 2015年6月24日

@author: peng
'''

from tornado import httpserver, ioloop, options, web
from apsw import textwrap
from LSC.widgets import appsview

options.define("port", default=8000, type=int, help=u"在给定的端口上运行")

class ReverseHandler(web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])
        
class WrapHandler(web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))
        
if __name__ == "__main__":
    options.parse_command_line()
    app = web.Application(
                          handlers=[
                                    (r"/reverse/(\w+)", ReverseHandler),
                                    (r"/wrap", WrapHandler)                                    
                                    ]
                          )
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()
        
        
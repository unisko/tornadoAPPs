#!/usr/bin/python2.7
#coding=utf-8
'''
Created on 2015年6月22日

@author: peng
'''

from tornado import ioloop
from tornado import httpserver
import tornado.options
from tornado.options import options, define
from tornado import web

define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', 亲爱的用户！\n')
        
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = web.Application(handlers=[(r"/", IndexHandler)])
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8001, help="在指定端口上运行", type=int)

class BookHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "book.html",
            title = "主页",
            header = "伟大的书籍",
            books = [
                     "Learning Python",
                     "Programming Collective Intelligence",
                     "Restful Web Services"
                     ]        
        )
        

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', BookHandler)]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
#!/usr/bin/env python2.7
# -*-coding: utf-8-*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path

from tornado.options import options, define
define("port", default=8000, help=u"在给定的端口上运行", type=int)


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('hello.html')


class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>你好，世界！</h1>'


class TextModule(tornado.web.UIModule):
    def render(self):
        text = ''
        for i in range(10):
            text = text + "<p>哈哈...</p>"
        return text


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', HelloHandler)],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        ui_modules={
            'Hello': HelloModule,
            'SomeText': TextModule
        }
    )
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

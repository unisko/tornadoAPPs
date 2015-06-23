#!/usr/bin/python2.7
#coding=utf-8
'''
Created on 2015年6月22日

@author: peng
'''

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url

class HelloHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return Application([
        url(r"/", HelloHandler),
        ])

def main():
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()
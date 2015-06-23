#!/usr/bin/python2.7
#coding=utf-8
'''
Created on 2015年6月22日

@author: peng
'''

from tornado import ioloop
from tornado import web

class MainHandler(web.RequestHandler):
    def get(self):
        self.write("你好，世界！")
        
application = web.Application([(r"/", MainHandler), ])

if __name__ == "__main__":
    application.listen(8888)
    ioloop.IOLoop.instance().start()
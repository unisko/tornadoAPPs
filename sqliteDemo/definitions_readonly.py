#!/usr/bin/env python2.7
# -*-coding: utf-8**

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import sqlite3

from tornado.options import define, options
define("port", default=8000, help=u"在给定的端口上运行", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/(\w+)", WordHandler)]
        tornado.web.Application.__init__(self, handlers, debug=True)


class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        conn = sqlite3.connect('example.db')
        cur = conn.cursor()
        sql = "SELECT definition FROM dict WHERE word = '%s'" % word
        cur.execute(sql)
        word_doc = cur.fetchone()[0]
        if word_doc:
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})
        conn.close()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

#!/usr/bin/env python2.7
# -*-coding: utf-8**

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path

import sqlite3

from tornado.options import define, options
define("port", default=8000, help=u"在给定的端口上运行", type=int)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/(\w+)", WordHandler)]
        db_path = os.path.join(BASE_DIR, "example.db")
        self.cur = sqlite3.connect(db_path).cursor()
        tornado.web.Application.__init__(self, handlers, debug=True)


class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        sql = "SELECT definition FROM dict WHERE word = '%s'" % word
        ret = dict()
        ret['word'] = word
        self.application.cur.execute(sql)
        res = self.application.cur.fetchone()
        if res:
            ret['definition'] = res[0]
            self.write(ret)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})
        # self.application.conn.close()

    def post(self, word):
        definition = self.get_argument("definition")
        sql = "SELECT definition FROM dict WHERE word = '%s'" % word
        self.application.cur.execute(sql)
        output = dict()
        output["word"] = word
        output["definition"] = definition
        res = self.application.cur.fetchone()
        if res:
            sql = "UPDATE dict SET definition = '%s' WHERE word = \
                    '%s'" % (definition, word)
            self.application.cur.execute(sql)
        else:
            sql = "INSERT INTO dict VALUES ('%s', '%s')" % (word, definition)
            self.application.cur.execute(sql)
        self.write(output)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

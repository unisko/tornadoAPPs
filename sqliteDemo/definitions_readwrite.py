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


def _execute(query):
    '''用于执行到一个本地sqlite数据库的查询'''
    dbPath = os.path.join(BASE_DIR, 'example.db')
    conn = sqlite3.connect(dbPath)
    cursorobj = conn.cursor()
    try:
        cursorobj.execute(query)
        result = cursorobj.fetchall()
        conn.commit()
    except:
        raise
    conn.close()
    return result


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/(\w+)", WordHandler)]
        tornado.web.Application.__init__(self, handlers, debug=True)


class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        sql = "SELECT definition FROM dict WHERE word = '%s'" % word
        ret = dict()
        ret['word'] = word
        res = _execute(sql)
        if res:
            ret['definition'] = res[0][0]
            self.write(ret)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})
        # self.application.conn.close()

    def post(self, word):
        definition = self.get_argument("definition")
        sql = "SELECT definition FROM dict WHERE word = '%s'" % word
        output = dict()
        output["word"] = word
        output["definition"] = definition
        res = _execute(sql)
        if res:
            sql = "UPDATE dict SET definition = '%s' WHERE word = \
                    '%s'" % (definition, word)
            _execute(sql)
        else:
            sql = "INSERT INTO dict VALUES ('%s', '%s')" % (word, definition)
            _execute(sql)
        self.write(output)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

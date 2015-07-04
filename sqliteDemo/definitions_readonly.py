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


def _dict_factory(cursor, row):
    '''将sqlite 数据库连接的row_factory方法由默认，重写为此方法'''
    d = dict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _execute(query):
    '''用于执行到一个本地sqlite数据库的查询'''
    dbPath = os.path.join(BASE_DIR, 'example.db')
    conn = sqlite3.connect(dbPath)
#  用上面定义的_dict_factory重写conn.row_factory
    conn.row_factory = _dict_factory
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
        res = _execute(sql)
        if res:
            self.write(res[0])
        else:
            self.set_status(404)
            self.write({"error": "word not found"})
        # self.application.conn.close()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

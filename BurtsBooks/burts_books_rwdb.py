#!/usr/bin/env python2.7
# -*-coding: utf-8-*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path
import tornado.auth
import tornado.escape
from tornado.options import define, options
import sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

define("port", default=8000, help="在指定端口上运行", type=int)


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


class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string('modules/book.html', book=book)

    def embedded_javascript(self):
        return "document.write(\"hi!\")"

    def css_files(self):
        return "/static/css/newreleases.css"

    def javascript_files(self):
        return "https://ajax.googleapis.com/ajax/libs/jqueryui/\
                1.8.14/jquery-ui.min.js"

#    def embedded_css(self):
#        return ".book {background-color: #F5F5F5}"

#    def html_body(self):
#        return "<script>document.write(\"你好\")</script>"


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/recommended/", RecommendedHandler),
            (r"/edit/([0-9Xx\-]+)", BookEditHandler),
            (r"/add", BookEditHandler)
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={
                'Book': BookModule,
            },
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
            page_title="Burt's Books | Home",
            header_text="欢迎来到Burt's Books!"
        )


class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        sql = "SELECT * FROM books WHERE 1"
        books = _execute(sql)
        self.render(
            "recommended.html",
            page_title="Burt's Books | 推荐读物",
            header_text="推荐读物",
            books=books
        )


class BookEditHandler(tornado.web.RequestHandler):
    def get(self, isbn=None):
        book = dict()
        if isbn:
            sql = "SELECT * FROM books WHERE isbn = '%s'" % isbn
            book = _execute(sql)[0]
        self.render(
            "book_edit.html",
            page_title="Burt's Books",
            header_text="编辑书籍",
            book=book
        )

    def post(self, isbn=None):
        import time
        book_fields = ['isbn', 'title', 'subtitle', 'images',
                'author', 'date_released', 'description']
        book = dict()
        if isbn:
            sql = "SELECT * FROM books WHERE isbn = '%s'" % isbn
            book = _execute(sql)[0]
        for key in book_fields:
            book[key] = self.get_argument(key, None)

        if isbn:
            sql = "UPDATE books SET isbn = '%s' title = '%s' \
                    subtitle = '%s' images = '%s' author = '%s' \
                    date_released = '%s', description = '%s' WHERE \
                    isbn = ?" % tuple(book[k] for k in book_fields)
            _execute(sql, (isbn, ))
        else:
            book['date_added'] = int(time.time())
            sql = "UPDATE books SET isbn = '%s' title = '%s' \
                subtitle = '%s' images = '%s' author = '%s' \
                date_released = '%s', description = '%s' WHERE \
                isbn = ?" % tuple(book[k] for k in book_fields)
            _execute(sql, (isbn, ))
        self.redirect("/recommended/")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

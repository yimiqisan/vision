#!/usr/bin/env python
# encoding: utf-8
"""
manager.py

Created by 刘 智勇 on 2012-06-13.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options

from vision import config
from urls import handlers


define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, handlers, **config.settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = HTTPServer(Application())
    http_server.listen(options.port)
    loop = IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()

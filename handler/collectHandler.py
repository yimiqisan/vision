#!/usr/bin/env python
# encoding: utf-8
"""
collectHandler.py

Created by 刘 智勇 on 2012-08-13.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from vision.apps.collect import Collect
from vision.apps.perm import addperm
from vision.apps.tools import session


class CollectHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        c = Collect()
        r = c._api.page(page=page, limit=15)
        return self.render("space/collect.html", vlist=r[1], vinfo=r[2])

class CollectItemHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self, id):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        v = Volume()
        r = v._api.page(page=page, limit=15)
        return self.render("space/collect.html", vlist=r[1], vinfo=r[2])

class AjaxCollectAddHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def post(self, rid):
        uid = self.SESSION['uid']
        c = Collect()
        print c._api.save(uid, rid)
        return self.write({})

class AjaxCollectDelHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def post(self, rid):
        uid = self.SESSION['uid']
        v = volume.Volume()
        r = v._api.remove(id)
        return self.redirect('/space/')

class CollectListHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    @addperm
    def get(selfe):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        prop = self.get_argument('prop', None)
        word = self.get_argument('word', None)
        v = volume.Volume()
        r = v._api.page(cuid=uid, owner=uid, perm=self.pm, prop=prop, name=word, subtype=subtype.upper(), page=page)
        return self.render("volume/list.html", vlist=r[1], vinfo=r[2], subtype=subtype)

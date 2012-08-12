#!/usr/bin/env python
# encoding: utf-8
"""
spaceHandler.py

Created by 刘 智勇 on 2012-07-14.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""


from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from vision.apps.staff import Staff
from vision.apps.volume import Volume
from vision.apps.perm import Permission
from vision.apps.tools import session


class SpaceHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        v = Volume()
        r = v._api.page_own(owner=uid, page=page, limit=15)
        return self.render("space/index.html", vlist=r[1], vinfo=r[2])

class SpacePermHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        return self.redirect("/perm/")

class SpaceNewHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        return self.redirect("/volume/new/")

class SpaceCollectHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        v = Volume()
        r = v._api.page(page=page, limit=15)
        return self.render("space/collect.html", vlist=r[1], vinfo=r[2])

class SpaceProjectHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        return self.redirect("/project/")


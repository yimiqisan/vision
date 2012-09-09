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
    '''空间首页
    '''
    @addslash
    @session
    @authenticated
    def get(self):
        perm = self.SESSION['perm']
        if perm[0][0] == 0x01:return self.redirect('/space/perm/')
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        v = Volume()
        r = v._api.page_own(owner=uid, page=page, limit=15)
        return self.render("space/index.html", vlist=r[1], vinfo=r[2], params={})

class SpacePermHandler(BaseHandler):
    '''空间权限首页
    '''
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        return self.redirect("/perm/")

class SpaceNewHandler(BaseHandler):
    '''空间新建页
    '''
    @addslash
    @session
    @authenticated
    def get(self):
        perm = self.SESSION['perm']
        if perm[0][0] == 0x01:return self.redirect('/space/perm/')
        uid = self.SESSION['uid']
        return self.redirect("/volume/new/")

class SpaceCollectHandler(BaseHandler):
    '''空间收藏首页
    '''
    @addslash
    @session
    @authenticated
    def get(self):
        perm = self.SESSION['perm']
        if perm[0][0] == 0x01:return self.redirect('/space/perm/')
        uid = self.SESSION['uid']
        return self.redirect("/collect/")

class SpaceProjectHandler(BaseHandler):
    '''空间项目首页
    '''
    @addslash
    @session
    @authenticated
    def get(self):
        perm = self.SESSION['perm']
        if perm[0][0] == 0x01:return self.redirect('/space/perm/')
        uid = self.SESSION['uid']
        return self.redirect("/project/")


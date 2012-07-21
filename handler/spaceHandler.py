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
        r = v._api.page(page=page, limit=15)
        return self.render("space/index.html", vlist=r[1], vinfo=r[2])

class SpacePermHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        return self.render("space/perm.html")
    
    @addslash
    @session
    @authenticated
    def post(self):
        e= self.get_argument('email', None)
        if e is None:return self.render('space/perm.html', **{'warning': '设置邮箱，可能帮您找回失散多年的密码'})
        n = self.get_argument('nick', None)
        if n is None:return self.render('space/perm.html', **{'warning': '请先报上名号'})
        p = self.get_argument('password', None)
        if p is None:return self.render('space/perm.html', **{'warning': '您接头暗号是？'})
        m = self.get_argument('maintype', None)
        if m is None:return self.render('space/perm.html', **{'warning': '请选择主分类？'})
        s = Staff()
        r = s.register(n, p, email=e)
        if r[0]:
            self._set_perm(r[1])
            self.redirect('/space/perm/')
        else:
            return self.render('space/perm.html', **{'warning': r[1], 'email':e})
    
    def _set_perm(self, uid):
        m = str(self.get_argument('maintype', 'EDITOR'))
        if m == 'MANAGER':
            key = m
        elif m == 'EDITOR':
            s = str(self.get_argument('subtype', 'NORMAL'))
            key = s
        p = Permission()
        p._api.award(uid, u'site', key)


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


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
from vision.apps.perm import Permission
from vision.apps.tools import session


class PermHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        page = self.get_argument('page', 1)
        s = Staff()
        r = s._api.page(page=page)
        if r[0]:
            return self.render("perm/index.html", slist=r[1], sinfo=r[2])

class PermNewHandler(BaseHandler):
    KEYS = ["email", "nick", "password", "perm", "profession", "logo", "male"]
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        d = {'pid':None}
        for n in self.KEYS:d[n] = None
        return self.render("perm/new.html", **d)
    
    @addslash
    @session
    @authenticated
    def post(self):
        uid = self.SESSION['uid']
        pid = self.get_argument('pid', None)
        e= self.get_argument('email', None)
        if e is None:return self.render('perm/new.html', **{'warning': '设置邮箱，可能帮您找回失散多年的密码'})
        n = self.get_argument('nick', None)
        if n is None:return self.render('perm/new.html', **{'warning': '请先报上名号'})
        p = self.get_argument('password', None)
        if p is None:return self.render('perm/new.html', **{'warning': '您接头暗号是？'})
        m = self.get_argument('perm', None)
        if m is None:return self.render('perm/new.html', **{'warning': '请选择主分类'})
        s = Staff()
        if pid:
            ####
            r = p._api.edit(pid, **d)
        else:
            r = r = s.register(n, p, email=e)
            pid = r[1]
        if r[0]:
            self._set_perm(r[1])
            self.redirect('/space/perm/')
        else:
            return self.render('perm/new.html', **{'warning': r[1], 'email':e})
    
    def _set_perm(self, uid):
        m = str(self.get_argument('perm', 'EDITOR'))
        if m == 'MANAGER':
            key = m
        elif m == 'EDITOR':
            s = str(self.get_argument('profession', 'NORMAL'))
            key = s
        p = Permission()
        p._api.award(uid, u'site', key.upper())

class PermEditHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self, sid):
        uid = self.SESSION['uid']
        s = Staff()
        r = s._api.get(sid)
        if r[0]:
            return self.render("project/new.html", **r[1])
        else:
            return self.render_alert(r[1])

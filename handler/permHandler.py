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
    KEY_DICT = {
                "email": "设置邮箱，可能帮您找回失散多年的密码",
                "nick": "请先报上名号",
                "password": "请填写密码",
                "perm": "请选择权限",
                "profession": "请选择职业",
                "logo": "",
                "male": ""
    }
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        d = {'pid':None}
        for n in self.KEY_DICT.keys():d[n] = None
        return self.render("perm/new.html", **d)
    
    @addslash
    @session
    @authenticated
    def post(self):
        uid = self.SESSION['uid']
        pid = self.get_argument('pid', None)
        d = {}
        for k in self.KEY_DICT.keys():
            v = self.get_argument(k, None)
            if (v is None)and(self.KEY_DICT[k]):
                return self.render('perm/new.html', **{'warning': self.KEY_DICT[k]})
            d[k] = v
        s = Staff()
        if pid:
            r = p._api.edit(pid, **d)
        else:
            r = r = s.register(**d)
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

class PermRemoveHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self, id):
        uid = self.SESSION['uid']
        s = Staff()
        s._api.remove(id)
        return self.redirect('/space/perm/')

class PermEditHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self, sid):
        uid = self.SESSION['uid']
        s = Staff()
        r = s._api.get(sid)
        if r[0]:
            print r
            return self.render("perm/new.html", **r[1])
        else:
            return self.render_alert(r[1])

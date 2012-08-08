#!/usr/bin/env python
# encoding: utf-8
"""
spaceHandler.py

Created by 刘 智勇 on 2012-07-14.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from md5 import md5
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
                "male": "",
                "job": "",
                "discribe": ""
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
                d['warning'] = self.KEY_DICT[k]
                d['pid'] = ''
                d.update(map(lambda x: (x,''), self.KEY_DICT.keys()))
                return self.render('perm/new.html', **d)
            d[k] = v.strip() if v is not None else ''
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
            d['warning'] = r[1]
            d['pid'] = ''
            return self.render('perm/new.html', **d)
    
    def _set_perm(self, uid):
        m = str(self.get_argument('perm', 'EDITOR'))
        if m == 'MANAGER':
            key = m
        elif m == 'EDITOR':
            s = self.request.arguments.get('profession', 'NORMAL')
            key = s
        p = Permission()
        for k in key:
            p._api.award(uid, u'site', k.upper())

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
            return self.render("perm/new.html", **r[1])
        else:
            return self.render_alert(r[1])

class PermCpwdHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self, she):
        uid = self.SESSION['uid']
        return self.render("perm/cpwd.html", pid=she)
    
    @addslash
    @session
    @authenticated
    def post(self, she):
        uid = self.SESSION['uid']
        vpwd = self.get_argument('verifypwd', None)
        opwd = self.get_argument('oldpwd', None)
        newpwd = self.get_argument('newpwd', None)
        repwd = self.get_argument('repwd', None)
        if newpwd != repwd:return self.render("perm/cpwd.html", pid=she, warning='重复密码不匹配')
        s = Staff()
        newpwd = unicode(md5(newpwd).hexdigest())
        if vpwd:
            s.whois("_id", uid)
            vpwd = unicode(md5(vpwd).hexdigest())
            if (s.password != vpwd):return self.render('perm/cpwd.html', pid=she, **{'warning': '密码不正确'})
            s._api.change_pwd(she, vpwd, newpwd, repwd)
        if opwd:
            s.whois("_id", she)
            opwd = unicode(md5(opwd).hexdigest())
            if (s.password != opwd):return self.render('perm/cpwd.html', pid=she, **{'warning': '密码不正确'})
            s._api.change_pwd(she, opwd, newpwd, repwd)
        return self.redirect('/space/perm/')
        
        
        
        
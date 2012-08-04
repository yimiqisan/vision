#!/usr/bin/env python
# encoding: utf-8
"""
commonHandler.py

Created by 刘 智勇 on 2012-06-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from vision.config import PERM_CLASS
from vision.apps.staff import Staff
from vision.apps.perm import Permission
from vision.apps.tools import session


class RootHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/space/')
        else:
            self.render("index.html")

class LoginHandler(BaseHandler):
    @addslash
    @session
    def post(self):
        n = self.get_argument('nick', None)
        if n is None:return self.render('login.html', **{'warning': '请先报上名号', 'n':n})
        p = self.get_argument('password', None)
        if p is None:return self.render('login.html', **{'warning': '请输入密码', 'n':n})
        s = Staff()
        r = s.login(n, p)
        if r[0]:
            uid = r[1]['_id']
            e = Permission()
            re = e._api.list(owner=uid, channel=u'site')
            self.SESSION['uid']=uid
            self.SESSION['nick']=n
            self.SESSION['logo']=r[1]['added'].get('logo', None)
            self.SESSION['perm']=re[0].get('value', PERM_CLASS['NORMAL']) if re else PERM_CLASS['SUPEROR']
            self.redirect('/')
        else:
            self.render_alert(r[1])

class LogoutHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self):
        del self.SESSION['uid'], self.SESSION['nick'], self.SESSION['logo'], self.SESSION['perm']
        self.redirect('/')

class Error404Handler(BaseHandler):
    @addslash
    def get(self):
        self.render_alert(u"该页面不存在")

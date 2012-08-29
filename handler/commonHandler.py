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
    '''根目录，即登陆后的首次展示页面
    '''
    def get(self):
        if self.current_user:
            self.redirect('/space/')
        else:
            self.render("index.html")

class LoginHandler(BaseHandler):
    '''登陆处理
    '''
    @addslash
    @session
    def post(self):
        m = self.get_argument('email', None)
        if m is None:return self.render('login.html', **{'warning': '请输入邮箱', 'm':m})
        p = self.get_argument('password', None)
        if p is None:return self.render('login.html', **{'warning': '请输入密码', 'm':m})
        c = self.get_argument('cache', None)
        s = Staff()
        r = s.login(m, p)
        if r[0]:
            uid = r[1]['_id']
            self.SESSION['uid']=uid
            self.SESSION['nick']=r[1]['nick'] if r[1]['nick'] else r[1]['email']
            self.SESSION['ulogo']=r[1].get('avatar', None)
            self.SESSION['perm']=r[1]['pm']
            self.redirect('/')
        else:
            self.render_alert(r[1])

class AjaxLoginHandler(BaseHandler):
    '''ajax方式登陆处理
    '''
    @addslash
    @session
    def post(self):
        m = self.get_argument('email', None)
        if m is None:return self.write(json.dumps({'error':'请输入邮箱'}))
        p = self.get_argument('password', None)
        if p is None:return self.write(json.dumps({'error':'请输入密码'}))
        c = self.get_argument('cache', None)
        s = Staff()
        r = s.login(m, p)
        if r[0]:
            uid = r[1]['_id']
            self.SESSION['uid']=uid
            self.SESSION['nick']=r[1]['nick'] if r[1]['nick'] else r[1]['email']
            self.SESSION['ulogo']=r[1].get('avatar', None)
            self.SESSION['perm']=r[1]['pm']
            self.redirect('/')
        else:
            self.write(json.dumps({'error':r[1]}))

class LogoutHandler(BaseHandler):
    '''退出登陆
    '''
    @addslash
    @session
    @authenticated
    def get(self):
        del self.SESSION['uid'], self.SESSION['nick'], self.SESSION['ulogo'], self.SESSION['perm']
        self.redirect('/')

class Error404Handler(BaseHandler):
    '''404错误页面
    '''
    @addslash
    def get(self):
        self.render_alert(u"该页面不存在")

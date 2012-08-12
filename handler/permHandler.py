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
from vision.config import PERM_CLASS
from vision.apps.staff import Staff
from vision.apps.perm import Permission, addperm
from vision.apps.tools import session


class PermHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        perm = self.SESSION['perm']
        kwargs = {}
        if perm[0][0] == 0x02:kwargs['level'] = u'editor'
        page = self.get_argument('page', 1)
        s = Staff()
        r = s._api.page(page=page, **kwargs)
        if r[0]:
            return self.render("perm/index.html", slist=r[1], sinfo=r[2])

class PermNewHandler(BaseHandler):
    KEY_DICT = {
                "email": "设置邮箱，可能帮您找回失散多年的密码",
                "password": "请填写密码",
                "pm": "请选择权限",
                "profession": "请选择属性",
                "level": "",
                "nick": "",
                "avatar": "",
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
        if d['pm'] is None:d['pm'] = [PERM_CLASS['NORMAL']]
        return self.render("perm/new.html", **d)
    
    @addslash
    @session
    @authenticated
    @addperm
    def post(self):
        uid = self.SESSION['uid']
        pid = self.get_argument('pid', None)
        k_dict = self.KEY_DICT.copy()
        d = {}
        if pid:
            k_dict.pop('email')
            k_dict.pop('password')
            k_dict.pop('pm')
            k_dict.pop('profession')
        if str(self.get_argument('pm', 'EDITOR')) == 'MANAGER':
            k_dict['profession'] = ''
        for k in k_dict.keys():
            v = self.get_argument(k, None)
            if (v is None)and(k_dict[k]):
                if pid:return self.redirect('/perm/'+pid+'/edit/')
                d['warning'] = k_dict[k]
                d['pid'] = ''
                d.update(map(lambda x: (x,''), k_dict.keys()))
                return self.render('perm/new.html', **d)
            d[k] = v.strip() if v is not None else ''
        s = Staff()
        if pid:
            r = s._api.edit(pid, **d)
        else:
            r = r = s.register(**d)
            pid = r[1]
        if r[0]:
            self._set_perm(r[1])
            if self.pm in [0x01, 0x02]:
                self.redirect('/space/perm/')
            else:
                self.redirect('/space/')
        else:
            d['warning'] = r[1]
            d['pid'] = ''
            return self.render('perm/new.html', **d)
    
    def _set_perm(self, uid):
        m = str(self.get_argument('pm', 'EDITOR'))
        if m == 'MANAGER':
            key = m
        elif m == 'EDITOR':
            s = self.request.arguments.get('profession', None)
            key = s
        if key is None:return
        p = Permission()
        p._api.deprive(uid, u'site')
        if isinstance(key, list):
            for k in key:
                p._api.award(uid, u'site', k.upper())
        else:
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
    @addperm
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
        if self.pm in [0x01, 0x02]:
            self.redirect('/space/perm/')
        else:
            self.redirect('/space/')
        
        
        
        
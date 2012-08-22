#!/usr/bin/env python
# encoding: utf-8
"""
spaceHandler.py

Created by 刘 智勇 on 2012-07-14.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from md5 import md5
import json
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
    PARAMS={'email':'设置邮箱，可能帮您找回失散多年的密码',
            'password':'请填写密码',
            'pm':'请选择权限',
            'profession':'请选择属性'
            }
    ARGS = ['level', 'nick', 'avatar', 'male', 'job', 'discribe']
    @addslash
    @session
    @authenticated
    @addperm
    def get(self):
        uid = self.SESSION['uid']
        l = self.PARAMS.keys() + self.ARGS
        d = {'pid':None}
        for n in l:d[n] = None
        d['pm'] = PERM_CLASS['NORMAL']
        return self.render("perm/new.html", **d)
    
    @addslash
    @session
    @authenticated
    @addperm
    def post(self):
        uid = self.SESSION['uid']
        pid = self.get_argument('pid', None)
        if pid:
            r = self._edit(pid)
        else:
            r = self._save()
        if uid == pid:
            s = Staff()
            s.whois('_id', uid)
            self.SESSION['nick']=s.nick if s.nick else s.email
            self.SESSION['ulogo']=s.avatar
        if r[0]:
            self._set_perm(r[1])
            if isinstance(self.pm, list):
                for p in self.pm:
                    if p[0] in [0x01, 0x02]:
                        return self.redirect('/space/perm/')
            elif isinstance(self.pm, tuple):
                if self.pm[0] in [0x01, 0x02]:
                    return self.redirect('/space/perm/')
            return self.redirect('/space/')
        else:
            l = self.PARAMS.keys() + self.ARGS
            d = {'pid':None, 'pm':PERM_CLASS['NORMAL'], 'warning': r[1]}
            for n in l:d[n] = None
            return self.render('perm/new.html', **d)
    
    @session
    def _save(self):
        uid = self.SESSION['uid']
        kwargs = {'belong':uid}
        params = self.PARAMS.copy()
        pm = self.get_argument('pm', None)
        if pm == u'MANAGER':
            kwargs['level'] = u'manager'
            params.pop('profession')
        elif pm == u'EDITOR':
            kwargs['level'] = u'editor'
        else:
            return (False, '请选择权限')
        for k, v in params.items():
            o = self.get_argument(k, None)
            if o:
                kwargs[k]=o
            else:
                return (False, v)
        for k in self.ARGS:
            o = self.get_argument(k, None)
            if o:kwargs[k]=o
        s = Staff()
        return s.register(**kwargs)
    
    @session
    @addperm
    def _edit(self, id):
        uid = self.SESSION['uid']
        l = self.ARGS
        kwargs = {}
        if self.pm[0] in [0x01, 0x02]:l.extend(self.PARAMS.keys())
        for k in l:
            o = self.get_argument(k, None)
            if o:kwargs[k]=o
        pm = self.get_argument('pm', None)
        if pm == u'MANAGER':
            kwargs['level'] = u'manager'
        elif pm == u'EDITOR':
            kwargs['level'] = u'editor'
        s = Staff()
        return s._api.edit(id, **kwargs)
    
    def _set_perm(self, uid):
        pm = self.get_argument('pm', None)
        if pm == u'MANAGER':
            key = pm
        elif pm == u'EDITOR':
            key = self.request.arguments.get('profession', None)
        else:
            s = self.request.arguments.get('profession', None)
            key = s if s else None
        if key is None:return
        p = Permission()
        p._api.deprive(uid, u'site')
        if isinstance(key, list):
            for k in key:
                p._api.award(uid, u'site', k.upper())
        else:
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
            return self.render("perm/new.html", **r[1])
        else:
            return self.render_alert(r[1])

class PermRemoveHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self, id):
        uid = self.SESSION['uid']
        s = Staff()
        s._api.remove(id)
        return self.redirect('/space/perm/')

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
        
class AjaxStaffListHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        s = Staff()
        r = s._api.page()
        l = []
        for i in r[1]:
            if i['pid'] != uid:
                l.append((i['pid'], i['nick']))
        return self.write(json.dumps(l))
    

#!/usr/bin/env python
# encoding: utf-8
"""
spaceHandler.py

Created by 刘 智勇 on 2012-07-14.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from hashlib import md5
import json
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from vision.config import PERM_CLASS
from vision.apps.staff import Staff
from vision.apps.perm import Permission, addperm
from vision.apps.tools import session


class PermHandler(BaseHandler):
    '''权限首页
    '''
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
        kwargs['order_by'] = 'email'
        kwargs['order'] = 1
        r = s._api.page(page=page, **kwargs)
        if r[0]:
            return self.render("perm/index.html", slist=r[1], sinfo=r[2])

class PermNewHandler(BaseHandler):
    '''新建账户
    '''
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
        d['isself'] = False
        return self.render("perm/new.html", **d)
    
    @addslash
    @session
    @authenticated
    @addperm
    def post(self):
        uid = self.SESSION['uid']
        perm = self.SESSION['perm']
        pid = self.get_argument('pid', None)
        if pid:
            r = self._edit(pid)
        else:
            r = self._save()
        if uid == pid:
            s = Staff()
            s.whois('_id', uid)
            self.SESSION['nick']=s.nick if s.nick and '@' not in s.nick else s.email
            self.SESSION['ulogo']=s.avatar
        if r[0]:
            self._set_perm(r[1])
            if (perm[0][0] in [0x01, 0x02]) and (uid != pid):
                self.redirect('/space/perm/')
            else:
                self.redirect('/space/')
        else:
            l = self.PARAMS.keys() + self.ARGS
            d = {'pid':None, 'pm':PERM_CLASS['NORMAL'], 'warning': r[1]}
            for n in l:d[n] = None
            s = Staff()
            rp = s._api.get(pid)
            rp[1]['isself'] = uid == pid
            rp[1]['warning'] = r[1]
            return self.render('perm/new.html', **rp[1])
    
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
        perm = self.SESSION['perm']
        l = self.ARGS
        kwargs = {}
        if self.pm[0] in [0x01, 0x02]:l.extend(self.PARAMS.keys())
        for k in l:
            o = self.get_argument(k, None)
            if o:kwargs[k]=o
        email = self.get_argument('email', None)
        if email:kwargs['email']=email
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
    '''账户编辑
    '''
    @addslash
    @session
    @authenticated
    def get(self, sid):
        uid = self.SESSION['uid']
        s = Staff()
        r = s._api.get(sid)
        if r[0]:
            return self.render("perm/new.html", isself=(sid==uid), **r[1])
        else:
            return self.render_alert(r[1])

class PermRemoveHandler(BaseHandler):
    '''删除账户
    '''
    @addslash
    @session
    @authenticated
    def get(self, id):
        uid = self.SESSION['uid']
        s = Staff()
        s._api.remove(id)
        return self.redirect('/space/perm/')

class PermCpwdHandler(BaseHandler):
    '''修改密码
    '''
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
        perm = self.SESSION['perm']
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
        if (perm[0][0] in [0x01, 0x02]) and (uid != she):
            self.redirect('/space/perm/')
        else:
            self.redirect('/space/')
        
class AjaxStaffListHandler(BaseHandler):
    '''ajax方式获取账户列表
    '''
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        cid = self.get_argument('cid', None)
        p = Permission()
        rp = p._api.list(channel=u'project', cid=cid)
        rlist = [i['owner'] for i in rp]
        s = Staff()
        r = s._api.page(level=u'editor')
        l = []
        for i in r[1]:
            if i['pid'] != uid:
                l.append((i['nick'][0], i['pid'], i['nick'], i['pid'] in rlist))
        l = self.cnsort(l)
        l = [(i[1], i[2], i[3]) for i in l]
        return self.write(json.dumps(l))
    
    def _init_py(self):
        self.dic_py = dict()
        py_f = self.settings.get('static_path')+'/js/py.txt'
        f_py = open(py_f,"r")
        content_py = f_py.read()
        lines_py = content_py.split('\n')
        n=len(lines_py)
        for i in range(0,n-1):
            word_py, mean_py = lines_py[i].split('\t', 1)
            self.dic_py[word_py]=mean_py
        f_py.close()
    
    def cnsort(self, nline):
        self._init_py()
        n = len(nline)
        l = [k[0][0] for k in nline]
        lines="\n".join(l)
        for i in range(1, n):
            tmp = nline[i]
            j = i
            while j > 0 and self.comp_char(nline[j-1][0][0], tmp[0][0]):
                nline[j] = nline[j-1]
                j -= 1
            nline[j] = tmp
        return nline

    def comp_char(self, A, B):
        try:
            charA = A.decode("utf-8")
        except:
            charA = A
        try:
            charB = B.decode("utf-8")
        except:
            charB = B
        n=min(len(charA),len(charB))
        i=0
        while i < n:
            dd=self.comp_char_PY(charA[i],charB[i])
            if dd == -1:
                i=i+1
                if i==n:
                    dd=len(charA)>len(charB)
            else:
                break
        return dd
    
    def comp_char_PY(self, A, B):
        if A==B:
            return -1
        pyA=self.searchdict(self.dic_py,A)
        pyB=self.searchdict(self.dic_py,B)
        if pyA > pyB:
            return 1
        elif pyA < pyB:
            return 0
        else:
            return -1

    def searchdict(self, dic, uchar):
        if isinstance(uchar, str):
            uchar = unicode(uchar,'utf-8')
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            value=dic.get(uchar.encode('utf-8'))
            if value == None:
                value = '*'
        else:
            value = uchar
        return value
    

#!/usr/bin/env python
# encoding: utf-8
"""
spaceHandler.py

Created by 刘 智勇 on 2012-07-14.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from vision.apps.staff import Staff
from vision.apps import volume
from vision.apps.perm import Permission
from vision.apps.tools import session


class SpaceHandler(BaseHandler):
    '''空间首页
    '''
    @addslash
    @session
    @authenticated
    def get(self, subtype):
        perm = self.SESSION['perm']
        self.SESSION['BSTACK'] = ['/space/'+subtype+'/']
        if perm[0][0] == 0x01:return self.redirect('/space/perm/')
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        prop = self.get_argument('prop', None)
        dtime = self.get_argument('dtime', None)
        live = self.get_argument('show_live', None)
        grade = self.get_argument('grade', None)
        nexus = self.get_argument('nexus', None)
        sex = self.get_argument('sex', None)
        period = self.get_argument('period', None)
        period_tuple = period.split('-') if period else None
        word = self.get_argument('word', None)
        href = self.get_argument('href', None)
        if subtype == u'show':
            prop=u'SHOW'
            subtype = ''
        if href:subtype = volume.relation(subtype, href)
        v = volume.Volume()
        r = v._api.page_own(cuid=uid, owner=uid, created=dtime, prop=prop, name=word, subtype=subtype.upper(), live=live, grade=grade, nexus=nexus, male=sex, born_tuple=period_tuple, page=page, limit=15)
        if r[0]:
            params = self._d_params()
            params.pop('page', None)
            return self.render("space/index.html", vlist=r[1], vinfo=r[2], subtype=subtype, params=json.dumps(params), f=params, vurl='/space/'+subtype+'/', vparams=self._build_params(params))
        else:
            return self.render_alert(r[1])
    
    def _d_params(self):
        params = {}
        for k in self.request.arguments.keys():
            params[k] = self.get_argument(k)
        return params
    
    def _build_params(self, params):
        l = []
        for k, v in params.items():
            try:
                s = str(k)+'='+v
            except:
                s = str(k)+'='+str(v)
            l.append(s)
        return '&'.join(l)
    
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


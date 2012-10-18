#!/usr/bin/env python
# encoding: utf-8
"""
volumeHandler.py

Created by 刘 智勇 on 2012-06-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import json
from tornado.web import addslash, authenticated

from vision.config import ADMIN
from baseHandler import BaseHandler
from vision.apps import volume
from vision.apps.item import Item
from vision.apps.perm import addperm
from vision.apps.tools import session

class VolumeNewHandler(BaseHandler):
    '''新建作品集
    '''
    KEYS = ["maintype", "maintype_cn", "prop", "prop_cn", "subtype", "subtype_cn", "logo", "name", "engname", "male", "born", "live", "agency", "website", "grade", "nexus", "intro", "intro_detail", "about", "builder", "post", "market"]
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        d = {}
        for n in self.KEYS:d[n] = None
        d['vid'] = None
        d['born'] = 0
        d['back'] = self.SESSION['BSTACK'][-1]
        return self.render("volume/new.html", **d)
    
    @addslash
    @session
    @authenticated
    def post(self):
        uid = self.SESSION['uid']
        vid = self.get_argument('vid', None)
        d = {}
        for n in self.KEYS:
            d[n] = self.get_argument(n, None)
        v = volume.Volume()
        if vid:
            r = v._api.edit(vid, **d)
        else:
            r = v._api.save(uid, **d)
            vid = r[1]
        if r[0]:
            return self.redirect('/volume/'+vid+'/')
        else:
            d.update({'vid':vid, 'warning':r[1]})
            return self.render("volume/new.html", **d)
        
class VolumeRemoveHandler(BaseHandler):
    '''删除作品集
    '''
    @addslash
    @session
    @authenticated
    def get(self, id):
        uid = self.SESSION['uid']
        v = volume.Volume()
        r = v._api.remove(id)
        return self.redirect(self.SESSION['BSTACK'][0])
    
class VolumeEditHandler(BaseHandler):
    '''编辑作品集
    '''
    @addslash
    @session
    @authenticated
    def get(self, vid):
        uid = self.SESSION['uid']
        v = volume.Volume()
        r = v._api.get(vid)
        if r[0]:
            return self.render("volume/new.html", back=self.SESSION['BSTACK'][0], **r[1])
        else:
            return self.render_alert(r[1])

class VolumeHandler(BaseHandler):
    '''单个作品集展示
    '''
    @addslash
    @session
    @authenticated
    def get(self, vid):
        uid = self.SESSION['uid']
        url = '/volume/'+vid+'/'
        if url not in self.SESSION['BSTACK']:
            bstack = self.SESSION['BSTACK']
            bstack.append(url)
            self.SESSION['BSTACK'] = bstack
        v = volume.Volume()
        r = v._api.get(vid)
        if r[0]:
            page = int(self.get_argument('page', 1))
            i = Item()
            ri = i._api.page(page=page, vid=vid)
            return self.render("volume/item.html", back=self.SESSION['BSTACK'][0], wlist=ri[1], winfo=ri[2], **r[1])
        else:
            return self.render_alert(r[1])

class VolumeListHandler(BaseHandler):
    '''作品集列表
    '''
    @addslash
    @session
    @authenticated
    @addperm
    def get(self, subtype):
        uid = self.SESSION['uid']
        self.SESSION['BSTACK'] = ['/volume/'+subtype+'/'] if subtype else ['/volume/']
        if ADMIN['admin'][-1] == uid:
            self.redirect('/perm/')
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
        r = v._api.page(cuid=uid, owner=uid, perm=self.pm, created=dtime, prop=prop, name=word, subtype=subtype.upper(), live=live, grade=grade, nexus=nexus, male=sex, born_tuple=period_tuple, page=page)
        if r[0]:
            params = self._d_params()
            return self.render("volume/list.html", vlist=r[1], vinfo=r[2], subtype=subtype, params=json.dumps(params), f=params, vurl='/volume/'+subtype+'/', vparams=self._build_params(params))
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
    
    
class AjaxVolumeTypeHandler(BaseHandler):
    '''ajax方式加载作品集分类
    '''
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        kind = self.get_argument('kind', None)
        if kind == u'maintype':
            options = volume.VOL_TYPES_MAIN[:-1]
        elif kind == u'property':
            options = volume.VOL_PROPERTY_MAIN
        elif kind == u'subtype':
            t = self.get_argument('maintype', None)
            p = self.get_argument('property', None)
            options = volume.get_sub(t, p)
        else:
            options = {}
        return self.write(json.dumps(options))

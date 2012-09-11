#!/usr/bin/env python
# encoding: utf-8
"""
collectHandler.py

Created by 刘 智勇 on 2012-08-13.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from vision.apps.collect import Collect
from vision.apps.volume import Volume
from vision.apps.item import Item
from vision.apps.perm import addperm
from vision.apps.tools import session


class CollectHandler(BaseHandler):
    '''收藏首页
    '''
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        dtime = self.get_argument('dtime', None)
        live = self.get_argument('show_live', None)
        grade = self.get_argument('grade', None)
        nexus = self.get_argument('nexus', None)
        sex = self.get_argument('sex', None)
        period = self.get_argument('period', None)
        period_tuple = period.split('-') if period else None
        word = self.get_argument('word', None)        
        v = Volume()
        r = v._api.page_own(cuid=uid, atte=uid, created=dtime, prop=prop, name=word, subtype=subtype.upper(), live=live, grade=grade, nexus=nexus, male=sex, born_tuple=period_tuple, page=page, limit=15)
#        c = Collect()
#        r = c._api.page(owner=uid, page=page, limit=15)
        if r[0]:
            params = self._d_params()
            return self.render("space/collect.html", vlist=r[1], vinfo=r[2], params=params)
        else:
            return self.render_alert(r[1])
    
    def _d_params(self, params={'abc':123}):
        return params


class CollectRemoveHandler(BaseHandler):
    '''取消收藏
    '''
    @addslash
    @session
    @authenticated
    def get(self, id):
        uid = self.SESSION['uid']
        v = Volume()
        r = v._api.forget(id, uid)
#        c = Collect()
#        r = c._api.remove(id)
        return self.redirect('/collect/')

class CollectItemHandler(BaseHandler):
    '''收藏单项展示
    '''
    @addslash
    @session
    @authenticated
    def get(self, cid):
        uid = self.SESSION['uid']
#        c = Collect()
#        r = c._api.get(cid)
        v = Volume()
        r = v._api.get(cid)
        if r[0]:
            page = int(self.get_argument('page', 1))
            i = Item()
            ri = i._api.page(page=page, vid=r[1]['vid'])
            return self.render("collect/item.html", wlist=ri[1], winfo=ri[2], **r[1])
        else:
            return self.render_alert(r[1])

class AjaxCollectAddHandler(BaseHandler):
    '''ajax方式添加收藏
    '''
    @addslash
    @session
    @authenticated
    def post(self, rid):
        uid = self.SESSION['uid']
        v = Volume()
        r = v._api.attention(rid, uid)
#        c = Collect()
#        r = c._api.save(uid, rid)
        return self.write({})

class AjaxCollectDelHandler(BaseHandler):
    '''ajax方式取消收藏
    '''
    @addslash
    @session
    @authenticated
    def post(self, rid):
        uid = self.SESSION['uid']
        v = volume.Volume()
        r = v._api.remove(id)
        return self.redirect('/space/')

class CollectListHandler(BaseHandler):
    '''收藏列表
    '''
    @addslash
    @session
    @authenticated
    @addperm
    def get(selfe):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        prop = self.get_argument('prop', None)
        word = self.get_argument('word', None)
        v = volume.Volume()
        r = v._api.page(cuid=uid, owner=uid, perm=self.pm, prop=prop, name=word, subtype=subtype.upper(), page=page)
        return self.render("volume/list.html", vlist=r[1], vinfo=r[2], subtype=subtype)



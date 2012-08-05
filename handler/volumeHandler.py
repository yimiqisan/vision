#!/usr/bin/env python
# encoding: utf-8
"""
volumeHandler.py

Created by 刘 智勇 on 2012-06-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from vision.apps import volume
from vision.apps.item import Item
from vision.apps.perm import addperm
from vision.apps.tools import session

class VolumeNewHandler(BaseHandler):
    KEYS = ["maintype", "maintype_cn", "prop", "prop_cn", "subtype", "subtype_cn", "logo", "name", "male", "year", "live", "agency", "website", "grade", "nexus", "intro", "about"]
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        d = {}
        for n in self.KEYS:d[n] = None
        d['vid'] = None
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
            d.update({'vid':vid, warning:r[1]})
            return self.render("volume/new.html", **d)

class VolumeRemoveHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self, id):
        uid = self.SESSION['uid']
        v = volume.Volume()
        r = v._api.remove(id)
        return self.redirect('/space/')

class VolumeEditHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self, vid):
        uid = self.SESSION['uid']
        v = volume.Volume()
        r = v._api.get(vid)
        if r[0]:
            return self.render("volume/new.html", **r[1])
        else:
            return self.render_alert(r[1])

class VolumeHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self, vid):
        uid = self.SESSION['uid']
        v = volume.Volume()
        r = v._api.get(vid)
        if r[0]:
            page = int(self.get_argument('page', 1))
            i = Item()
            ri = i._api.page(page=page, vid=vid)
            return self.render("volume/item.html", wlist=ri[1], winfo=ri[2], **r[1])
        else:
            return self.render_alert(r[1])

class VolumeListHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    @addperm
    def get(self, subtype):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        prop = self.get_argument('prop', None)
        word = self.get_argument('word', None)
        v = volume.Volume()
        r = v._api.page(cuid=uid, owner=uid, perm=self.pm, prop=prop, name=word, subtype=subtype.upper(), page=page)
        return self.render("volume/list.html", vlist=r[1], vinfo=r[2], subtype=subtype)

class AjaxVolumeTypeHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        kind = self.get_argument('kind', None)
        if kind == u'maintype':
            options = volume.VOL_TYPES_MAIN
        elif kind == u'property':
            options = volume.VOL_PROPERTY_MAIN
        elif kind == u'subtype':
            t = self.get_argument('maintype', None)
            p = self.get_argument('property', None)
            options = volume.get_sub(t, p)
        else:
            options = {}
        return self.write(json.dumps(options))




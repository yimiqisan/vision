#!/usr/bin/env python
# encoding: utf-8
"""
itemHandler.py

Created by 刘 智勇 on 2012-07-15.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import json

from tornado.web import addslash

from baseHandler import BaseHandler
from vision.apps.project import Project
from vision.apps.volume import Volume
from vision.apps.item import Item, VTYPE_LIST
from vision.apps.tools import session


class ItemNewHandler(BaseHandler):
    @addslash
    @session
    def get(self, tp, vid):
        uid = self.SESSION['uid']
        tp = tp.lower()
        if tp in VTYPE_LIST:
            html = "item/new_"+tp+".html"
            return self.render(html, vid=vid, vtype=tp, eid='')
        return self.render_alert("url error")
    
    @addslash
    @session
    def post(self, tp, vid):
        print vid
        uid = self.SESSION['uid']
        eid = self.get_argument('eid', None)
        logo, works = self.get_works_list()
        infos = self.get_info_dict(tp)
        e = Item()
        if not eid:
            r = e._api.save(uid, vid, tp, logo, *works, **infos)
        else:
            r = e._api.edit(eid, logo=logo, works=works, **infos)
        if r[0]:
            return self.redirect('/item/'+r[1]+'/')
        infos.update({'warning':r[1], 'vid':vid, 'eid':'', 'vtype':tp})
        return self.render("item/new_"+tp+".html", **infos)
    
    def get_works_list(self):
        c = int(self.get_argument('cover', 1))
        l = []
        i=1
        while(True):
            p, e = self.get_argument(str(i)+'PIC', None), self.get_argument(str(i)+'Edit', None)
            if not p or not e:break
            l.insert(0, (p, e))
            if c == i:logo=p
            i+=1
        return (logo, l)
    
    def get_info_dict(self, tp):
        tp = tp.lower()
        if tp == VTYPE_LIST[0]:
            ikeys = ["name", "client", "year"]
        elif tp == VTYPE_LIST[1]:
            ikeys = [""]
        else:
            ikeys = []
        d = {}
        for n in ikeys:d[n] = self.get_argument(n, None)
        return d

class ItemRemoveHandler(BaseHandler):
    @addslash
    @session
    def get(self, id):
        uid = self.SESSION['uid']
        e = Item()
        r = e._api.remove(id)
        if r[0]:
            return self.self.redirect('/'+r[1]+'/'+r[2]+'/')
        return self.render_alert(r[1])

class ItemEditHandler(BaseHandler):
    @addslash
    @session
    def get(self, id):
        uid = self.SESSION['uid']
        e = Item()
        r = e._api.get(id)
        
        print r[1]
        
        if r[0] and r[1]:
            tp = r[1]['vtype']
            if tp in VTYPE_LIST:
                html = "item/new_"+tp+".html"
                return self.render(html, **r[1])
        return self.render_alert(r[1])

class ItemHandler(BaseHandler):
    @addslash
    @session
    def get(self, eid):
        uid = self.SESSION['uid']
        e = Item()
        r = e._api.get(eid)
        if r[0]:
            vid, vtype = r[1]['vid'], r[1]['vtype']
            if vtype == u'project':
                p = Project()
                rv = p._api.get(vid)
                html = "item/project.html"
            else:
                v =  Volume()
                rv = v._api.get(vid)
                html = "item/index.html"
            vinfo = rv[1] if rv[0] and rv[1] else {}
            return self.render(html, vinfo=vinfo, **r[1])
        else:
            return self.render_alert(r[1])

class AjaxItemHandler(BaseHandler):
    @addslash
    @session
    def get(self, eid):
        uid = self.SESSION['uid']
        e = Item()
        r = e._api.get(eid)
        if r[0]:
            return self.write(json.dumps(r[1]['works']))





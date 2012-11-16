#!/usr/bin/env python
# encoding: utf-8
"""
itemHandler.py

Created by 刘 智勇 on 2012-07-15.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import json

from tornado.web import addslash, authenticated

from vision.config import BSTACK
from baseHandler import BaseHandler
from vision.apps.project import Project
from vision.apps.volume import Volume
from vision.apps.item import Item, VTYPE_LIST
from vision.apps.tools import session


class ItemNewHandler(BaseHandler):
    '''新建作品
    '''
    @addslash
    @session
    @authenticated
    def get(self, tp, vid):
        uid = self.SESSION['uid']
        tp = tp.lower()
        if tp in VTYPE_LIST:
            html = "item/new_"+tp+".html"
            return self.render(html, vid=vid, vtype=tp, eid='', name='', client='', title='', content='', year='')
        return self.render_alert("url error")
    
    @addslash
    @session
    @authenticated
    def post(self, tp, vid):
        uid = self.SESSION['uid']
        eid = self.get_argument('eid', None)
        logo, works = self.get_works_list()
        infos = self.get_info_dict(tp)
        e = Item()
        if not eid:
            r = e._api.save(uid, vid, tp, logo, *works, **infos)
            p = Project()
            rp = p._api.get(vid)
            l = rp[1]['works'].append(r[1])
            p._api.edit(vid, works=l, isOverWrite=True)
        else:
            r = e._api.edit(eid, logo=logo, works=works, **infos)
        if r[0]:
            return self.redirect('/item/'+r[1]+'/')
        infos.update({'warning':r[1], 'vid':vid, 'eid':'', 'vtype':tp})
        return self.render("item/new_"+tp+".html", **infos)
    
    def get_works_list(self):
        c = int(self.get_argument('cover', 1))
        logo, l = None, []
        i=1
        while(True):
            p, e = self.get_argument(str(i)+'PIC', None), self.get_argument(str(i)+'Edit', '')
            if not p:break
            l.append((p, e))
            if c == i:logo=p
            i+=1
        return (logo, l)
    
    def get_info_dict(self, tp):
        tp = tp.lower()
        if tp == VTYPE_LIST[0]:
            ikeys = ["name", "client", "year"]
        elif tp == VTYPE_LIST[1]:
            ikeys = ["title", "content"]
        elif tp == VTYPE_LIST[2]:
            ikeys = ["title", "content"]
        else:
            ikeys = []
        d = {}
        for n in ikeys:d[n] = self.get_argument(n, None)
        return d

class ItemPreviewHandler(BaseHandler):
    '''作品预览
    '''
    @addslash
    @session
    @authenticated
    def post(self, tp, vid):
        uid = self.SESSION['uid']
        eid = self.get_argument('eid', None)
        logo, works = self.get_works_list()
        infos = self.get_info_dict(tp)
        if tp == u'project':
            p = Project()
            rv = p._api.get(vid)
            html = "item/project.html"
        else:
            v =  Volume()
            rv = v._api.get(vid)
            html = "item/index.html"
        vinfo = rv[1] if rv[0] and rv[1] else {}
        vdict = {'vid':vid, 'vtype':tp, 'eid':'', 'name':'', 'client':'', 'created':'', 'nick':'', 'title':'', 'content':'', 'year':'', 'works':works, 'isPreview': True, 'back':'/item/'+eid+'/edit/' if eid else self.SESSION['BSTACK'][-1]}
        vdict.update(infos)
        return self.render(html, vinfo=vinfo, **vdict)
    
    def get_works_list(self):
        c = int(self.get_argument('cover', 1))
        logo, l = None, []
        i=1
        while(True):
            p, e = self.get_argument(str(i)+'PIC', None), self.get_argument(str(i)+'Edit', '')
            if not p:break
            l.append((p, e))
            if c == i:logo=p
            i+=1
        return (logo, l)
    
    def get_info_dict(self, tp):
        tp = tp.lower()
        if tp == VTYPE_LIST[0]:
            ikeys = ["name", "client", "year"]
        elif tp == VTYPE_LIST[1]:
            ikeys = ["title", "content"]
        elif tp == VTYPE_LIST[2]:
            ikeys = ["title", "content"]
        else:
            ikeys = []
        d = {}
        for n in ikeys:d[n] = self.get_argument(n, None)
        return d

class ItemRemoveHandler(BaseHandler):
    '''作品删除
    '''
    @addslash
    @session
    @authenticated
    def get(self, id):
        uid = self.SESSION['uid']
        refer = self.get_argument('refer', None)
        e = Item()
        r = e._api.remove(id)
        if refer:
            return self.redirect(refer)
        if r[0]:
            return self.redirect('/volume/'+r[2]+'/')
        return self.render_alert(r[1])

class ItemEditHandler(BaseHandler):
    '''作品编辑
    '''
    @addslash
    @session
    @authenticated
    def get(self, id):
        uid = self.SESSION['uid']
        e = Item()
        r = e._api.get(id)
        if r[0] and r[1]:
            tp = r[1]['vtype']
            if tp in VTYPE_LIST:
                html = "item/new_"+tp+".html"
                return self.render(html, **r[1])
        return self.render_alert(r[1])

class ItemHandler(BaseHandler):
    '''单个作品展示
    '''
    @addslash
    @session
    @authenticated
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
            r[1].update({'isPreview': False})
            vdict = r[1]
            return self.render(html, back=self.SESSION['BSTACK'].pop(), vinfo=vinfo, **vdict)
        else:
            return self.render_alert(r[1])

class AjaxItemHandler(BaseHandler):
    '''ajax方式展示单个作品
    '''
    @addslash
    @session
    @authenticated
    def get(self, eid):
        uid = self.SESSION['uid']
        e = Item()
        r = e._api.get(eid)
        if r[0]:
            return self.write(json.dumps({'works': r[1]['works'], 'logo':r[1]['logo']}))

class AjaxItemPasteHandler(BaseHandler):
    '''ajax方式粘贴作品
    '''
    @addslash
    @session
    @authenticated
    def post(self, eid):
        uid = self.SESSION['uid']
        vid = self.get_argument('vid', None)
        e = Item()
        r = e._api.copy(eid, **{'vid':vid, 'vtype':u'project'})
        p = Project()
        rp = p._api.get(vid)
        l = rp[1]['works']
        if isinstance(l, list):
            l.append(r[1]) 
        else:
            l = [r[1]]
        p._api.edit(vid, works=l, isOverWrite=True)
        if r[0]:return self.write(json.dumps({'rep':'ok'}))



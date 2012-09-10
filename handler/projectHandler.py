#!/usr/bin/env python
# encoding: utf-8
"""
projectHandler.py

Created by 刘 智勇 on 2012-06-13.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""


from tornado.web import addslash, authenticated

from config import PERM_CLASS
from baseHandler import BaseHandler
from vision.apps.project import Project
from vision.apps.perm import Permission
from vision.apps.item import Item
from vision.apps.collect import Collect
from vision.apps.volume import Volume
from vision.apps.reply import Reply
from vision.apps.tools import session


class ProjectNewHandler(BaseHandler):
    '''新建项目
    '''
    KEYS = ["title", "description"]
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        d = {'pid':None}
        for n in self.KEYS:d[n] = None
        return self.render("project/new.html", **d)
    
    @addslash
    @session
    @authenticated
    def post(self):
        uid = self.SESSION['uid']
        pid = self.get_argument('pid', None)
        d = {}
        for n in self.KEYS:
            d[n] = self.get_argument(n, None)
        p = Project()
        d['members'] = self.request.arguments.get('members', [])
        if pid:
            r = p._api.edit(pid, **d)
        else:
            r = p._api.save(uid, **d)
            pid = r[1]
        if r[0]:
            self._set_perm(pid)
            return self.redirect('/project/'+pid+'/')
        else:
            d.update({'pid':'', 'warning':r[1]})
            return self.render("project/new.html", **d)
    
    @session
    def _set_perm(self, pid):
        uid = self.SESSION['uid']
        members = self.request.arguments.get('members', [])
        p = Permission()
        p._api.deprive(uid, u'project', cid=pid)
        p._api.award(uid, u'project', 'PROJECTOR', cid=pid)
        p._api.deprive(channel=u'project', value='RELATION', cid=pid)
        for member in members:
            p._api.award(unicode(member), u'project', 'RELATION', cid=pid)

class ProjectRemoveHandler(BaseHandler):
    '''删除项目
    '''
    @addslash
    @session
    @authenticated
    def get(self, pid):
        uid = self.SESSION['uid']
        p = Project()
        r = p._api.remove(pid)
        return self.redirect("/space/project/")

class ProjectEditHandler(BaseHandler):
    '''编辑项目
    '''
    @addslash
    @session
    @authenticated
    def get(self, pid):
        uid = self.SESSION['uid']
        p = Project()
        r = p._api.get(pid, cuid=uid)
        if r[0]:
            proj = r[1]
            m = Permission()
            rp = m._api.list(channel=u'project', cid=pid)
            proj['members'] = rp
            return self.render("project/new.html", **proj)
        else:
            return self.render_alert(r[1])

class ProjectBuildHandler(BaseHandler):
    '''新建作品列表
    '''
    @addslash
    @session
    @authenticated
    def get(self, pid):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        i = Item()
        ro = i._api.page(vid=pid, vtype=u'project')
        olist = [o['refer_id'] for o in ro[1]]
        v = Volume()
        r = v._api.page_own(owner=uid, page=page)
        ilist = []
        for vi in r[1]:
            ri = i._api.page(vid=vi['vid'])
            for j in ri[1]:
                j['is_paste'] = j['eid'] in olist
            ilist.extend(ri[1])
        if r[0]:
            return self.render("project/build.html", ilist=ilist, pid=pid)
        else:
            return self.render_alert(r[1])

class ProjectStickHandler(BaseHandler):
    '''收藏作品列表
    '''
    @addslash
    @session
    @authenticated
    def get(self, pid):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        i = Item()
        ro = i._api.page(vid=pid, vtype=u'project')
        olist = [o['refer_id'] for o in ro[1]]
        c = Collect()
        r = c._api.page(owner=uid, page=page)
        ilist = []
        for ci in r[1]:
            rid = ci['refer_id']
            ri = i._api.page(vid=rid)
            for j in ri[1]:
                j['is_paste'] = j['eid'] in olist
            ilist.extend(ri[1])
        if r[0]:
            return self.render("project/stick.html", ilist=ilist, pid=pid)
        else:
            return self.render_alert(r[1])

class ProjectHandler(BaseHandler):
    '''项目首页
    '''
    @addslash
    @session
    @authenticated
    def get(self, pid):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        p = Project()
        r = p._api.page(cuid=uid)
        if r[0]:
            plist = self._f_proj(r[1])
            if not pid:pid = plist[0]['pid'] if len(plist)>0 else None
            rp = p._api.get(pid, cuid=uid)
            if rp[0]: project=rp[1]
            e = Item()
            re = e._api.page(vid=pid, page=page, limit=20)
            works= re[1] if re[0] and re[1] and pid else []
            return self.render("space/project.html", plist=plist, pinfo=re[2], works=works, project=project, pid=pid if pid else '', rl=[])
        else:
            return self.render_alert(r[1])
    
    @session
    def _f_proj(self, plist):
        perm = self.SESSION['perm']
        rlist = []
        for p in plist:
            flag = False
            for m in p['pm']:
                if m[0] in [0x20, 0x21]:
                    flag = True
            for m in perm:
                if m == PERM_CLASS['MANAGER']:
                    flag = True
            if flag:rlist.append(p)
        return rlist




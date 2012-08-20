#!/usr/bin/env python
# encoding: utf-8
"""
projectHandler.py

Created by 刘 智勇 on 2012-06-13.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""


from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from vision.apps.project import Project
from vision.apps.perm import Permission
from vision.apps.item import Item
from vision.apps.reply import Reply
from vision.apps.tools import session


class ProjectNewHandler(BaseHandler):
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
        for member in members:
            p._api.deprive(unicode(member), u'project', cid=pid)
            p._api.award(unicode(member), u'project', 'RELATION', cid=pid)

class ProjectRemoveHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self, pid):
        uid = self.SESSION['uid']
        p = Project()
        r = p._api.remove(pid)
        return self.redirect("/space/project/")

class ProjectEditHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self, pid):
        uid = self.SESSION['uid']
        p = Project()
        r = p._api.get(pid)
        if r[0]:
            return self.render("project/new.html", **r[1])
        else:
            return self.render_alert(r[1])

class ProjectHandler(BaseHandler):
    @addslash
    @session
    @authenticated
    def get(self, pid):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        p = Project()
        r = p._api.page()
        if r[0]:
            if not pid:pid = r[1][0]['pid'] if len(r[1])>0 else None
            rp = p._api.get(pid)
            if rp[0]: project=rp[1]
            e = Item()
            re = e._api.page(vid=pid, page=page, limit=20)
            works= re[1] if re[0] and re[1] and pid else []
            return self.render("space/project.html", plist=r[1], pinfo=re[2], works=works, project=project, pid=pid if pid else '', rl=[])
        else:
            return self.render_alert(r[1])







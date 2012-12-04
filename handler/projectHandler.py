#!/usr/bin/env python
# encoding: utf-8
"""
projectHandler.py

Created by 刘 智勇 on 2012-06-13.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""


from tornado.web import addslash, authenticated

from config import PERM_CLASS, ADMIN
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
        url = self.request.uri
        if url not in self.SESSION['BSTACK']:
            bstack = self.SESSION['BSTACK']
            bstack.append(url)
            self.SESSION['BSTACK'] = bstack
        d = {'pid':None}
        for n in self.KEYS:d[n] = None
        d['back'] = self.SESSION['BSTACK'][0]
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

class ProjectListHandler(BaseHandler):
    '''项目列表
    '''
    @addslash
    @session
    @authenticated
    def get(self):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        p = Project()
        r = p._api.page(cuid=uid, limit=10000)
        plist = self._flt_month(r[1])
        limit = 20
        return self.render("project/list.html", pinfo= self.page_info(page, 5, len(plist), limit), plist=plist[(page-1)*limit:page*limit])
    
    @session
    def _flt_month(self, plist):
        perm = self.SESSION['perm']
        l = []
        oy, om = ('', '')
        for p in plist:
            ny, nm = p['time_meta'].year, p['time_meta'].month
            if (oy != ny) or (om != nm):
                oy, om = ny, nm
                l.append({'pid':'','title':'','nick':'','created':str(oy)+u'年'+str(om)+u'月'})
            flag = False
            for m in p['pm']:
                if m[0] in [0x20, 0x21]:
                    flag = True
            for m in perm:
                if m == PERM_CLASS['MANAGER']:
                    flag = True
            if flag:l.append({'pid':p['pid'],'title':p['title'],'nick':p['nick'],'created':p['created']})
        return l

class ProjectSortHandler(BaseHandler):
    @session
    def get(self, pid):
        uid = self.SESSION['uid']
        url = '/project/'+pid+'/sort/'
        if url not in self.SESSION['BSTACK']:
            bstack = self.SESSION['BSTACK']
            bstack.append(url)
            self.SESSION['BSTACK'] = bstack
        page = int(self.get_argument('page', 1))
        p = Project()
        r = p._api.page(cuid=uid, limit=10000)
        if r[0]:
            plist = r[1]
            if not pid:pid = plist[0]['pid'] if len(plist)>0 else None
            rp = p._api.get(pid, cuid=uid)
            project = rp[1]
            e = Item()
            works = []
            for w in project['works']:
                if not w:continue
                rw = e._api.get(w)
                if rw[0] and rw[1]:
                    works.append(rw[1])
            return self.render("project/sort.html", pinfo=self.page_info(page, 5, len(works), 15), wlist=works, pid=pid if pid else '', back=self.SESSION['BSTACK'][0])
    
    @session
    def post(self, pid):
        uid = self.SESSION['uid']
        i = 1
        l = []
        item = self.get_argument('sort-'+str(i), None)
        while(item):
            l.append(item)
            i+=1
            item = self.get_argument('sort-'+str(i), None)
        p = Project()
        r = p._api.edit(pid, works=l, isOverWrite=True)
        if r[0]:
            return self.redirect('/project/'+pid+'/sort/')
        else:
            return self.render_alert(r[1])

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
            rp = m._api.page(channel=u'project', cid=pid, limit=1000)
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
        url = self.request.uri#'/project/'+pid+'/build/'
        if url not in self.SESSION['BSTACK']:
            bstack = self.SESSION['BSTACK']
            bstack.append(url)
            self.SESSION['BSTACK'] = bstack
        page = int(self.get_argument('page', 1))
        v = Volume()
        r = v._api.page_own(cuid=uid, owner=uid, page=page, limit=20)
        if r[0]:
            return self.render("project/build.html", vlist=r[1], vinfo=r[2], vurl='/project/'+pid+'/build/', pid=pid, back=self.SESSION['BSTACK'][0])
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
        url = self.request.uri#'/project/'+pid+'/stick/'
        if url not in self.SESSION['BSTACK']:
            bstack = self.SESSION['BSTACK']
            bstack.append(url)
            self.SESSION['BSTACK'] = bstack
        page = int(self.get_argument('page', 1))
        v = Volume()
        r = v._api.page_own(cuid=uid, atte=uid, page=page, limit=20)
        if r[0]:
            return self.render("project/stick.html", vlist=r[1], vinfo=r[2], vurl='/project/'+pid+'/stick/', pid=pid, back=self.SESSION['BSTACK'][0])
        else:
            return self.render_alert(r[1])

class ProjectWorksHandler(BaseHandler):
    @addslash
    @session
    def get(self, pid, vid):
        uid = self.SESSION['uid']
        page = int(self.get_argument('page', 1))
        i = Item()
        ro = i._api.page(vid=pid, vtype=u'project')
        olist = [o['refer_id'] for o in ro[1]]
        r = i._api.page(page=page, vid=vid)
        if r[0]:
            for j in r[1]:
                j['is_paste'] = j['eid'] in olist
            return self.render("project/works.html", ilist=r[1], pinfo=r[2], vurl='/project/'+pid+'/volume/'+vid+'/', back=self.SESSION['BSTACK'].pop(), pid=pid)
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
        if ADMIN['admin'][-1] == uid:self.redirect('/perm/')
        self.SESSION['BSTACK'] = [self.request.uri] if pid else ['/project/']
        page = int(self.get_argument('page', 1))
        p = Project()
        r = p._api.page(cuid=uid, limit=10000)
        if r[0]:
            plist = self._f_proj(r[1])
            if not pid:pid = plist[0]['pid'] if len(plist)>0 else None
            rp = p._api.get(pid, cuid=uid)
            if rp[0] and rp[1]:
                project = rp[1]
                if not rp[1]['works']:
                    project['works'] = []
            else:
                project={'works':[]}
            e = Item()
            works = []
            for w in project['works']:
                if not w:continue
                rw = e._api.get(w, cuid=uid)
                if rw[0] and rw[1]:
                    works.append(rw[1])
            wlimit = 15
            return self.render("space/project.html", plist=plist, pinfo=self.page_info(page, 5, len(works), wlimit), works=works[(page-1)*wlimit:(page)*wlimit], project=project, pid=pid if pid else '', rl=[])
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
    
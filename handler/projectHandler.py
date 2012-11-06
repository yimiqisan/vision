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
        r = p._api.page(cuid=uid, page=page)
        plist = self._flt_month(r[1])
        return self.render("project/list.html", pinfo= self.page_info(page, 5, len(plist), 20), plist=plist)
    
    def page_info(self, page, pglen, cnt, limit):
        info = {}
        total_page = cnt/limit
        if (cnt%limit) != 0:total_page+=1
        info['total_page'] = total_page
        info['has_pre'] = (page>1)
        info['start_page'] = 1
        info['pre_page'] = max(1, page-1)
        info['page'] = page
        info['page_list'] = range(max(1, min(page-4, total_page-pglen+1)), min(max(page+1+pglen/2, pglen+1), total_page+1))
        info['has_eps'] = (total_page>max(page+1+pglen/2, pglen+1)>pglen)
        info['has_next'] = (page<total_page)
        info['next_page'] = min(page+1, total_page)
        info['end_page'] = total_page
        return info
    
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
        url = '/project/'+pid+'/build/'
        if url not in self.SESSION['BSTACK']:
            bstack = self.SESSION['BSTACK']
            bstack.append(url)
            self.SESSION['BSTACK'] = bstack
        page = int(self.get_argument('page', 1))
        i = Item()
        ro = i._api.page(vid=pid, vtype=u'project')
        olist = [o['refer_id'] for o in ro[1]]
        v = Volume()
        r = v._api.page_own(owner=uid, limit=1000)
        ilist = []
        for vi in r[1]:
            ri = i._api.page(vid=vi['vid'])
            for j in ri[1]:
                j['is_paste'] = j['eid'] in olist
            ilist.extend(ri[1])
        if r[0]:
            return self.render("project/build.html", ilist=ilist, back=self.SESSION['BSTACK'][0], pinfo=self.page_info(page, 5, len(ilist), 20), pid=pid)
        else:
            return self.render_alert(r[1])

    def page_info(self, page, pglen, cnt, limit):
        info = {}
        total_page = cnt/limit
        if (cnt%limit) != 0:total_page+=1
        info['total_page'] = total_page
        info['has_pre'] = (page>1)
        info['start_page'] = 1
        info['pre_page'] = max(1, page-1)
        info['page'] = page
        info['page_list'] = range(max(1, min(page-4, total_page-pglen+1)), min(max(page+1+pglen/2, pglen+1), total_page+1))
        info['has_eps'] = (total_page>max(page+1+pglen/2, pglen+1)>pglen)
        info['has_next'] = (page<total_page)
        info['next_page'] = min(page+1, total_page)
        info['end_page'] = total_page
        return info


class ProjectStickHandler(BaseHandler):
    '''收藏作品列表
    '''
    @addslash
    @session
    @authenticated
    def get(self, pid):
        uid = self.SESSION['uid']
        url = '/project/'+pid+'/stick/'
        if url not in self.SESSION['BSTACK']:
            bstack = self.SESSION['BSTACK']
            bstack.append(url)
            self.SESSION['BSTACK'] = bstack
        page = int(self.get_argument('page', 1))
        back = self.request.headers.get('Referer', None)
        i = Item()
        ro = i._api.page(vid=pid, vtype=u'project')
        olist = [o['refer_id'] for o in ro[1]]
        v = Volume()
        r = v._api.page_own(atte=uid, limit=1000)
        ilist = []
        for ci in r[1]:
            rid = ci['vid']
            ri = i._api.page(vid=rid)
            for j in ri[1]:
                j['is_paste'] = j['eid'] in olist
            ilist.extend(ri[1])
        if r[0]:
            return self.render("project/stick.html", ilist=ilist, back=self.SESSION['BSTACK'][0], pinfo=self.page_info(page, 5, len(ilist), 20), pid=pid)
        else:
            return self.render_alert(r[1])
    
    def page_info(self, page, pglen, cnt, limit):
        info = {}
        total_page = cnt/limit
        if (cnt%limit) != 0:total_page+=1
        info['total_page'] = total_page
        info['has_pre'] = (page>1)
        info['start_page'] = 1
        info['pre_page'] = max(1, page-1)
        info['page'] = page
        info['page_list'] = range(max(1, min(page-4, total_page-pglen+1)), min(max(page+1+pglen/2, pglen+1), total_page+1))
        info['has_eps'] = (total_page>max(page+1+pglen/2, pglen+1)>pglen)
        info['has_next'] = (page<total_page)
        info['next_page'] = min(page+1, total_page)
        info['end_page'] = total_page
        return info

class ProjectHandler(BaseHandler):
    '''项目首页
    '''
    @addslash
    @session
    @authenticated
    def get(self, pid):
        uid = self.SESSION['uid']
        if ADMIN['admin'][-1] == uid:
            self.redirect('/perm/')
        self.SESSION['BSTACK'] = ['/project/'+pid+'/'] if pid else ['/project/']
        page = int(self.get_argument('page', 1))
        p = Project()
        r = p._api.page(cuid=uid, limit=10000)
        if r[0]:
            plist = self._f_proj(r[1])
            if not pid:pid = plist[0]['pid'] if len(plist)>0 else None
            rp = p._api.get(pid, cuid=uid)
            if rp[0]: project=rp[1]
            e = Item()
            re = e._api.page(vid=pid, page=page, limit=20)
            works= re[1] if re[0] and re[1] and pid else []
            return self.render("space/project.html", plist=plist, pinfo=self.page_info(page, 5, len(works), 15), works=works, project=project, pid=pid if pid else '', rl=[])
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
    
    def page_info(self, page, pglen, cnt, limit):
        info = {}
        total_page = cnt/limit
        if (cnt%limit) != 0:total_page+=1
        info['total_page'] = total_page
        info['has_pre'] = (page>1)
        info['start_page'] = 1
        info['pre_page'] = max(1, page-1)
        info['page'] = page
        info['page_list'] = range(max(1, min(page-4, total_page-pglen+1)), min(max(page+1+pglen/2, pglen+1), total_page+1))
        info['has_eps'] = (total_page>max(page+1+pglen/2, pglen+1)>pglen)
        info['has_next'] = (page<total_page)
        info['next_page'] = min(page+1, total_page)
        info['end_page'] = total_page
        return info




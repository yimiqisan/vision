#!/usr/bin/env python
# encoding: utf-8
"""
weiboHandler.py

Created by 刘 智勇 on 2011-11-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from vision.apps.reply import Reply
from vision.apps.staff import Staff
from vision.apps.alert import Alert
from vision.apps.tools import session
from datetime import datetime


class AjaxReplyHandler(BaseHandler):
    '''ajax方式显示回复
    '''
    CHANNEL = u'reply'
    @session
    def get(self):
        uid = self.SESSION['uid']
        tid = self.get_argument("id")
        cursor = self.get_argument('cursor', None)
        if cursor:cursor=int(cursor)
        rly = Reply()
        r = rly._api.extend(cuid=uid, channel=[u'reply'], topic=tid, cursor=cursor, limit=1000, order=-1)
        if r[0]:
            htmls = []
            for i in r[1]:
                i['info'] = self._oinfo(i['owner'])
                htmls.append(self.render_string("util/reply.html", reply=i, uid=uid))
            a = Alert()
            a._api.click(uid, tid)
            return self.write(json.dumps({'htmls':htmls, 'info':r[1], 'cursor': r[2]}))
        else:
            return self.write({'error':'save error'})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        reply = self.preserve(uid)
        if reply:
            reply["html"] = self.render_string("util/reply.html", reply=reply)
        else:
            return self.write(json.dumps({'error':'save error'}))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(json.dumps(reply))
    
    @session
    def preserve(self, uid):
        uid = self.SESSION['uid']
        ulogo = self.SESSION['ulogo']
        to = self.get_argument("to")
        c = self.get_argument("content")
        rly = Reply()
        nick = self.current_user if uid else '匿名驴友'
        kwargs = {'nick':nick}
        r = rly._api.save(c, owner=uid, tid=to, channel=self.CHANNEL, **kwargs)
        if r[0]:
            kwargs.update({'id':r[1], 'content':c, 'owner': uid, 'info':self._oinfo(uid), 'is_own':True, 'tid': to, 'created':'刚刚', 'ulogo':ulogo})
            return kwargs
        else:
            return None

    def _oinfo(self, owner):
        s = Staff()
        r = s._api.get(owner)
        if r[0] and r[1]:
            return r[1]['job'] if r[1]['job'] else '管理员'
        return 'none'

class AjaxNewReplyHandler(BaseHandler):
    '''ajax方式新建回复
    '''
    CHANNEL = u'reply'
    @session
    def get(self):
        uid = self.SESSION['uid']
        tid = self.get_argument("id")
        limit = int(self.get_argument("limit", 1000))
        cursor = self.get_argument('cursor', None)
        if cursor:cursor=int(cursor)
        tl = Reply()
        r = rly._api.extend(cuid=uid, channel=[u'reply'], topic=tid, cursor=cursor, limit=limit)
        if r[0]:
            htmls = []
            for i in r[1]:
                htmls.append(self.render_string("util/reply.html", reply=i, uid=uid))
            return self.write(json.dumps({'htmls':htmls, 'info':r[1], 'cursor': r[2]}))
        else:
            return self.write({'error':'save error'})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        reply = self.preserve(uid)
        if reply:
            reply["html"] = self.render_string("util/reply.html", reply=reply)
        else:
            return self.write(json.dumps({'error':'save error'}))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(json.dumps(reply))
    
    @session
    def preserve(self, uid):
        uid = self.SESSION['uid']
        ulogo = self.SESSION['ulogo']
        to = self.get_argument("to")
        c = self.get_argument("content")
        rly = Reply()
        nick = self.current_user if uid else '匿名'
        kwargs = {'nick':nick, 'ulogo':ulogo}
        r = rly._api.save(c, owner=uid, tid=to, channel=self.CHANNEL, **kwargs)
        if r[0]:
            kwargs.update({'id':r[1], 'content':c, 'owner': uid, 'info':self._oinfo(uid), 'is_own':True, 'tid': to, 'created':'刚刚', 'ulogo':ulogo})
            return kwargs
        else:
            return None
    
    def _oinfo(self, owner):
        s = Staff()
        r = s._api.get(owner)
        if r[0] and r[1]:
            return r[1]['job'] if r[1]['job'] else '管理员'
        return 'none'
    
class AjaxRemoveHandler(BaseHandler):
    '''ajax方式删除
    '''
    @session
    def post(self):
        rly = Reply()
        uid = self.SESSION['uid']
        rid = self.get_argument("id", None)
        r = rly._api.remove(rid)
        self.write(json.dumps('ok'))

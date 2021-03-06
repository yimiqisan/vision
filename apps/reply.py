#!/usr/bin/env python
# encoding: utf-8
"""
reply.py

Created by 刘 智勇 on 2012-08-19.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
import time

from vision.config import DB_CON, DB_NAME, DEFAULT_CUR_UID
from staff import StaffAPI
from modules import TimeLineDoc
from api import API, Added_id
import case

class Reply(object):
    def __init__(self, api=None):
        self._api = ReplyAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class ReplyAPI(API):
    def __init__(self):
        DB_CON.register([TimeLineDoc])
        datastore = DB_CON[DB_NAME]
        col_name = TimeLineDoc.__collection__
        collection = datastore[col_name]
        doc = collection.TimeLineDoc()
        self.staff = StaffAPI()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def _get_nick(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return r[1]['added'].get('nick', None)
        return None
    
    def _flt_at(self, c):
        l = c.split(u' ')
        at_l = []
        for i in l:
            if i.count('@')==1:
                s = i.find('@')+1
                at_l.append(i[s:])
            elif i.count('@')>1:
                s = i.find('@')+1
                t_l = i[s:].split('@')
                at_l.extend(t_l)
        return list(set(at_l))
    
    def _fire_alert(self, channel, tid, at_list):
        c = case.get_case_object()
        for at in at_list:
            uid = self.staff.nick2id(at)
            if uid:
                c.fire('a_reply', to=uid, tid=tid)
    
    def save(self, content, owner=None, tid=None, channel=u'reply', **kwargs):
        ''' 保存回复 '''
        if tid:
            a = Added_id(tid)
            a.incr()
        at_list = self._flt_at(content)
        self._fire_alert(channel, tid, at_list)
        return super(ReplyAPI, self).create(owner=owner, content=content, at_list=at_list, topic=tid, channel=channel, **kwargs)
    
    def remove(self, id):
        ''' 删除回复 '''
        r = self.get(id)
        if r[0] and r[1] and (r[1]['channel'] == u'reply'):
            a = Added_id(r[1]['tid'])
            a.decr()
        return super(ReplyAPI, self).remove(id)
    
    def _count(self, tid):
        if not tid:return 0
        a = Added_id(tid)
        c = a.count()
        return c if (c>0) else 0
    
    def _perm(self, cuid, owner):
        return 0x01
    
    def _output(self, result=[], cuid=DEFAULT_CUR_UID):
        ''' 回复格式化输出 '''
        now = datetime.now()
        output_map = lambda i: {'id':i['_id'], 'added_id':i['added_id'], 'owner':i['owner'], 'perm':self._perm(cuid, i['owner']), 'is_own':(cuid==i['owner'] if i['owner'] else True), 'nick':i['added'].get('nick', '匿名'), 'tid':i.get('topic', None), 'content':i['content'], 'ulogo':i['added'].get('ulogo', None), 'channel':i['channel'], 'count': self._count(i['_id']), 'created':self._escape_created(now, i['created'])}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        ''' 获取单个回复 '''
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output(result=r[1]))
        return r
    
    def extend(self, cuid=DEFAULT_CUR_UID, owner=None, topic=None, channel=None, at=None, cursor=None, limit=20, order_by='added_id', order=-1):
        ''' 获取扩展回复输出 '''
        kwargs = {}
        if owner:kwargs['owner']=owner
        if topic:kwargs['topic'] = {'$in':topic} if isinstance(topic, list) else topic
        if at:kwargs['at_list']=at
        if channel:kwargs['channel']={'$in':channel}
        if cursor:kwargs['cursor']=cursor
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(ReplyAPI, self).extend(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output(**kw)
            added_id = min(l[0]['added_id'], l[-1]['added_id']) if len(l)!=0 else -1
            return (True, l, added_id)
        else:
            return (False, r[1])
    
    def page(self, cuid=DEFAULT_CUR_UID, owner=None, topic=None, channel=None, at=None, page=1, pglen=5, cursor=None, limit=20, order_by='added_id', order=-1):
        ''' 分页显示回复 '''
        kwargs = {}
        if owner:kwargs['owner']=owner
        if topic:kwargs['topic'] = {'$in':topic} if isinstance(topic, list) else topic
        if at:kwargs['at_list']=at
        if channel:kwargs['channel']={'$in':channel}
        kwargs['page']=page
        kwargs['pglen']=pglen
        if cursor:kwargs['cursor']=cursor
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(ReplyAPI, self).page(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output(**kw)
            return (True, l, r[2])
        else:
            return (False, r[1])

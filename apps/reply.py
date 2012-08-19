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
from modules import TimeLineDoc
from api import API, Added_id

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
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def _flt_tpc(self, c, k):
        c = c.strip()
        t = tid = None
        if not k:k=u'weibo'
        if c.startswith('#')and(c.count('#')>1):
            l = c.split('#')
            for i in l:
                if (i!=''):t = i;break
            m = Mapping()
            r = m.do(k, t)
            if not r[0]:return r
            tid = r[1]
        return tid

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
        if channel == u'reply':
            for at in at_list:c.fire('a_weibo_ra', to=at)
        else:
            for at in at_list:c.fire('a_weibo_at', to=at)
    
    def save(self, content, owner=None, tid=None, channel=u'normal', **kwargs):
        if tid:
            a = Added_id(tid)
            a.incr()
        else:
            kind = kwargs.get('kind', u'event')
            tid = self._flt_tpc(content, kind)
        at_list = self._flt_at(content)
        #self._fire_alert(channel, tid, at_list)
        return super(ReplyAPI, self).create(owner=owner, content=content, at_list=at_list, topic=tid, channel=channel, **kwargs)
    
    def remove(self, id):
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
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        output_map = lambda i: {'id':i['_id'], 'added_id':i['added_id'], 'owner':i['owner'], 'perm':self._perm(cuid, i['owner']), 'is_own':(cuid==i['owner'] if i['owner'] else True), 'nick':i['added'].get('nick', '匿名驴友'), 'tid':i.get('topic', None), 'content':i['content'], 'ulogo':i['added'].get('ulogo', None), 'channel':i['channel'], 'count': self._count(i['_id']), 'created':self._escape_created(now, i['created'])}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def extend(self, cuid=DEFAULT_CUR_UID, owner=None, topic=None, channel=None, at=None, cursor=None, limit=20, order_by='added_id', order=-1):
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
            l = self._output_format(**kw)
            added_id = min(l[0]['added_id'], l[-1]['added_id']) if len(l)!=0 else -1
            return (True, l, added_id)
        else:
            return (False, r[1])
    
    def page(self, cuid=DEFAULT_CUR_UID, owner=None, topic=None, channel=None, at=None, page=1, pglen=10, cursor=None, limit=20, order_by='added_id', order=-1):
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
            l = self._output_format(**kw)
            return (True, l, r[2])
        else:
            return (False, r[1])
        
    def abbr(self, cuid=DEFAULT_CUR_UID, owner=None, topic=None, channel=None, at=None, order_by='added_id', order=-1):
        kwargs = {}
        if topic:kwargs['topic'] = {'$in':topic} if isinstance(topic, list) else topic
        if channel:kwargs['channel']={'$in':channel}
        c = super(ReplyAPI, self).count(**kwargs)
        if c == 0:
            return (False, u'抢沙发啦', False)
        elif c == 1:
            rt = self.extend(cuid=cuid, topic=topic, channel=channel, limit=1, order=1)
            return (rt[1][0]['content'], '点击留言', False)
        elif c== 2:
            rt = self.extend(cuid=cuid, topic=topic, channel=channel, limit=2, order=1)
            return (rt[1][0]['content'], '共2条留言', rt[1][1]['content'])
        elif c>2:
            rt = self.extend(cuid=cuid, topic=topic, channel=channel, limit=1, order=1)
            rb = self.extend(cuid=cuid, topic=topic, channel=channel, limit=1, order=-1)
            return (rt[1][0]['content'], '共'+str(c)+'条留言', rb[1][0]['content'])
        else:
            return (False, u'抢沙发啦', False)
    
    def pack(self, cuid=DEFAULT_CUR_UID, owner=None, topic=None, channel=None, at=None, order_by='added_id', order=-1):
        kwargs = {}
        if topic:kwargs['topic'] = {'$in':topic} if isinstance(topic, list) else topic
        if channel:kwargs['channel']={'$in':channel}
        c = super(ReplyAPI, self).count(**kwargs)
        if c == 0:
            return (True, False, False, 0)
        elif c == 1:
            rt = self.extend(cuid=cuid, topic=topic, channel=channel, limit=1, order=1)
            return (True, rt[1][0], False, 0)
        elif c== 2:
            rt = self.extend(cuid=cuid, topic=topic, channel=channel, limit=2, order=1)
            return (True, rt[1][0], rt[1][1], 0)
        elif c>2:
            rt = self.extend(cuid=cuid, topic=topic, channel=channel, limit=1, order=1)
            rb = self.extend(cuid=cuid, topic=topic, channel=channel, limit=1, order=-1)
            return (True, rt[1][0], rb[1][0], c-2)
        else:
            return (False, False, False, 0)
    
    def topN(self, cuid=DEFAULT_CUR_UID, owner=None, topic=None, channel=None, at=None, cursor=None, limit=5, order_by='added_id', order=-1):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if topic:kwargs['topic'] = {'$in':topic} if isinstance(topic, list) else topic
        if at:kwargs['at_list']=at
        if channel:kwargs['channel']={'$in':channel}
        if cursor:kwargs['cursor']=cursor
        c = super(ReplyAPI, self).count(**kwargs)
        left = c-limit
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(ReplyAPI, self).extend(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            l.reverse()
            if left>0:
                added_id = min(l[0]['added_id'], l[-1]['added_id']) if len(l)!=0 else -1
            else:
                added_id = -1
            return (True, l, added_id, left)
        else:
            return (False, r[1], -1, 0)

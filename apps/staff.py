#!/usr/bin/env python
# encoding: utf-8
"""
staff.py

Created by 刘 智勇 on 2012-06-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
import time
from md5 import md5

from vision.config import DB_CON, DB_NAME, DEFAULT_CUR_UID
from modules import StaffDoc
from api import API, Added_id


class Staff(object):
    
    ADMIN = {'admin': ('admin', u'57138d461d7343c685c15e9e6d3bd9ef')}
    
    def __init__(self, api=None):
        self._api = StaffAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None
    
    def register(self, **info):
        nick = info.get('nick', None)
        if nick:
            r = self._api.is_nick_exist(nick)
            if r:return (False, '名号已被占用')
        email = info.get('email', None)
        if email:
            if self._api.is_email_exist(email):return (False, '邮箱已被占用')
        password = info.get('password', None)
        if password:
            info['password'] = unicode(md5(password).hexdigest())
        c = self._api.create(**info)
        if c[0]:
            self.info = info
        else:
            self.info = None
        return c
    
    def login(self, nick, password):
        if (nick in self.ADMIN.keys()) and (password == self.ADMIN[nick][0]):
            return (True, {'_id':self.ADMIN[nick][1], 'added':{'logo': None}})
        r = self._api.is_nick_exist(nick)
        if not r:return (False, '查无此人')
        c = self._api.one(nick=nick)
        password = unicode(md5(password).hexdigest())
        if c[0] and (c[1]['password'] == password):
            self.info = c[1]
            return (True, c[1])
        self.info = None
        return (False, '用户名或密码错误')
    
    def reset_password(self, id, email):
        pwd = self.random_password()
        password = unicode(md5(pwd).hexdigest())
        self._api.edit(id, password=password)
        return (True, pwd)
        
    def random_password(self):
        from string import digits, ascii_letters
        from random import sample
        seed = digits+ascii_letters
        return ''.join(sample(seed, 6))

class StaffAPI(API):
    def __init__(self):
        DB_CON.register([StaffDoc])
        datastore = DB_CON[DB_NAME]
        col_name = StaffDoc.__collection__
        collection = datastore[col_name]
        doc = collection.StaffDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def is_nick_exist(self, nick):
        return self.exist("nick", nick)
    
    def is_email_exist(self, email):
        return self.exist("email", email)
    
    def is_nick(self, nick):
        try:
            nick.encode('utf8')
        except UnicodeEncodeError:
            return True
        if len(nick)==32:
            return False
        return True
    
    def change_pwd(self, id, o, n, c):
        self.edit(id, password=n)
    
    def nick2id(self, nick):
        if self.is_nick(nick):
            r = self.one(nick=nick)
            if r[0] and r[1]:
                return r[1]['_id']
            return None
        return nick
    
    def remove(self, id):
        r = self.get(id)
        return super(StaffAPI, self).remove(id)
    
    def _perm(self, cuid, uid):
        return 1
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        output_map = lambda i: {'pid':i['_id'], 'added_id':i['added_id'], 'email':i.get('email', None), 'password':None, 'belong':i['belong'], 'perm':self._perm(cuid, i['belong']), 'is_own':(cuid==i['belong'] if i['belong'] else True), 'nick':i['nick'], 'level':i['level'], 'logo':i['added'].get('logo', None), 'male':i['added'].get('male', None), 'created':self._escape_created(now, i['created'])}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def page(self, cuid=DEFAULT_CUR_UID, belong=None, level=None, page=1, pglen=10, cursor=None, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        if belong:kwargs['belong']=belong
        if level:kwargs['level'] = {'$in':level} if isinstance(level, list) else level
        kwargs['page']=page
        kwargs['pglen']=pglen
        if cursor:kwargs['cursor']=cursor
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(StaffAPI, self).page(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l, r[2])
        else:
            return (False, r[1])
    
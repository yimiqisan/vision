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

from vision.config import DB_CON, DB_NAME, PERM_CLASS, ADMIN, DEFAULT_CUR_UID
from modules import StaffDoc
from api import API, Added_id
from perm import Permission


class Staff(object):
    def __init__(self, api=None):
        self._api = StaffAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None
    
    def whois(self, k, v):
        ''' 确定用户身份 '''
        if v == ADMIN['admin'][1]:
            self.info = {'nick': ADMIN['admin'][0], 'password': unicode(md5(ADMIN['admin'][0]).hexdigest()), '_id': ADMIN['admin'][1]}
            self.uid = ADMIN['admin'][1]
            return None
        c = self._api.one(**{k:v})
        if c[0] and c[1]:
            self.info = c[1]
            self.uid = self.info['_id']
        else:
            self.uid = self.info = None
    
    def register(self, **info):
        ''' 注册账号 '''
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
    
    def login(self, email, password):
        ''' 账户登陆 '''
        if (email in ADMIN.keys()) and (password == ADMIN[email][0]):
            return (True, {'_id':ADMIN[email][1], 'pm':[PERM_CLASS['SUPEROR']], 'added':{'logo': None}, 'nick': 'admin'})
        r = self._api.is_email_exist(email)
        if not r:return (False, '查无此人')
        c = self._api.one(email=email)
        password = unicode(md5(password).hexdigest())
        if c[0] and (c[1]['password'] == password):
            p = Permission()
            info = c[1]
            info['pm'] = p._api.get_owner_value(info['_id'], u'site')
            self.info = info
            return (True, info)
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
        self.p = Permission()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def is_nick_exist(self, nick):
        ''' 判断nick是否存在 '''
        return self.exist("nick", nick)
    
    def is_email_exist(self, email):
        ''' 判断email是否存在 '''
        return self.exist("email", email)
    
    def is_nick(self, nick):
        ''' 判断是否是nick '''
        try:
            nick.encode('utf8')
        except UnicodeEncodeError:
            return True
        if len(nick)==32:
            return False
        return True
    
    def change_pwd(self, id, o, n, c):
        ''' 改变密码 '''
        self.edit(id, password=n)
    
    def nick2id(self, nick):
        ''' 根据nick获取id '''
        if self.is_nick(nick):
            r = self.one(nick=nick)
            if r[0] and r[1]:
                return r[1]['_id']
            return None
        return nick
    
    def remove(self, id):
        ''' 删除账号 '''
        r = self.get(id)
        return super(StaffAPI, self).remove(id)
    
    def _perm(self, uid):
        return self.p._api.get_owner_value(uid, u'site')
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        ''' 格式化输出用户信息 '''
        now = datetime.now()
        output_map = lambda i: {'pid':i['_id'], 'added_id':i['added_id'], 'pm':self._perm(i['_id']), 'email':i.get('email', None), 'password':None, 'belong':i['belong'], 'job':i['added'].get('job', ''), 'discribe':i['added'].get('discribe', ''), 'is_own':(cuid==i['belong'] if i['belong'] else True), 'nick':i['nick'] if i['nick'] and '@' not in i['nick'] else i.get('email', None), 'level':i['level'], 'avatar':i.get('avatar', None), 'male':i['added'].get('male', None), 'created':self._escape_created(now, i['created'])}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        ''' 获取单个用户信息 '''
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def page(self, cuid=DEFAULT_CUR_UID, belong=None, level=None, page=1, pglen=5, cursor=None, limit=20, order_by='added_id', order=-1):
        ''' 分页显示用户信息 '''
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
    
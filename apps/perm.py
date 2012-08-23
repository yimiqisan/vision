#!/usr/bin/env python
# encoding: utf-8
"""
perm.py

Created by 刘 智勇 on 2012-06-26.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
import time

from vision.config import DB_CON, DB_NAME, ADMIN, PERM_CLASS
from modules import PermissionDoc
from api import API


class Permission(object):
    def __init__(self, api=None):
        self._api = PermissionAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None
    
class PermissionAPI(API):
    def __init__(self):
        DB_CON.register([PermissionDoc])
        datastore = DB_CON[DB_NAME]
        col_name = PermissionDoc.__collection__
        collection = datastore[col_name]
        doc = collection.PermissionDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def award(self, owner, channel, key, cid=None, **kwargs):
        if key not in PERM_CLASS.keys():
            return (False, 'beyond key')
        value = unicode(key)
        return super(PermissionAPI, self).create(owner=owner, channel=channel, cid=cid, value=value, **kwargs)
    
    def deprive(self, owner, channel, cid=None):
        return super(PermissionAPI, self).drops(owner=owner, channel=channel, cid=cid)
    
    def get(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def get_owner_value(self, owner=None, channel=None, cid=None):
        kwargs = {}
        if owner:kwargs['owner'] = owner
        if channel:kwargs['channel'] = channel
        if cid:kwargs['cid'] = cid
        r = self.find(**kwargs)
        pl = []
        if r[0] and r[1]:
            pl = [PERM_CLASS[i.get('value', 'NORMAL')] for i in r[1]]
        else:
            pl.append(PERM_CLASS['NORMAL'])
        return pl
    
    def _output_map(self, out):
        ret_d = {'id':out['_id'], 'owner':out['owner'], 'channel':out['channel'], 'cid':out['cid'], 'value':out['value'], 'created':out['created'].strftime('%m-%d %H:%M')}
        for k in out['added']:
            ret_d[k] = out['added'][k]
        return ret_d
    
    def _output_format(self, result=[]):
        if isinstance(result, dict):
            return self._output_map(result)
        return [self._output_map(i) for i in result]
    
    def list(self, owner=None, channel=None, cid=None, key=None):
        kwargs = {}
        if owner:kwargs['owner'] = owner
        if channel:kwargs['channel'] = channel
        if cid:kwargs['cid'] = cid
        if key and (key in PERM_CLASS.keys()):kwargs['value'] = PERM_CLASS[key]
        r = self.find(**kwargs)
        if r[0]:
            return self._output_format(result=r[1])
        else:
            return None
    
class preperm(object):
    def __init__(self, keys=['SUPEROR', 'MANAGER']):
        self.keys = keys
    
    def __call__(self, method):
        def wapper(decorated_cls, *args):
            p = Permission()
            cuid = decorated_cls.SESSION['uid']
            pm = p._api.site_perm(cuid)
            if pm is None:decorated_cls.render_alert(u"该页无法显示")
            if isinstance(self.keys, str) and (pm!=PERM_CLASS[self.keys]):
                decorated_cls.render_alert(u"该页无法显示")
            elif isinstance(self.keys, list) and (pm not in [PERM_CLASS[k] for k in self.keys]):
                decorated_cls.render_alert(u"该页无法显示")
            decorated_cls.__setattr__('pm', pm)
            return method(decorated_cls, *args)
        return wapper


import functools
def addperm(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        uid = self.SESSION['uid']
        if uid == ADMIN['admin'][1]:
            self.__setattr__('pm', PERM_CLASS['SUPEROR'])
        else:
            p = Permission()
            v = p._api.get_owner_value(uid)
            self.__setattr__('pm', v)
        return method(self, *args, **kwargs)
    return wrapper
    
    
    
    
    
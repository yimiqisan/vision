#!/usr/bin/env python
# encoding: utf-8
"""
item.py

Created by 刘 智勇 on 2012-06-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
import time

from vision.config import DB_CON, DB_NAME, DEFAULT_CUR_UID
from modules import ItemDoc
from api import API, Added_id

VTYPE_LIST = [u'personal', u'organization', u'project']

class Item(object):
    def __init__(self, api=None):
        self._api = ItemAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return  None

class ItemAPI(API):
    def __init__(self):
        DB_CON.register([ItemDoc])
        datastore = DB_CON[DB_NAME]
        col_name = ItemDoc.__collection__
        collection = datastore[col_name]
        doc = collection.ItemDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def save(self, owner, vid, vtype, logo, *works, **kwargs):
        return super(ItemAPI, self).create(owner=owner, vid=vid, vtype=vtype, logo=logo, works=list(works), **kwargs)

    def remove(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):
            vtype, vid = r[1].get('vtype', None), r[1].get('vid', None)
            super(ItemAPI, self).remove(id)
            return (True, vtype, vid)
        return (False, 'item not exist')
    
    def edit(self, id, **kwargs):
        kwargs['isOverWrite']=True
        return super(ItemAPI, self).edit(id, **kwargs)

    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        output_map = lambda i: {'eid':i['_id'], 'logo':i.get('logo', None), 'vid':i.get('vid', None), 'vtype':i.get('vtype', None), 'added_id':i['added_id'], 'owner':i['owner'], 'is_own':(cuid==i['owner'] if i['owner'] else True), 'works':i['works'], 'created':self._escape_created(now, i['created']), 'name':i['added'].get('name', None), 'client':i['added'].get('client', None)}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def page(self, cuid=DEFAULT_CUR_UID, owner=None, vid=None, vtype=None, page=1, pglen=10, cursor=None, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if vid:kwargs['vid']=vid
        if vtype:kwargs['vtype']=vtype
        kwargs['page']=page
        kwargs['pglen']=pglen
        if cursor:kwargs['cursor']=cursor
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(ItemAPI, self).page(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l, r[2])
        else:
            return (False, r[1])
    
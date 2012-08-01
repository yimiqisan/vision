#!/usr/bin/env python
# encoding: utf-8
"""
project.py

Created by 刘 智勇 on 2012-06-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
import time

from vision.config import DB_CON, DB_NAME, DEFAULT_CUR_UID
from modules import ProjectDoc
from api import API, Added_id

class Project(object):
    def __init__(self, api=None):
        self._api = ProjectAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class ProjectAPI(API):
    def __init__(self):
        DB_CON.register([ProjectDoc])
        datastore = DB_CON[DB_NAME]
        col_name = ProjectDoc.__collection__
        collection = datastore[col_name]
        doc = collection.ProjectDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def save(self, owner, title, description, *members, **kwargs):
        return super(ProjectAPI, self).create(owner=owner, title=title, description=description, members=list(members), **kwargs)
    
    def remove(self, id):
        return super(ProjectAPI, self).remove(id)
    
    def edit(self, id, **kwargs):
        return super(ProjectAPI, self).edit(id, **kwargs)
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        output_map = lambda i: {'pid':i['_id'], 'added_id':i['added_id'], 'owner':i['owner'], 'is_own':(cuid==i['owner'] if i['owner'] else True), 'title':i['title'], 'description':i.get('description', None), 'members':i['members'], 'created':self._escape_created(now, i['created'])}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def page(self, cuid=DEFAULT_CUR_UID, owner=None, page=1, pglen=10, cursor=None, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        if owner:kwargs['owner']=owner
        kwargs['page']=page
        kwargs['pglen']=pglen
        if cursor:kwargs['cursor']=cursor
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(ProjectAPI, self).page(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l, r[2])
        else:
            return (False, r[1])
    

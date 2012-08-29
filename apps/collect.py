#!/usr/bin/env python
# encoding: utf-8
'''
volume.py

Created by 刘 智勇 on 2012-06-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
'''

import logging
import uuid
from datetime import datetime
import time
import re

from vision.config import DB_CON, DB_NAME, DEFAULT_CUR_UID, PERM_CLASS, DATE_FORMAT
from volume import Volume, get_cn
from modules import CollectDoc
from api import API, Added_id


class Collect(object):
    def __init__(self, api=None):
        self._api = CollectAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class CollectAPI(API):
    def __init__(self):
        DB_CON.register([CollectDoc])
        datastore = DB_CON[DB_NAME]
        col_name = CollectDoc.__collection__
        collection = datastore[col_name]
        doc = collection.CollectDoc()
        self.vol = Volume()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def save(self, owner, refer_id):
        ''' 新建收藏 '''
        kwargs = {}
        r = self.vol._api.get(refer_id)
        if r[0]:
            kwargs.update(r[1])
            kwargs.pop('added_id')
            kwargs['refer_id'] = kwargs.pop('vid')
            kwargs['owner'] = owner
            kwargs['born'] = datetime.strptime(kwargs['born'], '%Y%m%d')
            return super(CollectAPI, self).create(**kwargs)
        return (False, r[1])

    def edit(self, id, refer_id, **kwargs):
        ''' 编辑收藏 '''
        return super(CollectAPI, self).edit(id, **kwargs)
    
    def remove(self, id):
        ''' 删除单个收藏 '''
        return super(CollectAPI, self).remove(id)
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        ''' 格式化输出 '''
        now = datetime.now()
        output_map = lambda i: {'cid':i['_id'], 'refer_id':i['refer_id'], 'added_id':i['added_id'], 'logo':i.get('logo', None), 'name':i.get('name', '无名'), 'prop':i.get('prop', None), 'prop_cn':get_cn(p=i.get('prop', None)), 'maintype':i.get('maintype', None), 'maintype_cn':get_cn(m=i.get('maintype', None)), 'subtype':i.get('subtype', None), 'subtype_cn':get_cn(s=i.get('subtype', None)), 'live':i.get('live', None), 'male':i.get('male', None), 'male_cn':'男' if i.get('male', None) else '女', 'born':datetime.strftime(i.get('born', datetime.now()), '%Y%m%d'), 'website':i['added'].get('website', None), 'agency':i.get('agency', None), 'grade':i.get('grade', None), 'nexus':i.get('nexus', None), 'intro':i['added'].get('intro', None), 'about':i['added'].get('about', None), 'created':self._escape_created(now, i['created'])}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        ''' 获取单个收藏 '''
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def page(self, cuid=DEFAULT_CUR_UID, owner=None, perm=None, name=None, prop=None, live=None, agency=None, tags=[], grade=None, nexus=None, male=None, born_interval=(None, None), page=1, pglen=10, limit=20, order_by='added_id', order=-1):
        ''' 分页显示收藏 '''
        kwargs = {}
        if owner:kwargs['owner']=owner
        if name:kwargs['name']=re.compile('.*'+name+'.*')
        if prop:
            prop_list = [u'PERSONAL', u'ORGANIZATION', u'SHOW']
            if isinstance(prop, list) and set(prop).issubset(set(prop_list)):
                kwargs['prop']={'$all':prop}
            elif prop.upper() in prop_list:
                kwargs['prop']=prop
        if live:kwargs['live']=live
        if agency:kwargs['agency']=agency
        if grade:kwargs['grade']=grade
        if nexus:kwargs['nexus']=nexus
        if type(male) == type(False):kwargs['male']=male
        ### born_interval
        kwargs['page']=page
        kwargs['pglen']=pglen
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(CollectAPI, self).page(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l, r[2])
        else:
            return (False, r[1])

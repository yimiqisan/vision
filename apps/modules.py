#!/usr/bin/env python
# encoding: utf-8
"""
moudles.py

Created by 刘 智勇 on 2012-06-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from datetime import datetime
import uuid

from mongokit import Document, IS
from vision.config import DB_NAME

class IdDoc(Document):
    __collection__ = 'ids'
    __database__ = DB_NAME
    
    structure = {
            '_id':unicode,
            'id':int,
    }
    use_schemaless = True
    use_dot_notation=True

class StaffDoc(Document):
    ''' 账号表 '''
    __collection__ = 'staff'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'avatar':   unicode,
            'nick':     unicode,
            'email':    unicode,
            'password': unicode,
            'level':    IS(u'manager', u'editor'),
            'belong':   unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
    }
    
    required_fields = ['_id', 'email', 'password', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class PermissionDoc(Document):
    ''' 权限表 '''
    __collection__ = 'permission'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
            'channel':  IS(u'site', u'project'),
            'cid':      unicode,
            'value':    unicode,
    }
    required_fields = ['_id', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class ItemDoc(Document):
    ''' 作品表 '''
    __collection__ = 'item'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'logo':     unicode,
            'works':    list,
            'owner':    unicode,
            'vtype':    IS(u'personal', u'organization', u'project', u'show'),
            'vid':      unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
    }
    
    required_fields = ['_id', 'owner', 'vid', 'works', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class VolumeDoc(Document):
    ''' 作品集表 '''
    __collection__ = 'volume'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'logo':     unicode,
            'name':     unicode,
            'prop':     IS(u'PERSONAL', u'ORGANIZATION', u'SHOW'),
            'maintype': IS(u'FASHION', u'ART', u'DESIGN', u'HUMAN', u'BRAND'),
            'subtype':  unicode,
            'live':     unicode,
            'agency':   unicode,
            'tags':     list,
            'grade':    int,
            'nexus':    int,
            'male':     bool,
            'born':     datetime,
            'created':  datetime,
            'atte_list':list,
            'added':    dict,
            'added_id': int,
    }
    
    required_fields = ['_id', 'name', 'prop', 'maintype', 'subtype', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class CollectDoc(Document):
    ''' 收藏表 '''
    __collection__ = 'collect'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'refer_id': unicode,
            'owner':    unicode,
            'logo':     unicode,
            'name':     unicode,
            'prop':     IS(u'PERSONAL', u'ORGANIZATION', u'SHOW'),
            'maintype': IS(u'FASHION', u'ART', u'DESIGN', u'HUMAN', u'BRAND'),
            'subtype':  unicode,
            'live':     int,
            'agency':   unicode,
            'tags':     list,
            'grade':    int,
            'nexus':    int,
            'male':     bool,
            'born':     datetime,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
    }
    
    required_fields = ['_id', 'name', 'prop', 'maintype', 'subtype', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class ProjectDoc(Document):
    ''' 项目表 '''
    __collection__ = 'project'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'title':    unicode,
            'description':  unicode,
            'members':  list,
            'works':    list,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
    }
    
    required_fields = ['_id', 'title', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class TimeLineDoc(Document):
    ''' 回复表 '''
    __collection__ = 'timeline'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
            'content':  unicode,
            'at_list':  list,
            'topic':    unicode,
            'channel':  IS(u'normal', u'reply'),
    }
    required_fields = ['_id', 'created', 'content']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True








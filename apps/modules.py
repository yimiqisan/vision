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
    __collection__ = 'staff'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'nick':     unicode,
            'email':    unicode,
            'password': unicode,
            'level':    IS(u'manager', u'editor'),
            'belong':   unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
    }
    
    required_fields = ['_id', 'nick', 'password', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class PermissionDoc(Document):
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
    __collection__ = 'item'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'logo':     unicode,
            'works':    list,
            'owner':    unicode,
            'vtype':    IS(u'personal', u'organization', u'project'),
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
            'live':     int,
            'agency':   unicode,
            'tags':     list,
            'grade':    int,
            'nexus':    int,
            'male':     bool,
            'year':     int,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
    }
    
    required_fields = ['_id', 'name', 'prop', 'maintype', 'subtype', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class ProjectDoc(Document):
    __collection__ = 'project'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'title':    unicode,
            'description':  unicode,
            'members':  list,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
    }
    
    required_fields = ['_id', 'title', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

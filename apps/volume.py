#!/usr/bin/env python
# encoding: utf-8
'''
volume.py

Created by 刘 智勇 on 2012-06-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
'''

import logging
import uuid
from datetime import datetime, timedelta
import time
import re

from vision.config import DB_CON, DB_NAME, DEFAULT_CUR_UID, PERM_CLASS, DATE_FORMAT
from modules import VolumeDoc, CollectDoc
from api import API, Added_id

VOL_TYPES_MAIN = [
        ['FASHION', '时尚'],
        ['ART', '艺术'],
        ['DESIGN', '设计'],
        ['HUMAN', '人文'],
        ['BRAND', '品牌'],
        ['PROJECT', '项目']
]

VOL_TYPES_SUB = {
        'FASHION':[['FDESIGNER', '设计师'],
            ['FPHOTOGRAPHER', '摄影师'],
            ['FSTYLISTS', '造型师'],
            ['FMAKEUP', '化妆师'],
            ['FMODEL', '模特'],
            ['FBLOGER', '博主'],
            ['FARTIST', '艺术家'],
            ['FMAGAZINE', '杂志'],
            ['FASSOCIATION', '协会'],
            ['FINSTITUTIONS', '院校'],
            ['FSHOW', '展会']],
        'ART':[['APAINTING', '绘画'],
            ['AEQUIPMENT', '装置'],
            ['ASCULPTURE', '雕塑'],
            ['AIMAGE', '影像'],
            ['AMULTIMEDIA', '多媒体'],
            ['AASSOCIATION', '协会'],
            ['AINSTITUTION', '院校'],
            ['ASHOW', '展会']],
        'DESIGN':[['DBUILDING', '建筑'],
            ['DINDOOR', '室内'],
            ['DPRODUCT', '产品'],
            ['DFLAT', '平面'],
            ['DMUTILMEDIA', '多媒体'],
            ['DASSOCIATION', '协会'],
            ['DINSTITUTION', '院校'],
            ['DSHOW', '展会']],
        'HUMAN':[['HPERFORMER', '表演者'],
            ['HTHEATER', '剧院'],
            ['HMUSEUM', '博物馆']],
        'BRAND':[['BMEDIAPEOPLE', '媒体人'],
            ['BCOMPANY', '公司']]
}

VOL_PROPERTY_MAIN = [
            ['PERSONAL', '个人'],
            ['ORGANIZATION', '机构'],
            ['SHOW', '展会']
]
    
VOL_PROPERTY_SUB = {
        'PERSONAL':[['FDESIGNER', '设计师'],
            ['FPHOTOGRAPHER', '摄影师'],
            ['FSTYLISTS', '造型师'],
            ['FMAKEUP', '化妆师'],
            ['FMODEL', '模特'],
            ['FBLOGER', '博主'],
            ['FARTIST', '艺术家'],
            ['HPERFORMER', '表演者'],
            ['BMEDIAPEOPLE', '媒体人']],
        'ORGANIZATION':[['FMAGAZINE', '杂志'],
            ['FASSOCIATION', '协会'],
            ['FINSTITUTIONS', '院校'],
            ['AASSOCIATION', '协会'],
            ['AINSTITUTION', '院校'],
            ['DASSOCIATION', '协会'],
            ['DINSTITUTION', '院校'],
            ['HTHEATER', '剧院'],
            ['HMUSEUM', '博物馆'],
            ['BCOMPANY', '公司']],
        'SHOW':[['FSHOW', '展会'],
            ['ASHOW', '展会'],
            ['DSHOW', '展会']]
}

VOLUME_AFFECT_OWN = 0x01
VOLUME_AFFECT_COL = 0x02
VOLUME_AFFECT_DEF = 0x03

def _get_mtype(key):
    for s in VOL_TYPES_SUB.keys():
        if key == s:return s
        for t in VOL_TYPES_SUB[s]:
            if key == t[0]:
                return s
    return None

def _get_perm_key(value):
    for k, v in PERM_CLASS.items():
        if value == v:
            return k
    return None

def get_sub(t=None, p=None):
    if (t is None) and (p is None):
        return []
    elif (t is not None) and (p is None):
        return VOL_TYPES_SUB[t] if (t in VOL_TYPES_SUB) else []
    elif (t is None) and (p is not None):
        return []#VOL_PROPERTY_SUB[p] if (p in VOL_PROPERTY_SUB) else []
    else:
        return filter(lambda x:x in VOL_PROPERTY_SUB[p], VOL_TYPES_SUB[t])

def get_cn(m=None, p=None, s=None):
    if m is not None:
        for mt in VOL_TYPES_MAIN:
            if m == mt[0]:return mt[1]
    if p is not None:
        for pt in VOL_PROPERTY_MAIN:
            if p == pt[0]:return pt[1]
    if s is not None:
        if s[0] == 'F':
            sts = VOL_TYPES_SUB['FASHION']
        elif s[0] == 'A':
            sts = VOL_TYPES_SUB['ART']
        elif s[0] == 'D':
            sts = VOL_TYPES_SUB['DESIGN']
        elif s[0] == 'H':
            sts = VOL_TYPES_SUB['HUMAN']
        elif s[0] == 'B':
            sts = VOL_TYPES_SUB['BRAND']
        else:
            return None
        for st in sts:
            if s == st[0]:return st[1]
    return None

class Volume(object):
    def __init__(self, api=None):
        self._api = VolumeAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class VolumeAPI(API):
    def __init__(self):
        DB_CON.register([VolumeDoc])
        datastore = DB_CON[DB_NAME]
        col_name = VolumeDoc.__collection__
        collection = datastore[col_name]
        doc = collection.VolumeDoc()
        self.capi = CollectAPI()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def save(self, owner, name, prop, maintype, subtype, **kwargs):
        if kwargs.has_key('male'):
            kwargs['male'] = kwargs['male'] == u'male'
        if kwargs.has_key('year'):
            kwargs['year'] = datetime.strptime(kwargs['year'], DATE_FORMAT)
        if kwargs.has_key('live'):
            kwargs['live'] = int(kwargs['live'])
        if kwargs.has_key('grade'):
            kwargs['grade'] = int(kwargs['grade'])
        if kwargs.has_key('nexus'):
            kwargs['nexus'] = int(kwargs['nexus'])
        return super(VolumeAPI, self).create(owner=owner, name=name, prop=prop, maintype=maintype, subtype=subtype, **kwargs)
        
    def edit(self, id, **kwargs):
        if kwargs.has_key('male'):
            kwargs['male'] = kwargs['male'] == u'male'
        if kwargs.has_key('year'):
            kwargs['year'] = datetime.strptime(kwargs['year'], DATE_FORMAT)
        if kwargs.has_key('live'):
            kwargs['live'] = int(kwargs['live'])
        if kwargs.has_key('grade'):
            kwargs['grade'] = int(kwargs['grade'])
        if kwargs.has_key('nexus'):
            kwargs['nexus'] = int(kwargs['nexus'])
        return super(VolumeAPI, self).edit(id, **kwargs)
    
    def remove(self, id):
        return super(VolumeAPI, self).remove(id)
    
    def _affect(self, cuid, owner, rid):
        if (cuid == owner):
            r = VOLUME_AFFECT_OWN
        elif self.capi.exist(rid):
            r = VOLUME_AFFECT_COL
        else:
            r = VOLUME_AFFECT_DEF
        return r
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        output_map = lambda i: {'vid':i['_id'], 'added_id':i['added_id'], 'affect':self._affect(cuid, i['owner'], i['_id']), 'logo':i.get('logo', None), 'name':i.get('name', '无名'), 'builder':i['added'].get('builder', None), 'prop':i.get('prop', None), 'prop_cn':get_cn(p=i.get('prop', None)), 'maintype':i.get('maintype', None), 'maintype_cn':get_cn(m=i.get('maintype', None)), 'subtype':i.get('subtype', None), 'subtype_cn':get_cn(s=i.get('subtype', None)), 'live':i.get('live', None), 'male':i.get('male', None), 'male_cn':'男' if i.get('male', None) else '女', 'year':datetime.strftime(i.get('year', datetime.now()), DATE_FORMAT), 'website':i['added'].get('website', None), 'agency':i.get('agency', None), 'grade':i.get('grade', None), 'nexus':i.get('nexus', None), 'intro':i['added'].get('intro', None), 'about':i['added'].get('about', None), 'market':i['added'].get('market', None), 'created':self._escape_created(now, i['created'])}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def _deal_created(self, dtime):
        if dtime == 'day':
            year = datetime.now().year
            month = datetime.now().month
            day = datetime.now().day
            return {'created':{'$gt':datetime(year=year,month=month,day=day)}}
        elif dtime == 'week':
            t = datetime.today()
            n = datetime.now() - timedelta(days=t.weekday())
            year, month, day = n.year, n.month, n.day
            return {'created':{'$gt':datetime(year=year,month=month,day=day)}}
        elif dtime == 'month':
            year = datetime.now().year
            month = datetime.now().month
            return {'created':{'$gt':datetime(year=year,month=month,day=1)}}
        else:
            return {}
    
    def page_own(self, cuid=DEFAULT_CUR_UID, owner=None, perm=None, name=None, prop=None, live=None, agency=None, tags=[], grade=None, nexus=None, male=None, year_interval=(None, None), page=1, pglen=10, limit=20, order_by='added_id', order=-1):
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
        ### year_interval
        kwargs['page']=page
        kwargs['pglen']=pglen
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(VolumeAPI, self).page(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l, r[2])
        else:
            return (False, r[1])
        
    def page(self, cuid=DEFAULT_CUR_UID, owner=None, perm=None, created=None, name=None, prop=None, maintype=None, subtype=None, live=None, agency=None, tags=[], grade=None, nexus=None, male=None, year_interval=(None, None), page=1, pglen=10, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        pmlist = [PERM_CLASS['SUPEROR'], PERM_CLASS['MANAGER']]
        if isinstance(perm, tuple):perm = [perm]
        if subtype:
            mtype_l = ['FASHION', 'ART', 'DESIGN', 'HUMAN', 'BRAND']
            subkey = _get_mtype(subtype)
            pmlist.append(PERM_CLASS.get(subkey, ''))
            if perm and owner:
                for p in perm:
                    if p in pmlist:
                        owner=None
                        break
                if owner:kwargs['owner']=owner
            
            if subtype in mtype_l:
                kwargs['maintype']=subtype
            elif subtype == 'INSTITUTIONS':
                kwargs['subtype']={'$in': [u'FINSTITUTIONS', u'AINSTITUTION', u'DINSTITUTION']}
            elif subtype == 'ASSOCIATION':
                kwargs['subtype']={'$in': [u'FASSOCIATION', u'AASSOCIATION', u'DASSOCIATION']}
            elif subtype == 'MAGAZINE':
                kwargs['subtype']={'$in': [u'FMAGAZINE']}
            else:
                kwargs['subtype']=subtype
        elif perm is not None:
            flag = False
            mtypelist = []
            for p in perm:
                if p not in pmlist:
                    flag = True
                mtypelist.append(_get_perm_key(p))
            if flag:
                kwargs['maintype'] = {'$in':mtypelist}
        if created:kwargs.update(self._deal_created(created))
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
        ### year_interval
        kwargs['page']=page
        kwargs['pglen']=pglen
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        print kwargs
        r = super(VolumeAPI, self).page(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l, r[2])
        else:
            return (False, r[1])

class CollectAPI(API):
    def __init__(self):
        DB_CON.register([CollectDoc])
        datastore = DB_CON[DB_NAME]
        col_name = CollectDoc.__collection__
        collection = datastore[col_name]
        doc = collection.CollectDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def exist(self, rid):
        try:
            return self.collection.one({'refer_id': rid}) is not None
        except Exception, e:
            logging.info(e)
            raise Exception

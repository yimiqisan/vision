#!/usr/bin/env python
# encoding: utf-8
"""
pstore.py

Created by 刘 智勇 on 2012-06-21.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
import gridfs
from mongokit import Connection, ObjectId
import Image
import StringIO

PIC_DB_NAME = 'vpicture'
PIC_DB_CON = Connection(host='localhost', port=27017)


class Pstore(object):
    def __init__(self):
        db = PIC_DB_CON[PIC_DB_NAME]
        self.fs = gridfs.GridFS(db)
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None
    
    def put(self, data, **kwargs):
        ''' 保存图片 '''
        return self.fs.put(data, **kwargs)
    
    def get_by_id(self, id):
        ''' 获取图片 '''
        if not isinstance(id, ObjectId):id=ObjectId(id)
        return self.fs.get(id)
    
    def remove(self, fn):
        ''' 删除图片 '''
        try:
            id = self.fs.get_version(filename=fn)._id
            self.fs.delete(id)
        except Exception, e:
            return False
        return True
    
    def get_version(self, filename=None, version=-1, **kwargs):
        ''' 根据版本号获取图片 '''
        try:
            return (True, self.fs.get_version(filename=filename, **kwargs).read())
        except Exception, e:
            return (False, e)
        
    def get_last_version(self, filename=None, **kwargs):
        ''' 获取扮作新版本的图片 '''
        try:
            return (True, self.fs.get_last_version(filename=filename, **kwargs).read())
        except Exception, e:
            return (False, e)
    
    def list(self):
        ''' 获取图片列表 '''
        return self.fs.list()
    
    
class ImageProcessor(object):
    def __init__(self, uid=None):
        self.uid = uid
        self.sz_l = [300, 100]
        self.p = Pstore()
        self.max_sz = 600
    
    def _get_attr(self, im):
        if not im:
            log.error("Invalid parameter. [im]: %s" % im)
            return False
        args = {}
        args["size"] = "%dx%d" % (im.columns(), im.rows())
        args["content_type"] = "image/" + im.magick().lower()
        return args
        
    def _get_fn(self, suffix=None):
        uu = uuid.uuid4().hex
        return uu+'_'+str(suffix) if suffix else uu
        
    def _thumbnail(self, im_obj, size):
        o = StringIO.StringIO()
        try:
            im_obj.thumbnail((size, size), Image.ANTIALIAS)
            im_obj.save(o, 'JPEG')
        except Exception, e:
            try:
                im_obj.save(o, 'GIF')
            except Exception, e:
                print 'save eror'
                return None
        return o.getvalue()
        
    def process(self, data):
        ofn = self._get_fn()
        im = Image.open(StringIO.StringIO(data))
        if (im.size[0]>self.max_sz)or(im.size[1]>self.max_sz):
            data = self._thumbnail(im, self.max_sz)
        if data is None:return None
        self.p.put(data, filename=ofn, size=-1)
        for sz in self.sz_l:
            fn = ofn+'_'+str(sz)
            data = self._thumbnail(im, sz)
            self.p.put(data, filename=fn)
        return ofn
    
    def remove(self, filename):
        self.p.remove(filename)
        for sz in self.sz_l:
            fn = filename+'_'+str(sz)
            self.p.remove(fn)
        return True
    
    def display(self, fn, version=None, **kwargs):
        if version is None:
            r = self.p.get_last_version(filename=fn, **kwargs)
        else:
            kwargs['version'] = version
            r = self.p.get_version(filename=fn, **kwargs)
        return r[1] if r[0] else ''

class AvatarProcessor(ImageProcessor):
    def __init__(self, uid=None):
        self.uid = uid
        self.sz_l = [100, 80, 50, 30]
        self.p = Pstore()
        self.max_sz = 600
    
    def _get_fn(self, suffix=None):
        return self.uid+'_'+str(suffix) if suffix else self.uid

class AttachProcessor(ImageProcessor):
    pass

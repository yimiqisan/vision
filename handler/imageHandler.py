#!/usr/bin/env python
# encoding: utf-8
"""
imageHandler.py

Created by 刘 智勇 on 2012-06-21.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from vision.apps.pstore import AvatarProcessor, AttachProcessor
from vision.apps.tools import session


class AvatarHandler(BaseHandler):
    '''头像图片显示处理
    '''
    def get(self, fn=None):
        if not fn:return
        v = self.get_argument('v', None)
        p=AvatarProcessor()
        kwargs = {}
        kwargs['version']=v
        self.write(p.display(fn, **kwargs))

class AttachHandler(BaseHandler):
    '''图片显示处理
    '''
    def get(self, fn=None):
        if not fn:return
        v = self.get_argument('v', None)
        p=AttachProcessor()
        kwargs = {}
        kwargs['version']=v
        d = p.display(fn, **kwargs)
        self.write(d)

class UploadImageHandler(BaseHandler):
    '''图片上传
    '''
    def get(self):
        pid = self.get_argument("pid", None)
        self.render('upload_image.html', pid=pid)
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        p=AvatarProcessor(uid)
        f=self.request.files['upload'][0]
        r = p.process(f['body'])
        self.redirect('/image/upload?pid='+r)
    
class AjaxImageHandler(BaseHandler):
    '''ajax方式显示图片
    '''
    @session
    def post(self):
        uid = self.get_argument('uid', None)
        p=AttachProcessor()
        f = self.request.files['upload'][0]
        r = p.process(f['body'])
        return self.write(r)

class AjaxImageDeleteHandler(BaseHandler):
    '''ajax方式删除图片
    '''
    @session
    def post(self):
        uid = self.SESSION['uid']
        pid = self.get_argument('pid', None)
        p=AttachProcessor()
        r = p.remove(pid)
        return self.write({'ret':'ok'})

class AjaxImageCheckHandler(BaseHandler):
    '''ajax方式检测图片
    '''
    def post(self):
        return True

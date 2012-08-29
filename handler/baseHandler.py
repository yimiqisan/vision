#!/usr/bin/env python
# encoding: utf-8
"""
base.py

Created by 刘 智勇 on 2012-06-13.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from tornado.web import RequestHandler
from vision.apps.tools import session
from vision.config import DB_CON

class BaseHandler(RequestHandler):
    '''处理基类
    '''
    @property
    def db(self):
        '''数据库
        '''
        return DB_CON
        
    @property
    def cache(self):
        '''系统缓存
        '''
        return self.settings["cache_engine"]
    
    @session
    def get_current_user(self):
        '''获取用户名
        '''
        return self.SESSION['nick']
    
    @session
    def render(self, template_name, **kwargs):
        '''网页渲染方法
        '''
        kwargs['uid'] = self.SESSION['uid']
        kwargs['ulogo'] = self.SESSION['ulogo']
        kwargs['perm'] = self.SESSION['perm']
        kwargs['warning'] = kwargs.get('warning', None)
        super(BaseHandler, self).render(template_name, **kwargs)
    
    @session
    def render_alert(self, msg, **kwargs):
        '''错误提示
        '''
        kwargs['alert']=msg
        self.render('alert.html', **kwargs)
    

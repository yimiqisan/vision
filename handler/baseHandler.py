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
    @property
    def db(self):
        return DB_CON
        
    @property
    def cache(self):
        return self.settings["cache_engine"]
    
    @session
    def get_current_user(self):
        return self.SESSION['nick']
    
    @session
    def render(self, template_name, **kwargs):
        kwargs['uid'] = self.SESSION['uid']
        kwargs['ulogo'] = self.SESSION['ulogo']
        kwargs['perm'] = self.SESSION['perm']
        kwargs['warning'] = kwargs.get('warning', None)
        super(BaseHandler, self).render(template_name, **kwargs)
    
    @session
    def render_alert(self, msg, **kwargs):
        kwargs['alert']=msg
        self.render('alert.html', **kwargs)
    

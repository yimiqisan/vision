#!/usr/bin/env python
# encoding: utf-8
"""
config.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import os
import redis
from mongokit import Connection
import uimethods

#config settings
settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "htmls"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        login_url="/",
        autoescape="xhtml_escape",
        debug=True,
        ui_methods=uimethods,
        cache_engine=redis.Redis(host='localhost', port=6379, db=1),
)

ADMIN = {'admin': ('admin', u'57138d461d7343c685c15e9e6d3bd9ef')}

PERM_CLASS = {
    'SUPEROR':      (0x01, "超级管理员"),
    'MANAGER':      (0x02, "管理员"),
    
    'EDITOR':       (0x10, "编辑"),
    
    'PROJECTOR':    (0x20, "项目创建者"),
    'RELATION':     (0x21, "项目相关人员"),
    
    'FASHION':      (0x30, "时尚"),
    'FDESIGNER':    (0x31, "设计师"),
    'FPHOTOGRAPHER':(0x32, "摄影师"),
    'FSTYLISTS':    (0x33, "造型师"),
    'FMAKEUP':      (0x34, "化妆师"),
    'FMODEL':       (0x35, "模特"),
    'FBLOGER':      (0x36, "博主"),
    'FARTIST':      (0x37, "艺术家"),
    'FMAGAZINE':    (0x38, "杂志"),
    'FASSOCIATION': (0x39, "协会"),
    'FINSTITUTIONS':(0x3a, "院校"),
    'FSHOW':        (0x3b, "展会"),
    
    'ART':          (0x40, "艺术"),
    'APAINTING':    (0x41, "绘画"),
    'AEQUIPMENT':   (0x42, "装置"),
    'ASCULPTURE':   (0x43, "雕塑"),
    'AIMAGE':       (0x44, "影像"),
    'AMULTIMEDIA':  (0x45, "多媒体"),
    'AASSOCIATION': (0x46, "协会"),
    'AINSTITUTION': (0x47, "院校"),
    'ASHOW':        (0x48, "展会"),
    
    'DESIGN':       (0x50, "设计"),
    'DBUILDING':    (0x51, "建筑"),
    'DINDOOR':      (0x52, "室内"),
    'DPRODUCT':     (0x53, "产品"),
    'DFLAT':        (0x54, "平面"),
    'DMUTILMEDIA':  (0x55, "多媒体"),
    'DASSOCIATION': (0x56, "协会"),
    'DINSTITUTION': (0x57, "院校"),
    'DSHOW':        (0x58, "展会"),
    
    'HUMAN':        (0x60, "人文"),
    'HPERFORMER':   (0x61, "表演者"),
    'HTHEATER':     (0x62, "剧院"),
    'HMUSEUM':      (0x63, "博物馆"),
    
    'BRAND':        (0x70, "品牌"),
    'BMEDIAPEOPLE': (0x71, "媒体人"),
    'BCOMPANY':     (0x72, "公司"),
    
    'NORMAL':       (0x90, "游客"),
}


#mongodb settings
DB_NAME = 'vision'
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DB_CON = Connection(host=MONGO_HOST, port=MONGO_PORT)

#session initialize settings
SESSION_SET = {
    "SESSION_EXPIRE_TIME": 86400,    # sessions are valid for 86400 seconds (24 hours)
    "REDIS_URL": {'ip': 'localhost', 'port': 6379, 'db': 0, },
}

#loggging config
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_CUR_UID = '948a55d68e1b4317804e4650a9505641'

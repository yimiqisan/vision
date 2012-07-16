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

#import uimethods, uimodules


#config settings
settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "htmls"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        login_url="/account/login",
        autoescape="xhtml_escape",
        debug=True,
        cache_engine=redis.Redis(host='localhost', port=6379, db=1),
)

PERM_CLASS = {
    'SUPEROR':      0x01,
    'MANAGER':      0x02,
    
    'EDITOR':       0x10,
    
    'PROJECTOR':    0x20,
    'RELATION':     0x21,
    
    'FASHION':      0x30,
    'FDESIGNER':    0x31,
    'FPHOTOGRAPHER':0x32,
    'FSTYLISTS':    0x33,
    'FMAKEUP':      0x34,
    'FMODEL':       0x35,
    'FBLOGER':      0x36,
    'FARTIST':      0x37,
    'FMAGAZINE':    0x38,
    'FASSOCIATION': 0x39,
    'FINSTITUTIONS':0x3a,
    'FSHOW':        0x3b,
    
    'ART':          0x40,
    'APAINTING':    0x41,
    'AEQUIPMENT':   0x42,
    'ASCULPTURE':   0x43,
    'AIMAGE':       0x44,
    'AMULTIMEDIA':  0x45,
    'AASSOCIATION': 0x46,
    'AINSTITUTION': 0x47,
    'ASHOW':        0x48,
    
    'DESIGN':       0x50,
    'DBUILDING':    0x51,
    'DINDOOR':      0x52,
    'DPRODUCT':     0x53,
    'DFLAT':        0x54,
    'DMUTILMEDIA':  0x55,
    'DASSOCIATION': 0x56,
    'DINSTITUTION': 0x57,
    'DSHOW':        0x58,
    
    'HUMAN':        0x60,
    'HPERFORMER':   0x61,
    'HTHEATER':     0x62,
    'HMUSEUM':      0x63,
    
    'BRAND':        0x70,
    'BMEDIAPEOPLE': 0x71,
    'BCOMPANY':     0x72,
    
    'NORMAL':       0x90,
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

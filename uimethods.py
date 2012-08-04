#!/usr/bin/env python
# encoding: utf-8
"""
uimethods.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

#from huwai.apps.perm import PERM_CLASS

def ifNone(handler, v=None):
    return v if v else ''

def truncate(handler, v, length=100):
    return v[:length]

def verify(handler, perm, reference):
    if isinstance(reference, int):
        return perm == reference
    elif isinstance(reference, list):
        return (perm in reference)
    elif isinstance(reference, dict):
        s=reference.get('start', 0x00)
        e=reference.get('end', 0x99)
        return (s <= perm <= e)
    return False

def list2txt(handler, v=None):
    if isinstance(v, list):
        return ','.join(map(lambda x: x[1], v))
    elif isinstance(v, unicode) or isinstance(v, str):
        return v
    return ''

def dict2txt(handler, v=None):
    if isinstance(v, dict):
        return ''.join(v.values())

def cntDict(handler, l, **kwargs):
    cnt = 0
    for i in l:
        plus = True
        for k, v in kwargs.items():
            if i.get(k, None) != v:
                plus = False
        if plus:cnt += 1
    return cnt

def abstract(handler, c, n=100):
    import re
    s = re.sub(r'</?\w+[^>]*>','',c)
    s = s.replace(' ', '')
    if (len(s) > n):
        return s[:n-3] + '...'
    else:
        return s[:n]

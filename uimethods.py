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

def affect(handler, affect, reference):
    if isinstance(reference, int):
        if isinstance(affect, list):
            for a in affect:
                if a == reference:return True
        else:
            return affect == reference
    elif isinstance(reference, list):
        if isinstance(affect, list):
            for a in affect:
                if a in reference:return True
        else:
            return (affect in reference)
    elif isinstance(reference, dict):
        s=reference.get('start', 0x00)
        e=reference.get('end', 0x99)
        if isinstance(affect, list):
            for a in affect:
                if (s <= a <= e):return True
        else:
            return (s <= affect <= e)
    return False

def verify(handler, perm, reference):
    if isinstance(reference, int):
        if isinstance(perm, list):
            for p in perm:
                if p[0] == reference:return True
        else:
            return perm[0] == reference
    elif isinstance(reference, list):
        if isinstance(perm, list):
            for p in perm:
                if p[0] in reference:return True
        else:
            return (perm[0] in reference)
    elif isinstance(reference, dict):
        s=reference.get('start', 0x00)
        e=reference.get('end', 0x99)
        if isinstance(perm, list):
            for p in perm:
                if (s <= p[0] <= e):return True
        else:
            return (s <= perm[0] <= e)
    return False

def list2txt(handler, v=None):
    if isinstance(v, tuple):
        return v[1]
    elif isinstance(v, list):
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

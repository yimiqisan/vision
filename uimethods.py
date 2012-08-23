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

def flist(handler, pid, l):
    return l
    cnt = len(l)
    if cnt == 0:return []
    idx = 0
    for i in xrange(0, cnt+1):
        if l[i]['pid'] == pid:
            idx = i
            break
    start = idx-2
    end = idx+3
    if start<0:
        end -= start
        start = 0
    if end > cnt:
        end = cnt
    if end - start < 5:
        start = max(0, end-5)
    return l[start:end]

def per_index(handler, pid, l):
    return 0
    cnt = len(l)
    idx = 0
    for i in xrange(0, cnt+1):
        if l[i]['pid'] == pid:
            idx = i
            break
    start = idx-2
    end = idx+3
    if start<0:
        end -= start
        start = 0
    if end > cnt:
        end = cnt
    if end - start < 5:
        start = max(0, end-5)
    return max(start, idx-1)

def next_index(handler, pid, l):
    return 0
    cnt = len(l)
    idx = 0
    for i in xrange(0, cnt+1):
        if l[i]['pid'] == pid:
            idx = i
            break
    start = idx-2
    end = idx+3
    if start<0:
        end -= start
        start = 0
    if end > cnt:
        end = cnt
    if (cnt-idx)<3:
        return min(4, cnt-1)
    else:
        return min(3, idx+1)

def build_params(handler, params):
    l = []
    for k, v in params.items():
        s = str(k)+'='+str(v)
        l.append(s)
    return '&'.join(l)

if __name__ == '__main__':
    #l = [{'pid':'a'}, {'pid':'b'}, {'pid':'c'}, {'pid':'d'}, {'pid':'e'}, {'pid':'f'}, {'pid':'g'}, {'pid':'h'}, {'pid':'i'}]
    #print next_index('handler', 'a', l)
    parms = {}#{'day':'today', 'people':'lzy', 'place':'bj'}
    print build_params('handler', parms)





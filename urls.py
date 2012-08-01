#!/usr/bin/env python
# encoding: utf-8
"""
urls.py

Created by 刘 智勇 on 2012-06-13.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from handler import *

handlers = [(r"/", RootHandler),
            (r"/login/", LoginHandler),
            (r"/logout/", LogoutHandler),
            
            (r"/space/", SpaceHandler),
            (r"/space/perm/", SpacePermHandler),
            (r"/space/new/", SpaceNewHandler),
            (r"/space/collect/", SpaceCollectHandler),
            (r"/space/project/", SpaceProjectHandler),
            
            (r"/perm/", PermHandler),
            (r"/perm/new/", PermNewHandler),
            (r"/perm/(.{32})/remove/", PermRemoveHandler),
            (r"/perm/(.{32})/edit/", PermEditHandler),
            
            (r"/volume/new/", VolumeNewHandler),
            (r"/volume/(.{32})/remove/", VolumeRemoveHandler),
            (r"/volume/(.{32})/edit/", VolumeEditHandler),
            (r"/volume/(.{32})/", VolumeHandler),
            (r"/volume/", VolumeListHandler),
            (r"/a/volume/type/", AjaxVolumeTypeHandler),
            
            (r"/item/([a-z]+)/(.{32})/new/", ItemNewHandler),
            (r"/item/([a-z]+)/(.{32})/preview/", ItemPreviewHandler),
            (r"/item/(.{32})/remove/", ItemRemoveHandler),
            (r"/item/(.{32})/edit/", ItemEditHandler),
            (r"/item/(.{32})/", ItemHandler),
            (r"/a/item/(.{32})/", AjaxItemHandler),
            
            (r"/project/new/", ProjectNewHandler),
            (r"/project/(.{32})/remove/", ProjectRemoveHandler),
            (r"/project/(.{32})/edit/", ProjectEditHandler),
            (r"/project/(.{32})?/?", ProjectHandler),
            
            (r"/image/upload", UploadImageHandler),
            (r"/image/avatar/?(\w*)", AvatarHandler),
            (r"/image/attach/?(\w*)", AttachHandler),
            (r"/a/image/?", AjaxImageHandler),
            (r"/a/image/delete/", AjaxImageDeleteHandler),
            (r"/a/image/check/?", AjaxImageCheckHandler),
            
            (r".*", Error404Handler),
            ]

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
            (r"/a/login/", AjaxLoginHandler),
            (r"/logout/", LogoutHandler),
            
            (r"/space/perm/", SpacePermHandler),
            (r"/space/new/", SpaceNewHandler),
            (r"/space/collect/", SpaceCollectHandler),
            (r"/space/project/", SpaceProjectHandler),
            (r"/space/?([a-z]*)/", SpaceHandler),
            
            (r"/perm/", PermHandler),
            (r"/perm/new/", PermNewHandler),
            (r"/perm/(.{32})/remove/", PermRemoveHandler),
            (r"/perm/(.{32})/edit/", PermEditHandler),
            (r"/perm/(.{32})/cpwd/", PermCpwdHandler),
            (r"/a/staff/", AjaxStaffListHandler),
            
            (r"/volume/new/", VolumeNewHandler),
            (r"/volume/(.{32})/remove/", VolumeRemoveHandler),
            (r"/volume/(.{32})/edit/", VolumeEditHandler),
            (r"/volume/(.{32})/", VolumeHandler),
            (r"/volume/?([a-z]*)/", VolumeListHandler),
            (r"/a/volume/type/", AjaxVolumeTypeHandler),
            
            (r"/collect/(.{32})/remove/", CollectRemoveHandler),
            (r"/collect/(.{32})/", CollectItemHandler),
            (r"/collect/?([a-z]*)/", CollectHandler),
            (r"/a/collect/(.{32})/add/", AjaxCollectAddHandler),
            (r"/a/collect/(.{32})/del/", AjaxCollectDelHandler),
            (r"/collect/list/", CollectListHandler),
            
            (r"/item/([a-z]+)/(.{32})/new/", ItemNewHandler),
            (r"/item/([a-z]+)/(.{32})/preview/", ItemPreviewHandler),
            (r"/item/(.{32})/remove/", ItemRemoveHandler),
            (r"/item/(.{32})/edit/", ItemEditHandler),
            (r"/item/(.{32})/", ItemHandler),
            (r"/a/item/(.{32})/", AjaxItemHandler),
            (r"/a/item/(.{32})/paste/", AjaxItemPasteHandler),
            
            (r"/project/new/", ProjectNewHandler),
            (r"/project/(.{32})/remove/", ProjectRemoveHandler),
            (r"/project/(.{32})/edit/", ProjectEditHandler),
            (r"/project/(.{32})?/?", ProjectHandler),
            (r"/project/(.{32})/edit/", ProjectEditHandler),
            (r"/project/(.{32})/build/", ProjectBuildHandler),
            (r"/project/(.{32})/stick/", ProjectStickHandler),
            
            (r"/a/reply/", AjaxReplyHandler),
            (r"/a/reply/new/", AjaxNewReplyHandler),
            (r"/a/reply/remove/", AjaxRemoveHandler),
            
            (r"/image/upload", UploadImageHandler),
            (r"/image/avatar/?(\w*)", AvatarHandler),
            (r"/image/attach/?(\w*)", AttachHandler),
            (r"/a/image/?", AjaxImageHandler),
            (r"/a/image/delete/", AjaxImageDeleteHandler),
            (r"/a/image/check/?", AjaxImageCheckHandler),
            
            (r".*", Error404Handler),
            ]


            


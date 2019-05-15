# -*- coding: utf-8 -*-
# @Time    : 2018/pet/6/pet/7 下午4:18
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : urls.py
# @Software: PyCharm

from Handlers import MTTRegisterHandler
from Handlers import MTTLoginHandler
from Handlers import MTTFileUploadHandler
from Handlers import MTTUploadTokenHandler
from Handlers import MTTPublishDynamicHandler
from Handlers import MTTDynamicListHandler
from Handlers import MTTPublishCommentHandler
from Handlers import MTTCommentListHandler
from Handlers import MTTPublishReplyHandler
from Handlers import MTTReplyListHandler
from Handlers import MTTCommentReplyListHandler
from Handlers import MTTChangeAvatarHandler
from Handlers import MTTChangeUsernameHandler
from Handlers import MTTChangePasswordHandler
from Handlers import MTTAESHandler
from Handlers import MTTRegisterDeviceHandler
from Handlers import MTTDeviceDynamicListHandler
from Handlers import MTTReportAbuseHandler
from Handlers import MTTPraiseHandler
from Handlers import MTTPushHandler




handlers = [
    (r'/pet/register', MTTRegisterHandler.MTTRegisterHandler),
    (r'/pet/register_device', MTTRegisterDeviceHandler.MTTRegisterDeviceHandler),
    (r'/pet/login', MTTLoginHandler.MTTLoginHandler),
    (r'/pet/upload', MTTFileUploadHandler.MTTFileUploadHandler),
    (r'/pet/upload_token', MTTUploadTokenHandler.MTTUploadTokenHandler),
    (r'/pet/publish_dynamic', MTTPublishDynamicHandler.MTTPublishDynamicHandler),
    (r'/pet/dynamic_list', MTTDynamicListHandler.MTTDynamicListHandler),
    (r'/pet/publish_comment', MTTPublishCommentHandler.MTTPublishCommentHandler),
    (r'/pet/comment_list', MTTCommentListHandler.MTTCommentListHandler),
    (r'/pet/publish_reply', MTTPublishReplyHandler.MTTPublishReplyHandler),
    (r'/pet/reply_list', MTTReplyListHandler.MTTReplyListHandler),
    (r'/pet/comment_reply_list', MTTCommentReplyListHandler.MTTCommentReplyListHandler),
    (r'/pet/change_avatar', MTTChangeAvatarHandler.MTTChangeAvatarHandler),
    (r'/pet/change_username', MTTChangeUsernameHandler.MTTChangeUsernameHandler),
    (r'/pet/change_password', MTTChangePasswordHandler.MTTChangePasswordHandler),
    (r'/pet/encryption', MTTAESHandler.MTTAESHandler),
    (r'/pet/device_dynamic_list', MTTDeviceDynamicListHandler.MTTDeviceDynamicListHandler),
    (r'/pet/report_abuse', MTTReportAbuseHandler.MTTReportAbuseHandler),
    (r'/pet/praise', MTTPraiseHandler.MTTPraiseHandler),
    (r'/pet/push', MTTPushHandler.MTTPushHandler),
]
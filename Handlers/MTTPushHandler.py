# -*- coding: utf-8 -*-
# @Time    : 2018/12/27 1:01 PM
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTPushHandler.py
# @Software: PyCharm

from Handlers import MTTBaseHandler
from PsuhManager.MTTPushNotificationManager import MTTPushNotificationManager

class MTTPushHandler(MTTBaseHandler.MTTBaseHandler):

    def push_noti(self):
        app_versions = ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]
        title = self.get_argument("title")
        subtitle = self.get_argument("subtitle")
        description = self.get_argument("description")
        push_body = self.get_argument("body")
        production_mode = self.get_argument("production_mode")

        notification = MTTPushNotificationManager()
        for (index, appverion) in enumerate(app_versions):
            notification.push_notification(description=description, push_body=push_body, app_version=appverion, title=title, subtitle=subtitle, production_mode=production_mode, ptype="broadcast")

    def get(self, *args, **kwargs):
        self.push_noti()

    def post(self, *args, **kwargs):
        self.push_noti()



# -*- coding: utf-8 -*-
# @Time    : 2018/12/27 2:40 PM
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTPushNotificationManager.py
# @Software: PyCharm
from .notification import AndroidNotification, IosNotification

key = "5b737e3ea40fa31a7b000721"
secret = "rj3j31g6gxl4xlsu8j4h1k8fstslvss2"
class MTTPushNotificationManager(object):

    def __init__(self):
        self.app_key = ""

    def push_notification(self, description, push_body, app_version, production_mode=True, title="", subtitle="", ptype="groupcast"):
        noti = IosNotification(app_key=key, master_secret=secret, ptype=ptype)
        noti.production_mode = production_mode
        noti.filter = {
            "where": {
                    "and": [{"app_version": app_version}]
                }
        }
        noti.sound = "default"
        noti.description = description
        noti.alert = {"title": title,
                      "subtitle": subtitle,
                      "body": push_body
                      }
        noti.send()

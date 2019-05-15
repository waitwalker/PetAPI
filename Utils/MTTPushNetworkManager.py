# -*- coding: utf-8 -*-
# @Time    : 2018/12/27 1:07 PM
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTPushNetworkManager.py
# @Software: PyCharm

import hashlib
import json
import time
import requests


class MTTPushNetworkManager(object):

    USER_AGENT = "Mozilla/5.0"
    HOST = "http://msg.umeng.com"
    UPLOAD_PATH = "/upload"
    POST_PATH = "/api/send"

    API_URL = "%s%s" % (HOST, POST_PATH)

    def __md5(self, s):
        if isinstance(s, str):
            m = hashlib.md5(s.encode())
        else:
            m = hashlib.md5(s)
        return m.hexdigest()

    def send(self, description, production_mode, push_type, pushed_body, title="", subtitle="",):

        appkey = "5b737e3ea40fa31a7b000721"
        payload = {"aps": {"alert": {"title": title,
                                   "subtitle": subtitle,
                                   "body": pushed_body
                                   },
                          "sound": "default"
                          }
                   }
        timestamp = str(int(time.time()))
        push_body = {"description": description,
                    "production_mode": production_mode,
                    "appkey": appkey,
                    "payload": payload,
                    "type": push_type,
                    "timestamp": timestamp
                    }

        post_body = json.dumps(push_body)
        sign = self.__md5('{}{}{}{}'.format('POST', self.API_URL, post_body, appkey))
        print("sign %s; postbody:%s" % (sign, post_body))
        #print sign, postBody
        r = requests.post(self.API_URL + '?sign=' + sign, data=post_body)
        #print r.status_code, r.text
        print("r.status_code %s; r.text:%s" % (r.status_code, r.text))
        return r

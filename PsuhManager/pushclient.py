# -*- coding: utf-8-*-
import hashlib
import json

import requests


class PushClientMixin(object):

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

    def send(self):
        postBody = json.dumps(self.to_json())
        sign = self.__md5('{}{}{}{}'.format('POST', self.API_URL, postBody, self.master_screte))
        print("sign %s; postbody:%s" % (sign, postBody))
        #print sign, postBody
        r = requests.post(self.API_URL + '?sign=' + sign, data=postBody)

        #print r.status_code, r.text
        # print("r.status_code %s; r.text:%s" % (r.status_code, r.text))


        return r

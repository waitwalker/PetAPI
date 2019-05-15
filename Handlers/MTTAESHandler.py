# -*- coding: utf-8 -*-
# @Time    : 2018/7/9 上午10:41
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTAESHandler.py
# @Software: PyCharm

from Handlers import MTTBaseHandler
from Security import MTTSecurityManager
from Crypto.Cipher import AES

class MTTAESHandler(MTTBaseHandler.MTTBaseHandler):

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):

        para = self.get_argument('encryption')

        # print("para:", para)

        de = self.security_manager.decrypt('6Q+ATrlrXHa309Ki2b0Png==')

        # print(de)



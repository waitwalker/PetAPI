# -*- coding: utf-8 -*-
# @Time    : 2018/7/6 下午2:41
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTSecurityManager.py
# @Software: PyCharm

import sys
from Crypto.Cipher import AES
import base64
from Crypto import Random

# padding算法
BS = AES.block_size # aes数据分组长度为128 bit
pad = lambda s: s + (BS - len(s) % BS) * chr(0)



class MTTSecurityManager(object):

    def __init__(self, key, iv, mode):

        if type(key) == list:
            key = bytes(key)

        if type(iv) == list:
            iv = bytes(iv)

        self.key = key
        self.mode = mode
        self.iv = iv

    def encrypt(self, content):

        """
        aes 加密 
        :param content: 原始内容 
        :return: 加密后结果  
        """
        # 生成随机初始向量IV
        # iv = Random.new().read(AES.block_size)
        # print("iv:", self.iv)
        # print("change to str:",str(self.iv))
        cryptor = AES.new(self.key, self.mode, self.iv)
        ciphertext = cryptor.encrypt(pad(content))
        # print("ciphertext:", ciphertext)
        return base64.encodebytes(self.iv + ciphertext)

    # 解密
    def decrypt(self, content):
        """
        :param content:加密串 
        :return: 解密结果 
        """
        # print(type(content))
        if type(content) == str:
            content = bytes(content.encode('utf-8'))
            # print("content:", content)
            # print("type:", type(content))
        content = base64.decodebytes(content)
        content = content[0:len(content)]
        cryptor = AES.new(self.key, self.mode, self.iv)
        text = cryptor.decrypt(content)
        if type(text) == bytes:
            after_decrypt = str(text.decode('utf-8'))
            if str.find(after_decrypt, '\n'):
                after_decrypt = after_decrypt.replace('\n', '')
            # print("after_decrypt:", after_decrypt)
            return after_decrypt
        else:
            return text



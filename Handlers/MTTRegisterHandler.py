# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 下午4:19
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTRegisterHandler.py
# @Software: PyCharm

# ***********************

# 注册接口

# ***********************

# 注册接口
# 字段
# phone:str
# username:str
# password:str
# header_photo:str 默认 header_photo_placeholder
# login_times:int 默认0
# user_type:int 用户类型, 默认0(低级)
# create_time:date

from Handlers import MTTBaseHandler
import datetime
import pymysql
import time
import uuid
import random
from Security import MTTSecurityManager
from Crypto.Cipher import AES


class MTTRegisterHandler(MTTBaseHandler.MTTBaseHandler):


    # 注册 post 请求
    def post(self, *args, **kwargs):
        self.handler_register()

    # 注册 get 请求
    def get(self, *args, **kwargs):
        self.handler_register()


    def handler_register(self):
        # 获取注册参数
        phone = self.get_argument('phone')
        username = self.get_argument('username')
        pa = self.get_argument('password')
        password = self.security_manager.decrypt(pa)
        time_a = self.get_argument('time')
        local = time.localtime(int(time_a))
        # print("current time :", local)
        # 格式化时间
        format_time = time.strftime("%Y-%m-%d %S", local)
        # print("formatter time:{} type:{}".format(format_time, type(format_time)))
        uid_tmp = str(uuid.uuid1())
        # print("uuid:{uid_tmp}".format(uid_tmp=uid_tmp))
        data = ""
        msg = ""
        kwargs_ = None
        cursor = self.cur

        sql = """\
                        SELECT * FROM user_info WHERE phone = '{phone}'
                        """
        db = self.db
        db.ping(reconnect=True)
        result = cursor.execute(sql.format(phone=phone))

        # result = self.query()
        # print("query user result:", result)

        if result == True:
            data = ""
            msg = "手机号已经被注册过了,请换一个再试"
            kwargs_ = {"data": data, "msg": msg}
            self.failure_response(**kwargs_)
        else:
            uid = self.get_uid(time=time_a)
            # print("user id:{uid}".format(uid=uid))
            insert_sql = """\
                            INSERT INTO user_info(uid,phone,username,header_photo,password,create_date) VALUES ('{uid}', '{phone}','{username}', '{header_photo}', '{password}','{create_date}')
                            """
            db = self.db
            db.ping(reconnect=True)
            insert_result = self.insert(
                insert_sql.format(uid=uid, phone=phone, username=username, header_photo="header_photo_placeholder", password=password, create_date=format_time))
            if insert_result == True:
                query_result = self.query(sql.format(phone=phone))
                if query_result == True:

                    try:
                        # fetch_one = results[0]
                        # data = fetch_one
                        msg = "注册成功"
                        kwargs_ = {"data": "", "msg": msg}
                        self.success_response(**kwargs_)
                    except pymysql.Error as error:
                        # print("user data insert failure):", error)
                        self.db.rollback()
                        self.failure_response(msg="注册失败", data="")

                else:
                    # print("user data insert failure2")
                    data = ""
                    msg = "注册失败"
                    kwargs_ = {"data": data, "msg": msg}
                    self.failure_response(**kwargs_)
            else:
                # print("user data insert failure3")
                data = ""
                msg = "注册失败"
                kwargs_ = {"data": data, "msg": msg}
                self.failure_response(**kwargs_)
            cursor.close()

    # 生成用户id
    def get_uid(self, time):
        tmp = int(random.randrange(10, 1000000000))
        uid = tmp + int(time)
        return uid



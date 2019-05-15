# -*- coding: utf-8 -*-
# @Time    : 2018/6/8 下午3:50
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTLoginHandler.py
# @Software: PyCharm

# ***********************

# 登录接口

# ***********************

from Handlers import MTTBaseHandler
import pymysql
from Crypto.Cipher import AES
from Security import MTTSecurityManager
from Utils import MTTPushNetworkManager

class MTTLoginHandler(MTTBaseHandler.MTTBaseHandler):
    my_db = pymysql.connect(
        host='localhost',
        user='root',
        password='etiantian',
        db='pet_database',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    def post(self, *args, **kwargs):
        self.handler_login()
        push_manager = MTTPushNetworkManager.MTTPushNetworkManager()
        push_manager.send(description="测试推送", push_type="broadcast", title="测试title", subtitle="测试subtitle",
                          production_mode="false", pushed_body="测试推送内容")

    def get(self, *args, **kwargs):
        self.handler_login()
        push_manager = MTTPushNetworkManager.MTTPushNetworkManager()
        push_manager.send(description="测试推送", push_type="broadcast", title="测试title", subtitle="测试subtitle", production_mode="false", pushed_body="测试推送内容")

    # 响应账号或密码错误
    def response_account_error(self,msg):
        data = ""
        the_msg = msg
        the_msg.encode('utf-8').decode('unicode_escape')
        kwargs_ = {"data": data, "msg": the_msg}
        self.failure_response(**kwargs_)

    # 处理登录
    def handler_login(self):

        phone = self.get_argument('phone')
        pa = self.get_argument('password')
        security_manager = MTTSecurityManager.MTTSecurityManager(self.aes_key, self.aes_iv, AES.MODE_CBC)
        password = security_manager.decrypt(pa)

        sql = """\
        SELECT * FROM user_info WHERE phone = '{phone}'
        """

        print(sql)

        # 操作游标
        cursor = self.cur

        try:
            db = self.db
            db.ping(reconnect=True)
            result = cursor.execute(sql.format(phone=phone))

            if result == True:
                # print("phone exist, can login")

                try:
                    db = self.db
                    db.ping(reconnect=True)
                    result = cursor.execute(sql.format(phone=phone))
                    if result == True:
                        results = cursor.fetchall()
                        user = results[0]
                        if str(user["phone"]) != str(phone) or str(user["password"]) != str(password):
                            self.response_account_error(msg="账号或密码错误")
                        else:
                            data = {"uid": user["uid"], "phone": user["phone"], "username": user["username"],
                                    "header_photo": user["header_photo"], "login_times": user["login_times"],
                                    "user_type": user["user_type"]}
                            msg = "登录成功"
                            self.success_response(data=data, msg=msg)

                    else:
                        self.response_account_error(msg="账号或密码错误")
                except pymysql.Error as error:
                    # print('login error:', error)
                    self.response_account_error(msg="账号或密码错误")

            else:
                self.response_account_error(msg="账号不存在")

        except pymysql.Error as error:
            # print("could not find phone", error)
            self.response_account_error(msg="账号不存在")
        cursor.close()

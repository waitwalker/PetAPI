# -*- coding: utf-8 -*-
# @Time    : 2018/6/12 下午4:34
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTUploadTokenHandler.py
# @Software: PyCharm

from Handlers import MTTBaseHandler
from qiniu import Auth
import pymysql
import redis

# 把token缓存起来,第一个用户或者超时时在生成


class MTTUploadTokenHandler(MTTBaseHandler.MTTBaseHandler):

    def get(self, *args, **kwargs):
        self.handler_login()

    def post(self, *args, **kwargs):
        self.handler_login()

    # 响应账号或密码错误
    def response_account_error(self, msg):
        data = ""
        the_msg = msg
        the_msg.encode('utf-8').decode('unicode_escape')
        kwargs_ = {"data": data, "msg": the_msg}
        self.failure_response(**kwargs_)

    def handler_login(self):

        phone = self.get_argument('phone')
        password = self.get_argument('password')
        password = self.security_manager.decrypt(password)

        sql = """\
           SELECT * FROM user_info WHERE phone = '{phone}'
           """
        db = self.db
        db.ping(reconnect=True)
        query_result = self.query(sql.format(phone=phone))
        if query_result == True:
            # print("phone exist,can get token")
            cursor = self.db.cursor()
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
                        token = None
                        msg = '获取token成功'
                        upload_file_token = self.redis.get('upload_file_token')
                        if upload_file_token == None:
                            access_key = '七牛access_key'
                            secret_key = '七牛secret_key'
                            bucket_name = '文件桶名称'

                            q = Auth(access_key=access_key, secret_key=secret_key)
                            token = q.upload_token(bucket=bucket_name, expires=36000)
                            # print("token:", token)
                            self.redis.set('upload_file_token', token, ex=36000)
                            expire = 36000
                            # print("get token from qiniu")
                        else:
                            token = upload_file_token
                            expire = self.redis.ttl("upload_file_token")
                            # print("token remaining time:", expire)
                            # print("get token from redis")
                        data = {"token": token, "expire": expire}
                        self.success_response(msg=msg, data=data)

                else:
                    self.response_account_error(msg="账号或密码错误")
                cursor.close()
            except pymysql.Error as error:
                # print('login error:', error)
                self.response_account_error(msg="账号或密码错误")

        else:
            self.response_account_error(msg="账号不存在")




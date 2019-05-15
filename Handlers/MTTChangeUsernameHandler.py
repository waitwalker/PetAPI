# -*- coding: utf-8 -*-
# @Time    : 2018/6/19 下午2:12
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTChangeUsernameHandler.py
# @Software: PyCharm

import pymysql
from Handlers import MTTBaseHandler

class MTTChangeUsernameHandler(MTTBaseHandler.MTTBaseHandler):

    def get(self, *args, **kwargs):
        self.handler_change_username()

    def post(self, *args, **kwargs):
        self.handler_change_username()

    # 处理更改用户名
    def handler_change_username(self):
        uid = self.get_argument('uid')
        password = self.get_argument('password')
        username = self.get_argument('username')
        password = self.security_manager.decrypt(password)
        query_user_sql = """\
        SELECT * FROM user_info WHERE uid='{uid}'
        """
        cursor_1 = self.cur
        try:
            db = self.db
            db.ping(reconnect=True)
            query_user_result = cursor_1.execute(query_user_sql.format(uid=uid))
            if query_user_result == True:
                user = cursor_1.fetchone()
                password_original = user['password']
                username_original = user['username']
                if str(password_original) == str(password):
                    if not str(username_original) == str(username):
                        update_user_sql = """\
                        UPDATE user_info SET username='{username}' WHERE uid='{uid}'
                        """
                        cursor_2 = self.cur
                        try:
                            db = self.db
                            db.ping(reconnect=True)
                            update_user_result = cursor_2.execute(update_user_sql.format(username=username, uid=uid))
                            self.db.commit()
                            if update_user_result == True:
                                data = {"username": username}
                                self.success_response(msg="更改用户名成功", data=data)
                                # print("update username success1")
                            else:
                                # print("update username failure1:")
                                self.db.rollback()
                                self.failure_response(msg="错误,更新用户名失败", data="")

                        except pymysql.Error as error:
                            # print("update username failure2:", error)
                            self.failure_response(msg="错误,更新用户名失败", data="")
                        cursor_2.close()
                    else:
                        # print("update username success, not update database")
                        data = {"username": username}
                        self.success_response(msg="更改用户名成功", data=data)
                else:
                    self.failure_response(msg="密码错误,请核查后重试", data="")
            else:
                self.failure_response(msg="用户不存在", data="")
            cursor_1.close()
        except pymysql.Error as error:
            # print("user not exist:", error)
            self.failure_response(msg="用户不存在", data="")





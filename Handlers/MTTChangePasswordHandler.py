# -*- coding: utf-8 -*-
# @Time    : 2018/6/19 下午3:12
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTChangePasswordHandler.py
# @Software: PyCharm

import pymysql
from Security import MTTSecurityManager
from Crypto.Cipher import AES

from Handlers import MTTBaseHandler

class MTTChangePasswordHandler(MTTBaseHandler.MTTBaseHandler):

    def get(self, *args, **kwargs):
        self.handler_change_password()

    def post(self, *args, **kwargs):
        self.handler_change_password()

    # 处理修改密码
    def handler_change_password(self):
        uid = self.get_argument('uid')
        pa = self.get_argument('password')
        password = self.security_manager.decrypt(pa)
        query_user_sql = """\
        SELECT * FROM user_info WHERE uid='{uid}'
        """

        # print("new password:", password)
        cursor_1 = self.cur
        try:
            db = self.db
            db.ping(reconnect=True)
            query_user_result = cursor_1.execute(query_user_sql.format(uid=uid))
            if query_user_result == True:
                user = cursor_1.fetchone()
                password_oririnal = user['password']
                # print("user:", user)
                if not str(password) == str(password_oririnal):
                    update_user_sql = """\
                    UPDATE user_info SET password='{password}' WHERE uid='{uid}'
                    """
                    cursor_2 = self.cur
                    try:
                        db = self.db
                        db.ping(reconnect=True)
                        update_user_result = cursor_2.execute(update_user_sql.format(password=password, uid=uid))
                        self.db.commit()
                        if update_user_result == True:
                            data = {"password": password}
                            self.success_response(msg="修改密码成功", data=data)
                            print("update password success")
                        else:
                            print("update password failure")
                            self.failure_response(msg="修改密码失败, 请稍后重试", data="")
                    except pymysql.Error as error:
                        print("update password failure:", error)
                        self.db.rollback()
                        self.failure_response(msg="更新密码失败", data=error)
                        cursor_2.close()
                else:
                    print("update password success, not update database")
                    data = {"password": password}
                    self.success_response(msg="修改密码成功", data=data)
            else:
                print("update password failure 2")
                self.failure_response(msg="修改密码失败, 用户不存在, 请稍后重试", data="")
            cursor_1.close()
        except pymysql.Error as error:
            print("update password failure 3:", error)
            self.failure_response(msg="错误,更新密码错误", data=error)

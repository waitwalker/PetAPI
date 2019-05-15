# -*- coding: utf-8 -*-
# @Time    : 2018/6/19 上午11:35
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTChangeAvatarHandler.py
# @Software: PyCharm

import pymysql
from Handlers import MTTBaseHandler
import time

class MTTChangeAvatarHandler(MTTBaseHandler.MTTBaseHandler):


    def get(self, *args, **kwargs):
        self.handler_change_avatar()

    def post(self, *args, **kwargs):
        self.handler_change_avatar()

    # 处理更换头像
    def handler_change_avatar(self):
        uid = self.get_argument('uid')
        attach = self.get_argument('attach')
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
                header_photo_original = user['header_photo']
                if not str(header_photo_original) == str(attach):
                    update_user_sql = """\
                                                            UPDATE user_info SET header_photo='{header_photo}' WHERE uid='{uid}'
                                                            """
                    cursor_2 = self.cur
                    try:
                        db = self.db
                        db.ping(reconnect=True)
                        update_user_result = cursor_2.execute(update_user_sql.format(header_photo=attach, uid=uid))
                        self.db.commit()
                        if update_user_result == True:
                            header_photo = attach
                            data = {"header_photo": header_photo}
                            self.success_response(msg="更换头像成功", data=data)
                            cursor_2.close()
                            # print("update avatar success")
                        else:
                            self.db.rollback()
                            # print("update avatar failure")
                            self.failure_response(msg="更新头像失败", data="")

                    except pymysql.Error as error:
                        # print("query user failure:", error)
                        self.db.rollback()
                        self.failure_response(msg="更新头像失败", data="")

                else:
                    header_photo = attach
                    data = {"header_photo": header_photo}
                    self.success_response(msg="更换头像成功", data=data)
                    # print("update avatar success2")
                cursor_1.close()
            else:
                self.failure_response(msg="用户不存在", data="")

        except pymysql.Error as error:
            # print("query user failure:", error)
            self.failure_response(msg="用户不存在", data="")


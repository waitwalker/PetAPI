# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 下午3:02
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTPublishReplyHandler.py
# @Software: PyCharm
from Handlers import MTTBaseHandler

import pymysql


class MTTPublishReplyHandler(MTTBaseHandler.MTTBaseHandler):

    def get(self, *args, **kwargs):
        self.handler_publish_reply()

    def post(self, *args, **kwargs):
        self.handler_publish_reply()

    # 处理回复
    def handler_publish_reply(self):


        from_uid = self.get_argument('from_uid')
        to_uid = self.get_argument('to_uid')
        comment_id = self.get_argument('comment_id')
        content = self.get_argument('content')
        time = self.get_argument('time')
        reply_id = int(comment_id) + int(time)

        query_user_sql = """\
                SELECT * FROM user_info WHERE uid = '{uid}'
                """
        query_comment_sql = """\
                SELECT * FROM comment_info WHERE comment_id = '{comment_id}'
                """

        cursor_1 = self.cur
        cursor_2 = self.cur
        cursor_3 = self.cur

        try:
            db = self.db
            db.ping(reconnect=True)
            query_user_from_result = cursor_1.execute(query_user_sql.format(uid=from_uid))
            cursor_1.close()
            query_user_to_result = cursor_2.execute(query_user_sql.format(uid=to_uid))
            cursor_2.close()
            query_comment_result = cursor_3.execute(query_comment_sql.format(comment_id=comment_id))
            cursor_3.close()

            if query_user_from_result == True and query_user_to_result == True and query_comment_result == True:

                reply_insert_sql = """\
                INSERT INTO reply_info(comment_id, reply_id, content, from_uid, to_uid, time) VALUES ('{comment_id}', '{reply_id}', '{content}', '{from_uid}', '{to_uid}', '{time}')
                """

                cursor_4 = self.cur
                try:
                    db = self.db
                    db.ping(reconnect=True)
                    cursor_4.execute(reply_insert_sql.format(comment_id=comment_id, reply_id=reply_id, content=content, from_uid=from_uid, to_uid=to_uid, time=time))
                    self.db.commit()
                    self.success_response(msg="回复成功", data="")
                except pymysql.Error as error:
                    # print("publish reply failure:", error)
                    self.db.rollback()
                    self.failure_response(msg="回复失败, 请稍后重试", data="")
                cursor_4.close()

            else:
                # print("user or comment id not exist1:")
                self.failure_response(msg="用户或者评论不存在", data="")

        except pymysql.Error as error:
            # print("user or comment id not exist 2:", error)
            self.failure_response(msg="用户或者评论不存在", data="")



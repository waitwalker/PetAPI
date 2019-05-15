# -*- coding: utf-8 -*-
# @Time    : 2018/12/24 2:16 PM
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTPraiseHandler.py
# @Software: PyCharm
from Handlers import MTTBaseHandler
import pymysql

class MTTPraiseHandler(MTTBaseHandler.MTTBaseHandler):

    def get(self, *args, **kwargs):
        self.handle_praise()

    def post(self, *args, **kwargs):
        self.handle_praise()

    def handle_praise(self):

        from_uid = self.get_argument('from_uid')
        topic_id = self.get_argument('topic_id')
        time = self.get_argument('time')
        query_sql = """\
                SELECT * FROM praise_info WHERE from_uid = '{from_uid}' AND topic_id = '{topic_id}'
                """
        praise_state = self.get_argument('praise_state')
        cursor = self.cur

        # 点赞
        if praise_state == '1':
            db = self.db
            db.ping(reconnect=True)
            result = cursor.execute(query_sql.format(from_uid=from_uid, topic_id=topic_id))
            if result == True:
                self.success_response(msg="点赞成功", data={})
            else:
                try:
                    insert_sql = """\
                    INSERT INTO praise_info(from_uid,topic_id, time) VALUES ('{from_uid}', '{topic_id}', '{time}')
                    """
                    try:
                        db = self.db
                        db.ping(reconnect=True)
                        insert_result = cursor.execute(insert_sql.format(from_uid=from_uid, topic_id=topic_id, time = time))
                        if insert_result == True:
                            self.success_response(msg="点赞成功", data="")
                            self.db.commit()
                        else:
                            self.failure_response(msg="点赞失败, 请重试", data="")

                    except pymysql.Error as error:
                        self.db.rollback()
                        self.failure_response(msg="点赞失败, 请重试", data="")

                except pymysql.Error as error:
                    self.failure_response(msg="点赞失败, 请重试", data="")
        else:
            #取消赞
            db = self.db
            db.ping(reconnect=True)
            result = cursor.execute(query_sql.format(from_uid=from_uid, topic_id=topic_id))
            if result == False:
                self.success_response(msg="取消点赞成功", data={})
            else:
                try:
                    delete_sql = """\
                DELETE FROM praise_info WHERE from_uid = '{from_uid}' AND topic_id = '{topic_id}'
                """
                    try:
                        db = self.db
                        db.ping(reconnect=True)
                        delete_result = cursor.execute(delete_sql.format(from_uid=from_uid, topic_id=topic_id))
                        if delete_result == True:
                            self.success_response(msg="取消点赞成功", data="")
                            self.db.commit()
                        else:
                            self.failure_response(msg="取消点赞失败, 请重试", data="")

                    except pymysql.Error as error:
                        self.db.rollback()
                        self.failure_response(msg="取消点赞失败, 请重试", data="")

                except pymysql.Error as error:
                    self.failure_response(msg="取消点赞失败, 请重试", data="")
        cursor.close()



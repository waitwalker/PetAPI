# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 上午11:01
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTPublishCommentHandler.py
# @Software: PyCharm

from Handlers import MTTBaseHandler
import pymysql
from PsuhManager.MTTPushNotificationManager import MTTPushNotificationManager

class MTTPublishCommentHandler(MTTBaseHandler.MTTBaseHandler):

    def push_noti(self):
        app_versions = ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]
        username = self.get_argument("username")
        notification = MTTPushNotificationManager()
        for (index, appverion) in enumerate(app_versions):
            notification.push_notification(description="提醒", push_body=username + ":  写了新的评论,赶快去查看吧!", app_version=appverion)

    def get(self, *args, **kwargs):
        self.push_noti()
        self.handler_publish_comment()

    def post(self, *args, **kwargs):
        self.push_noti()
        self.handler_publish_comment()

    # 处理发表评论
    def handler_publish_comment(self):

        # 预留 校验问题 同时校验 用户和topic_id  这里先不校验topic_id
        from_uid = self.get_argument('from_uid')
        topic_id = self.get_argument('topic_id')
        to_uid = self.get_argument('to_uid')
        time = self.get_argument('time')
        content = self.get_argument('content')
        comment_id = int(topic_id) + int(time)

        query_user_sql = """\
        SELECT * FROM user_info WHERE uid = '{uid}'
        """

        query_topic_sql = """\
        SELECT * FROM dynamic_info WHERE topic_id = '{topic_id}'
        """
        cursor = self.cur
        cursor2 = self.cur
        try:
            db = self.db
            db.ping(reconnect=True)
            query_result = cursor.execute(query_user_sql.format(uid=from_uid))
            query_topic_result = cursor2.execute(query_topic_sql.format(topic_id=topic_id))

            # print("query result: user:'{}', topic:'{}'".format(query_result, query_topic_result))
            cursor2.close()

            if query_result == True and query_topic_result == True:
                try:
                    comment_insert_sql = """\
                                    INSERT INTO comment_info(topic_id, from_uid, content, comment_id, time, to_uid) VALUES ('{topic_id}', '{from_uid}', '{content}', '{comment_id}', '{time}', '{to_uid}')
                                    """
                    cursor.execute(comment_insert_sql.format(topic_id=topic_id, from_uid=from_uid, content=content,
                                                             comment_id=comment_id, time=time, to_uid=to_uid))
                    self.db.commit()

                    # print("publish comment success")
                    self.success_response(msg="发表评论成功", data="")

                except pymysql.Error as error:
                    self.db.rollback()
                    # print("publish comment failure 1:", error)
                    self.failure_response(msg="发表评论失败", data="")
            else:
                # print("user not exist 1")
                self.failure_response(msg="用户或者动态主题不存", data="")

        except pymysql.Error as error:
            # print("user not exist 2:", error)
            self.failure_response(msg="用户不存在", data="")
        cursor.close()
        cursor2.close()



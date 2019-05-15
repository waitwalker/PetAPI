# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 下午4:20
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTReplyListHandler.py
# @Software: PyCharm

from Handlers import MTTBaseHandler
import pymysql


class MTTReplyListHandler(MTTBaseHandler.MTTBaseHandler):

    def get(self, *args, **kwargs):
        self.handler_reply_list()

    def post(self, *args, **kwargs):
        self.handler_reply_list()

    # 处理回复列表
    def handler_reply_list(self):
        uid = self.get_argument('uid')
        topic_id = self.get_argument('topic_id')

        cursor_1 = self.cur
        cursor_2 = self.cur
        query_user_sql = """\
                SELECT * FROM user_info WHERE uid = '{uid}'
                """
        query_topic_sql = """\
                SELECT * FROM dynamic_info WHERE topic_id = '{topic_id}'
                """
        try:
            db = self.db
            db.ping(reconnect=True)
            query_user_result = cursor_1.execute(query_user_sql.format(uid=uid))
            query_topic_result = cursor_2.execute(query_topic_sql.format(topic_id=topic_id))

            if query_topic_result == True and query_user_result == True:

                try:
                    query_reply_sql = """\
                            SELECT * FROM reply_info
                            """
                    cursor_3 = self.cur
                    cursor_3.execute(query_reply_sql.format())
                    reply_results = cursor_3.fetchall()
                    # print("all reply data:", reply_results)
                    reply_list = self.handler_reply_query_result(reply_results)
                    self.success_response(msg="获取回复列表成功", data=reply_list)
                    cursor_3.close()
                except pymysql.Error as error:
                    print("user or reply not exist 1:", error)

            else:
                # print("user or reply not exist 2:")
                self.failure_response(msg="用户或者回复不存在", data="")
        except pymysql.Error as error:
            # print("user or reply not exist 3:", error)
            self.failure_response(msg="用户或者回复不存在", data="")
        cursor_1.close()
        cursor_2.close()


    def handler_reply_query_result(self, results):

        reply_list = []
        for result in results:

            if type(result) == type({}):

                # print("query result:", result)
                from_uid = result['from_uid']
                to_uid = result['to_uid']
                content = result['content']
                comment_id = result['comment_id']
                time = result['time']

                cursor_1 = self.cur
                cursor_2 = self.cur
                query_user_sql = """\
                                    SELECT * FROM user_info WHERE uid = '{uid}'
                                    """
                try:
                    db = self.db
                    db.ping(reconnect=True)
                    query_user_from_result = cursor_1.execute(query_user_sql.format(uid=from_uid))
                    query_user_to_result = cursor_2.execute(query_user_sql.format(uid=to_uid))

                    if query_user_from_result == True and query_user_to_result == True:
                        fetch_from_result = cursor_1.fetchone()
                        fetch_to_result = cursor_2.fetchone()
                        from_username = fetch_from_result['username']
                        to_username = fetch_to_result['username']

                        reply = {"from_uid": from_uid, "from_username": from_username, "to_uid": to_uid, "to_username": to_username, "content": content, "comment_id": comment_id, "time": time}
                        reply_list.append(reply)

                except pymysql.Error as error:
                    # print("user not exist:", error)
                    reply = ""
                    reply_list.append(reply)
                cursor_1.close()
                cursor_2.close()
        return reply_list


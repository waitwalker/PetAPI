# -*- coding: utf-8 -*-
# @Time    : 2018/6/19 上午9:23
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTCommentReplyListHandler.py
# @Software: PyCharm

import pymysql

from Handlers import MTTBaseHandler

class MTTCommentReplyListHandler(MTTBaseHandler.MTTBaseHandler):

    def get(self, *args, **kwargs):
        self.handler_comment_reply_list()

    def post(self, *args, **kwargs):
        self.handler_comment_reply_list()

    # 处理评论和回复列表
    def handler_comment_reply_list(self):
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
                    query_comment_sql = """\
                            SELECT * FROM comment_info
                            """
                    cursor_3 = self.cur
                    db = self.db
                    db.ping(reconnect=True)
                    cursor_3.execute(query_comment_sql.format())
                    comment_results = cursor_3.fetchall()
                    # print("queryed all comment data:", comment_results)
                    comment_list = self.handler_comment_query_result(comment_results)
                    cursor_3.close()

                    query_reply_sql = """\
                                                SELECT * FROM reply_info
                                                """
                    cursor_4 = self.cur
                    db = self.db
                    db.ping(reconnect=True)
                    cursor_4.execute(query_reply_sql.format())
                    reply_results = cursor_4.fetchall()
                    # print("reply all data:", reply_results)
                    reply_list = self.handler_reply_query_result(reply_results)
                    cursor_4.close()

                    if len(comment_list) > int(0):
                        if len(reply_list) > int(0):
                            comment_list.extend(reply_list)

                            # print("coment and reply join list:",comment_list)

                            sorted_list = sorted(comment_list, key=lambda the_dict:the_dict['time'])

                            # print("sorted list:", sorted_list)
                            self.success_response(msg="获取评论列表成功", data=sorted_list)

                        else:
                            self.success_response(msg="获取评论列表成功", data=comment_list)
                    else:
                        self.success_response(msg="目前还没有人评论", data="")

                except pymysql.Error as error:
                    # print("user or topic id not exits 1:", error)
                    self.failure_response(msg="用户或者动态主题不存在", data="")

            else:
                # print("user or topic id not exits 2:")
                self.failure_response(msg="用户或者动态主题不存在", data="")
        except pymysql.Error as error:
            # print("user or topic id not exits 3:", error)
            self.failure_response(msg="用户或者动态主题不存在", data="")
        cursor_1.close()
        cursor_2.close()

        # 参数 uid
        # topic_id

    # 处理回复列表
    def handler_comment_query_result(self, results):

        comment_list = []
        for result in results:

            if type(result) == type({}):

                # print("query result:", result)
                from_uid = result['from_uid']
                content = result['content']
                comment_id = result['comment_id']
                time = result['time']

                cursor = self.cur
                query_user_sql = """\
                                    SELECT * FROM user_info WHERE uid = '{uid}'
                                    """
                try:
                    db = self.db
                    db.ping(reconnect=True)
                    query_user_result = cursor.execute(query_user_sql.format(uid=from_uid))
                    if query_user_result == True:
                        fetch_result = cursor.fetchone()
                        username = fetch_result['username']
                        uid = fetch_result['uid']

                        comment = {"uid": uid, "username": username, "content": content, "comment_id": comment_id, "time": time}
                        comment_list.append(comment)

                except pymysql.Error as error:
                    # print("user not exist:", error)
                    comment = ""
                    comment_list.append(comment)
        return comment_list

    # 处理回复列表
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
        return reply_list


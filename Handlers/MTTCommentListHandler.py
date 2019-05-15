# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 下午12:01
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTCommentListHandler.py
# @Software: PyCharm

from Handlers import MTTBaseHandler
import pymysql

class MTTCommentListHandler(MTTBaseHandler.MTTBaseHandler):

    def get(self, *args, **kwargs):
        self.handler_comment_list()

    def post(self, *args, **kwargs):
        self.handler_comment_list()

    # 处理评论
    def handler_comment_list(self):
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
                    SELECT * FROM comment_info WHERE topic_id = '{topic_id}' ORDER BY TIME DESC 
                    """
                    db = self.db
                    db.ping(reconnect=True)
                    cursor_3 = self.cur
                    cursor_3.execute(query_comment_sql.format(topic_id=topic_id))
                    comment_results = cursor_3.fetchall()
                    print("queryed all comment data::", comment_results)
                    comment_list = self.handler_comment_query_result(comment_results)
                    self.success_response(msg="获取评论列表成功", data=comment_list)
                    cursor_3.close()
                except pymysql.Error as error:
                    print("user or comment id not exist:", error)

            else:
                # print("user or comment id not exist 2:")
                self.failure_response(msg="用户或者动态主题不存在", data="")
        except pymysql.Error as error:
            # print("user or comment id not exist 3:", error)
            self.failure_response(msg="用户或者动态主题不存在", data="")
        cursor_1.close()
        cursor_2.close()

    def handler_comment_query_result(self, results):

        comment_list = []
        if len(results) > 0:
            for result in results:
                # print("query result::", result)
                from_uid = result['from_uid']
                to_uid = result['to_uid']
                content = result['content']
                comment_id = result['comment_id']
                time = result['time']

                cursor = self.cur
                cursor2 = self.cur
                query_user_sql = """\
                                                    SELECT * FROM user_info WHERE uid = '{uid}'
                                                    """

                try:
                    db = self.db
                    db.ping(reconnect=True)
                    query_user_result = cursor.execute(query_user_sql.format(uid=from_uid))
                    query_user_result2 = cursor2.execute(query_user_sql.format(uid=to_uid))
                    if query_user_result == True and query_user_result2 == True:
                        fetch_result = cursor.fetchone()
                        f_username = fetch_result['username']
                        f_uid = fetch_result['uid']

                        fetch_result2 = cursor2.fetchone()
                        t_username = fetch_result2['username']
                        t_uid = fetch_result2['uid']

                        comment = {"from_uid": f_uid, "from_username": f_username, "content": content,
                                   "comment_id": comment_id, "to_username": t_username, "to_uid": t_uid, "time": time}
                        comment_list.append(comment)

                except pymysql.Error as error:
                    # print("user not exist:", error)
                    comment = ""
                    comment_list.append(comment)

                cursor.close()
                cursor2.close()

        return comment_list

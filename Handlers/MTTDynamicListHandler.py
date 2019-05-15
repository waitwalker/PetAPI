# -*- coding: utf-8 -*-
# @Time    : 2018/6/14 上午11:38
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTDynamicListHandler.py
# @Software: PyCharm

from Handlers import MTTBaseHandler
import pymysql

class MTTDynamicListHandler(MTTBaseHandler.MTTBaseHandler):

    def get(self, *args, **kwargs):
        self.handler_dynamic_list()

    def post(self, *args, **kwargs):
        self.handler_dynamic_list()

    # 处理动态列表
    def handler_dynamic_list(self):
        uid = self.get_argument('uid')
        page_num = self.get_argument('pageNum')
        page_itmes = self.get_argument('pageItems')

        # print("parameter uid:", uid)
        cursor = self.cur

        query_user_sql = """\
        SELECT * FROM user_info WHERE uid='{uid}'
        """
        try:
            # 查询用户是否存在
            db = self.db
            db.ping(reconnect=True)
            query_user_result = cursor.execute(query_user_sql.format(uid=uid))

            cursor.close()

            # print("get dynamic list query user result:", query_user_result)

            if query_user_result == True:

                # print("user exist, can query dynamic")
                query_all_dynamic_sql = """\
                SELECT * FROM dynamic_info WHERE id > 0 ORDER BY time DESC 
                """
                try:
                    curs = self.cur
                    db = self.db
                    db.ping(reconnect=True)
                    curs.execute(query_all_dynamic_sql)
                    results = curs.fetchall()
                    curs.close()
                    isHaveMoreData = 0

                    if len(results) == 0:
                        isHaveMoreData = 0
                        msg = "目前还没有动态数据,请发一个试试"
                        data = {"dynamic_list": [],
                                "isHaveMoreData": isHaveMoreData
                                }

                        self.success_response(msg=msg, data=data)
                    else:
                        # 数据库中的总页数
                        # print("database dynamic list all results:", len(results))
                        current_results = []

                        all_pages = len(results) / int(page_itmes)

                        if type(all_pages) == float:
                            # print("the_all_pages:", int(all_pages))
                            all_pages = int(all_pages) + 1

                        # print("all page:", all_pages)
                        # print("current page:", page_num)

                        # 如果数据库中的总页数小于当前页数 说明没有那么多页
                        if int(all_pages) < int(page_num):
                            isHaveMoreData = 0
                            current_results = []
                        elif int(all_pages) == int(page_num):
                            current_results = results[int(int(page_num) - 1) * int(page_itmes): len(results)]
                            isHaveMoreData = 0
                        else:
                            current_results = results[int(int(page_num) - 1) * int(page_itmes): int(int(page_num) - 1) * int(page_itmes) + 10]
                            isHaveMoreData = 1

                        res_data = self.handler_query_result(data=current_results)
                        handlered_data = {"dynamic_list": res_data,
                                          "isHaveMoreData": isHaveMoreData
                                          }
                        self.success_response(msg="获取动态数据成功", data=handlered_data)
                    curs.close()
                except pymysql.Error as error:
                    print("query dynamic error 2:", error)
                    self.failure_response(msg="当前还有没有动态", data="")

            else:
                print("user not exist")
                self.failure_response(msg="用户不存在", data="")

        except pymysql.Error as error:
            print("user not exist:", error)
            self.failure_response(msg="用户不存在", data="")
        cursor.close()


    # 处理查询结果
    def handler_query_result(self, data):


        handlered_results = []
        for result in data:
            user_uid = self.get_argument('uid')
            uid = str(result["uid"])
            # print("type uid:", type(uid))
            topic_id = result["topic_id"]
            content = result["content"]
            attach = result["attach"]
            dynamic_type = result["dynamic_type"]
            time = result["time"]

            # 后期优化可以上缓存

            query_user_sql = """\
            SELECT * FROM user_info WHERE uid='{uid}'
            """
            cursor = self.cur

            try:
                db = self.db
                db.ping(reconnect=True)
                query_comment_sql = """\
                                    SELECT * FROM comment_info WHERE topic_id = '{topic_id}'
                                    """
                query_praise_sql = """\
                                                    SELECT * FROM praise_info WHERE topic_id = '{topic_id}'
                                                    """

                cursor_3 = self.cur
                cursor_3.execute(query_comment_sql.format(topic_id=topic_id))
                comment_results = cursor_3.fetchall()

                cursor_4 = self.cur
                cursor_4.execute(query_praise_sql.format(topic_id=topic_id))
                praise_results = cursor_4.fetchall()

                db = self.db
                db.ping(reconnect=True)
                cursor.execute(query_user_sql.format(uid=uid))
                query_result = cursor.fetchone()
                phone = query_result["phone"]
                username = query_result["username"]
                header_photo = query_result["header_photo"]
                isPraise = 0
                if len(praise_results) > 0:
                    for (index, dic) in enumerate(praise_results):
                        from_uid = str(dic['from_uid'])
                        if from_uid == user_uid:
                            isPraise = 1
                        else:
                            isPraise = 0
                else:
                    isPraise = 0
                single_dynamic_info = {"uid": uid, "phone": phone, "username": username, "header_photo": header_photo, "time": time, "topic_id": topic_id, "content": content, "attach": attach, "dynamicType": dynamic_type, "comment_num": len(comment_results), "praise_num": len(praise_results), "isPraise": isPraise}
                handlered_results.append(single_dynamic_info)
            except pymysql.Error as error:
                handlered_results = []
            cursor.close()
        return handlered_results


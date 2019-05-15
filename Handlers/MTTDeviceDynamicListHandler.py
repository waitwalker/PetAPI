# -*- coding: utf-8 -*-
# @Time    : 2018/7/20 下午2:16
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTDeviceDynamicListHandler.py
# @Software: PyCharm

from Handlers import MTTBaseHandler
import pymysql


class MTTDeviceDynamicListHandler(MTTBaseHandler.MTTBaseHandler):

    def post(self, *args, **kwargs):
        self.handler_device_dynamic_lsit()

    def get(self, *args, **kwargs):
        self.handler_device_dynamic_lsit()

    def handler_device_dynamic_lsit(self):
        device_token = self.get_argument("deviceToken")
        time = self.get_argument("time")
        # print("time:", time)

        cursor = self.cur
        query_sql = """\
        SELECT * FROM device_info WHERE device_token = '{device_token}'
        """
        db = self.db
        db.ping(reconnect=True)
        query_result = cursor.execute(query_sql.format(device_token=device_token))

        cursor.close()
        if query_result == True:

            cursor_1 = self.cur
            query_dynamic_sql = """\
            SELECT * FROM dynamic_info WHERE id > 0
            """
            db = self.db
            db.ping(reconnect=True)
            query_dynamic_result = cursor_1.execute(query_dynamic_sql)

            if int(query_dynamic_result) > 0:

                results = cursor_1.fetchall()
                response_results = results

                if len(results) > 8:
                    response_results = results[:8]
                # print("dynamic list count:", len(response_results))
                handlered_results = self.handler_response_data(response_results)
                if len(handlered_results) > 0:
                    msg = "获取动态列表成功"
                    data = {"dynamic_list": handlered_results}
                    self.success_response(msg=msg, data=data)
                else:
                    msg = "目前还没有动态,请先发布一条吧"
                    data = {}
                    self.success_response(msg=msg, data=data)

            else:
                msg = "目前还没有动态,请先发布一条吧"
                data = {}
                self.success_response(msg=msg, data=data)
            cursor_1.close()
        else:
            msg = "设备还没有注册,请重试"
            data = {}
            self.failure_response(msg=msg, data=data)
        cursor.close()


    def handler_response_data(self, data):

        reponse = []
        for result in data:
            content = result["content"]
            time = result["time"]
            attach = result["attach"]
            uid = result["uid"]
            dynamic_type = result["dynamic_type"]
            topic_id = result["topic_id"]

            # print("parameter_uid:", uid)

            cursor = self.cur
            query_user_sql = """\
            SELECT * FROM user_info WHERE uid='{uid}'
            """
            try:
                db = self.db
                db.ping(reconnect=True)
                query_user_result = cursor.execute(query_user_sql.format(uid=uid))

                if query_user_result == 1:

                    user = cursor.fetchone()

                    username = user["username"]
                    header_photo = user["header_photo"]
                    single_dynamic_info = {"username": username, "header_photo": header_photo, "topic_id": topic_id, "content": content, "attach": attach, "time": time, "dynamicType": dynamic_type}
                    reponse.append(single_dynamic_info)
            except pymysql.Error as error:
                print("query user error:", error)
                if len(reponse) > 0:
                    reponse = []
            cursor.close()
        return reponse











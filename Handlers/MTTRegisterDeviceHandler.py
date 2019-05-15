# -*- coding: utf-8 -*-
# @Time    : 2018/7/20 下午1:40
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTRegisterDeviceHandler.py
# @Software: PyCharm

from Handlers import MTTBaseHandler
import pymysql


class MTTRegisterDeviceHandler(MTTBaseHandler.MTTBaseHandler):

    def post(self, *args, **kwargs):
        self.handler_register_device()

    def get(self, *args, **kwargs):
        self.handler_register_device()

    def handler_register_device(self):

        device_token = self.get_argument("deviceToken")
        time = self.get_argument("time")

        cursor = self.cur
        query_device_sql = """\
        SELECT * FROM device_info WHERE device_token = '{device_token}'
        """
        db = self.db
        db.ping(reconnect=True)
        query_result = cursor.execute(query_device_sql.format(device_token=device_token))
        cursor.close()

        # print('query_result:', query_result)

        if query_result == True:
            msg = "设备已经注册过了,可以发起其他请求"
            data = {"deviceToken": device_token}
            self.success_response(msg=msg, data=data)
        else:
            cursor_1 = self.cur
            insert_sql = """\
            INSERT INTO device_info(device_token, time) VALUES ('{device_token}', '{time}')
            """
            db = self.db
            db.ping(reconnect=True)
            insert_result = cursor_1.execute(insert_sql.format(device_token=device_token, time=time))
            self.db.commit()
            if insert_result == True:
                self.db.commit()
                msg = "设备注册成功,可以发起其他请求"
                data = {"deviceToken": device_token}
                self.success_response(msg=msg, data=data)
            else:
                self.db.rollback()
                msg = "设备注册失败"
                data = {"deviceToken": ""}
                self.failure_response(msg=msg, data=data)
            cursor_1.close()





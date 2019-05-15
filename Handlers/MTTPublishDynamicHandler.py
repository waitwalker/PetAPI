# -*- coding: utf-8 -*-
# @Time    : 2018/6/14 上午10:04
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTPublishDynamicHandler.py
# @Software: PyCharm

# 发表动态接口

from Handlers import MTTBaseHandler, MTTFilterKeywordManager
import pymysql
from PsuhManager.MTTPushNotificationManager import MTTPushNotificationManager

class MTTPublishDynamicHandler(MTTBaseHandler.MTTBaseHandler):

    def push_noti(self):
        app_versions = ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]
        username = self.get_argument("username")
        notification = MTTPushNotificationManager()
        for (index, appverion) in enumerate(app_versions):
            notification.push_notification(description="提醒", push_body=username + ":  写了新的心情,赶快去查看吧!", app_version=appverion)

    def get(self, *args, **kwargs):
        self.push_noti()
        self.handler_publish_dynamic()


    def post(self, *args, **kwargs):
        self.push_noti()
        self.handler_publish_dynamic()


    # 处理发表动态
    def handler_publish_dynamic(self):
        uid = self.get_argument('uid')
        content = self.get_argument('content')
        time = self.get_argument('time')
        topic_id = int(uid) + int(time)
        attach = self.get_argument('attach')
        dynamic_type = self.get_argument('dynamic_type')
        if not len(attach) > 0:
            attach = ""
        cursor = self.cur

        if len(content) > 0:
            filterManager = MTTFilterKeywordManager.MTTFilterKeywordManager(words=[])
            trie = filterManager.get_trie()

            filter_result = filterManager.replace_word(trie=trie, content=content)
            if len(filter_result) > 0:
                for subStr in filter_result:
                    content = content.replace(subStr, "****")


        sql = """\
        SELECT * FROM user_info WHERE uid = '{uid}'
        """
        try:
            db = self.db
            db.ping(reconnect=True)
            result = cursor.execute(sql.format(uid=uid))

            if result == True:
                try:
                    insert_sql = """\
                    INSERT INTO dynamic_info(uid,topic_id,content,attach,time,dynamic_type) VALUES ('{uid}', '{topic_id}', '{content}', '{attach}', '{time}', '{dynamic_type}')
                    """
                    try:
                        # 格式化输出
                        # print("dynamic info:  uid:{},topic_id:{},content:{},attach:{},time:{},dynamic_type:{}".format(uid, topic_id, content, attach, time, dynamic_type))
                        db = self.db
                        db.ping(reconnect=True)
                        insert_result = cursor.execute(insert_sql.format(uid=uid, topic_id=topic_id, content=content, attach=attach, time=time, dynamic_type=dynamic_type))

                        if insert_result == True:
                            self.success_response(msg="发表动态成功", data="")
                            self.db.commit()
                        else:
                            # print("insert dynamic failure 1")
                            self.failure_response(msg="发表动态失败, 请重试", data="")

                    except pymysql.Error as error:
                        # print("insert dynamic failure 2:", error)
                        self.db.rollback()
                        self.failure_response(msg="发表动态失败, 请重试", data="")

                except pymysql.Error as error:
                    # print("insert dynamic failure 3:", error)
                    self.failure_response(msg="发表动态失败, 请重试", data="")

            else:
                # print("user not exist")
                self.failure_response(msg="当前用户不存在", data="")

        except pymysql.Error as error:
            # print("user not exist", error)
            self.failure_response(msg="当前用户不存在", data="")
        cursor.close()




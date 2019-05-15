# -*- coding: utf-8 -*-
# @Time    : 2018/10/16 11:20 AM
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTReportAbuseHandler.py
# @Software: PyCharm


from Handlers import MTTBaseHandler
import pymysql
from Handlers import MTTFilterKeywordManager
import os

class MTTReportAbuseHandler(MTTBaseHandler.MTTBaseHandler):

    def get(self, *args, **kwargs):
        self.handler_report()

    def post(self, *args, **kwargs):
        self.handler_report()

    def handler_report(self):

        report_keyword = self.get_argument("report_keyword")
        report_content = self.get_argument("report_content")
        content = self.get_argument("content")
        topic_id = self.get_argument("topic_id")

        if len(content) == 0:
            self.success_response(msg="举报成功",data=[])
        else:
            filterManager = MTTFilterKeywordManager.MTTFilterKeywordManager(words=[])
            trie = filterManager.get_trie()

            filter_result = filterManager.filter_word(trie=trie, content=content)

            if filter_result == True:

                delete_sql = """\
                                                            DELETE FROM dynamic_info WHERE topic_id='{topic_id}'
                                                            """
                cur = self.cur
                try:
                    db = self.db
                    db.ping(reconnect=True)
                    delete_result = cur.execute(delete_sql.format(topic_id=topic_id))

                    print("delete result:", delete_result)
                    self.success_response(msg="举报成功", data=[])

                except pymysql.error as e:
                    self.failure_response(msg="举报失败,请稍候重试",data=[])

            else:
                self.success_response(msg="举报成功", data=[])



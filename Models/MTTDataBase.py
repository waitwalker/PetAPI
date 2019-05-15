# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 下午5:22
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTDataBase.py
# @Software: PyCharm


# 数据连接


import pymysql
import time


class MTTDataBase:

    error_code = ''
    instance = None
    # db = None
    # cursor = None

    timeout = 30
    time_count = 0

    # 构造函数 初始化实例 创建 连接连接db对象
    def __init__(self, config):
        try:
            self.db = pymysql.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                db=config['db'],
                charset=config['charset'],
                cursorclass=pymysql.cursors.DictCursor)
            print("connect database success")

        except pymysql.Error as error:
            self.error_code = error.args[0]
            error_msg = 'mysql connect error !',error[1]
            print(error_msg)
            if self.time_count < self.timeout:
                interval = 5
                self.time_count += interval
                time.sleep(interval)
                return self.__init__(config)
            else:
                raise Exception(error_msg)
        self.c = self.db.cursor()


    # 查询数据 根据查询结果 添加相应的返回值
    def query(self, sql):
        try:
            result = self.cursor.execute(sql)
        except pymysql.Error as error:
            print('query error:', error)
            self.error_code = error.args[0]
            result = False
        return result

    # 更新数据 数据更新失败:回滚
    def update(self, sql):
        try:
            result = self.cursor.execute(sql)
            self.db.commit()

        except pymysql.Error as error:
            print("update database error:", error)
            self.error_code = error.args[0]
            result = False
            self.rollback()
        return result

    # 插入输入 数据插入失败:回滚
    def insert(self, sql):
        try:
            result = self.cursor.execute(sql)
            self.db.commit()
        except pymysql.Error as error:
            print("insert error:",error)
            self.error_code = error.args[0]
            result = False
            self.rollback()
        return result

    # 删除数据 数据删除失败:回滚
    def delete(self, sql):
        try:
            result = self.cursor.execute(sql)
            self.db.commit()
        except pymysql.Error as error:
            print("delete error:",error)
            self.error_code = error.args[0]
            result = False
            self.rollback()
        return result

    # 获取所有数据
    def fetchall(self):
        return self.cursor.fetchall()

    # 回滚: 遇到错误或者其他情况
    def rollback(self):
        self.db.rollback()

    # 关闭数据库
    def close(self):
        try:
            self.cursor.close()
            self.db.close()
        except pymysql.Error as error:
            print(error)


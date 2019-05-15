# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 上午10:57
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MainServer.py
# @Software: PyCharm


import tornado.web,tornado.options,tornado.ioloop,tornado.httpserver
from tornado.options import define,options
from urls import urls
import pymysql
import redis
import tornado.log
import logging
import os
import logging.handlers


# 宏定义
# 端口
define('port', type=int, default=8000, help='listen port')

# console输出格式
class MTTLogFormatter(tornado.log.LogFormatter):
    def __init__(self):
        super(MTTLogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

# application
class MTTApplication(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(MTTApplication, self).__init__(*args, **kwargs)
        self.database = pymysql.connect(host='localhost',
                                  user='root',password='etiantian',
                                  db='pet_database',
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor
                                  )
        # redis 连接池
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        self.redis = redis.Redis(connection_pool=pool)

# 入口函数
def main():

    # if "log_file_prefix" in options._options:
    #     # print("log_file_prefix have define")
    # else:
    #     tornado.options.define('log_file_prefix', default=get_logger_file_path())
    #     # print("options._options", options._options)

    tornado.options.parse_command_line()
    app = MTTApplication(
      urls.handlers,
    )
    # [i.setFormatter(MTTLogFormatter()) for i in logging.getLogger().handlers]

    # 自定义logger
    # set_logger()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

# 获取文件绝对路径
def get_logger_file_path():
    current_path = os.path.abspath(__file__)

    father_path = os.path.abspath(os.path.dirname(current_path))

    file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + "/loggers/tornado_main.log"))


    # print("current_path:", current_path)

    # print("father_path:", father_path)

    # print("file_path:", file_path)
    return file_path

# 自定义logger
def set_logger():

    log_file = get_logger_file_path()
    handler = logging.handlers.RotatingFileHandler(filename=log_file, maxBytes=1024 * 1024 * 1024,backupCount=5)
    formatter = MTTLogFormatter()
    handler.setFormatter(formatter)

    # print("handler.baseFilename", handler.baseFilename)

    logger = logging.getLogger('tornado_main')

    # print("logger.handlers", logger.handlers)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info('abc')


def define(name, default=None, type=None, help=None, metavar=None,
           multiple=False, group=None, callback=None):
    if name not in options._options:
        return define(name, default, type, help, metavar,
                       multiple, group, callback)


if __name__ == '__main__':

    main()

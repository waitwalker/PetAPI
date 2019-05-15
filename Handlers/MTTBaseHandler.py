# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 上午11:06
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTBaseHandler.py
# @Software: PyCharm

# ***********************

# handler处理基类

# ***********************

from tornado.web import RequestHandler
import json
import pymysql
from Models import MTTDataBase
from Security import MTTSecurityManager
from Crypto.Cipher import AES
import os
import logging
import logging.handlers
import tornado.log
import traceback



database = pymysql.connect(
    host='localhost',
    user='root',
    password='etiantian',
    db='pet_database',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

key = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

iv = [123, 2, 3, 4, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# 定义处理基类 继承自RequestHandler
class MTTBaseHandler(RequestHandler):

    @property
    def aes_key(self):
        return key

    @property
    def aes_iv(self):
        return iv

    @property
    def security_manager(self):
        s_manager = MTTSecurityManager.MTTSecurityManager(self.aes_key, self.aes_iv, AES.MODE_CBC)
        return s_manager

    # 属性装饰器,使db函数变成一个属性,便于后面直接调用
    @property
    def db(self):
        return self.application.database

    # 属性装饰器 操作游标
    @property
    def cur(self):
        return self.db.cursor()

    # 属性装饰器 redis
    @property
    def redis(self):
        return self.application.redis

    # 属性装饰器,使db函数变成一个属性,便于后面直接调用
    # @property
    # def db(self):
    #     connect_config = {'host': 'localhost', 'user': 'root', 'password': 'etiantian', 'db': 'pet_database',
    #                       'charset': 'utf8mb4'}
    #     the_db = MTTDataBase.MTTDataBase(config=connect_config)
    #     return the_db.db
    #
    # # 属性装饰器 操作游标
    # @property
    # def cur(self):
    #     return self.db.c

    # 重写方法
    def prepare(self):
        pass
        print("method:",self.request.method)
        print("uri:",self.request.uri)
        print("path:", self.request.path)
        print("query:", self.request.query)
        print("version:", self.request.version)
        remote_ip = self.request.remote_ip
        print("remote_ip", remote_ip)
        # print("query_arguments", self.get_query_arguments(name='username'))
        # print("body_arguments", self.get_body_arguments(name='username'))

        self.set_logger(info=self.request, filename="pet_info.log")

    # get 请求方法
    def get(self, *args, **kwargs):
        pass

    # post 请求方法
    def post(self, *args, **kwargs):
        pass


    def write_error(self, status_code, **kwargs):

        print('status_code:', status_code)

        error_trace_list = traceback.format_exception(*kwargs.get("exc_info"))

        argu = {"request": self.request, "error_trace": error_trace_list}

        self.set_logger(info=argu, filename="pet_error.log")

        if status_code == 300:
            msg = "被请求的资源有一系列可供选择的回馈信息，每个都有自己特定的地址和浏览器驱动的商议信息。"
            self.handler_packge(msg=msg,status_code=status_code)

        elif status_code == 301:
            msg = "被请求的资源已永久移动到新位置，并且将来任何对此资源的引用都应该使用本响应返回的若干个 URI 之一。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 302:
            msg = "请求的资源临时从不同的 URI响应请求"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 303:
            msg = "对应当前请求的响应可以在另一个 URI 上被找到，而且客户端应当采用 GET 的方式访问那个资源。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 304:
            msg = "如果客户端发送了一个带条件的 GET 请求且该请求已被允许，而文档的内容（自上次访问以来或者根据请求的条件）并没有改变，则服务器应当返回这个状态码。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 305:
            msg = "被请求的资源必须通过指定的代理才能被访问。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 306:
            msg = "在最新版的规范中，306状态码已经不再被使用。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 307:
            msg = "请求的资源临时从不同的URI 响应请求。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 400:
            msg = "语义有误，当前请求无法被服务器理解。请求参数有误。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 401:
            msg = "当前请求需要用户验证。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 402:
            msg = "该状态码是为了将来可能的需求而预留的。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 403:
            msg = "服务器已经理解请求，但是拒绝执行它。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 404:
            msg = "请求失败，请求所希望得到的资源未被在服务器上发现。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 405:
            msg = "请求行中指定的请求方法不能被用于请求相应的资源。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 406:
            msg = "请求的资源的内容特性无法满足请求头中的条件，因而无法生成响应实体。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 407:
            msg = "与401响应类似，只不过客户端必须在代理服务器上进行身份验证。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 408:
            msg = "请求超时。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 409:
            msg = "由于和被请求的资源的当前状态之间存在冲突，请求无法完成。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 410:
            msg = "响应的目的主要是帮助网站管理员维护网站，通知用户该资源已经不再可用，并且服务器拥有者希望所有指向这个资源的远端连接也被删除。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 411:
            msg = "由于和被请求的资源的当前状态之间存在冲突，请求无法完成。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 411:
            msg = "服务器拒绝在没有定义 Content-Length 头的情况下接受请求。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 412:
            msg = "服务器在验证在请求的头字段中给出先决条件时，没能满足其中的一个或多个。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 413:
            msg = "服务器拒绝处理当前请求，因为该请求提交的实体数据大小超过了服务器愿意或者能够处理的范围。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 414:
            msg = "请求的URI 长度超过了服务器能够解释的长度，因此服务器拒绝对该请求提供服务。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 415:
            msg = "对于当前请求的方法和所请求的资源，请求中提交的实体并不是服务器中所支持的格式，因此请求被拒绝。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 416:
            msg = "如果请求中包含了 Range 请求头，并且 Range 中指定的任何数据范围都与当前资源的可用范围不重合，同时请求中又没有定义 If-Range 请求头，那么服务器就应当返回416状态码。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 417:
            msg = "在请求头 Expect 中指定的预期内容无法被服务器满足，或者这个服务器是一个代理服务器，它有明显的证据证明在当前路由的下一个节点上，Expect 的内容无法被满足。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 421:
            msg = "从当前客户端所在的IP地址到服务器的连接数超过了服务器许可的最大范围。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 422:
            msg = "请求格式正确，但是由于含有语义错误，无法响应。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 423:
            msg = "当前资源被锁定。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 424:
            msg = "由于之前的某个请求发生的错误，导致当前请求失败，例如 PROPPATCH。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 425:
            msg = "在WebDav Advanced Collections 草案中定义，但是未出现在《WebDAV 顺序集协议》（RFC 3658）中。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 426:
            msg = "客户端应当切换到TLS/1.0。（RFC 2817）"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 449:
            msg = "由微软扩展，代表请求应当在执行完适当的操作后进行重试。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 451:
            msg = "该请求因法律原因不可用。（RFC 7725）"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 500:
            msg = "服务器遇到了一个未曾预料的状况，导致了它无法完成对请求的处理。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 501:
            msg = "服务器不支持当前请求所需要的某个功能。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 502:
            msg = "作为网关或者代理工作的服务器尝试执行请求时，从上游服务器接收到无效的响应。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 503:
            msg = "由于临时的服务器维护或者过载，服务器当前无法处理请求。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 504:
            msg = "作为网关或者代理工作的服务器尝试执行请求时，未能及时从上游服务器（URI标识出的服务器，例如HTTP、FTP、LDAP）或者辅助服务器（例如DNS）收到响应。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 505:
            msg = "服务器不支持，或者拒绝支持在请求中使用的 HTTP 版本。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 505:
            msg = "服务器不支持，或者拒绝支持在请求中使用的 HTTP 版本。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 506:
            msg = "由《透明内容协商协议》（RFC 2295）扩展，代表服务器存在内部配置错误：被请求的协商变元资源被配置为在透明内容协商中使用自己，因此在一个协商处理中不是一个合适的重点。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 507:
            msg = "服务器无法存储完成请求所必须的内容。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 510:
            msg = "获取资源所需要的策略并没有被满足。"
            self.handler_packge(msg=msg, status_code=status_code)

        elif status_code == 600:
            msg = "源站没有返回响应头部，只返回实体内容"
            self.handler_packge(msg=msg, status_code=status_code)

        else:
            msg = "系统异常,请稍候重试"
            self.handler_packge(msg=msg, status_code=status_code)


    def get_logger_file_path(self, filename):
        current_path = os.path.abspath(__file__)

        father_path = os.path.abspath(os.path.dirname(current_path))

        grand_father_path = os.path.abspath(os.path.dirname(father_path))

        file_path = os.path.join(os.path.abspath(grand_father_path + "/loggers/" + filename))

        # print("current_path:", current_path)
        #
        # print("father_path:", father_path)
        #
        # print("grand_father_path", grand_father_path)
        #
        # print("file_path:", file_path)
        return file_path

    # 自定义logger
    def set_logger(self, filename, info):

        log_file = self.get_logger_file_path(filename)
        handler = logging.handlers.RotatingFileHandler(filename=log_file, maxBytes=1024 * 1024 * 1024, backupCount=5)
        formatter = MTTLogFormatter()
        handler.setFormatter(formatter)

        # print("handler.baseFilename", handler.baseFilename)

        logger = logging.getLogger('pet_error')

        # print("logger.handlers", logger.handlers)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(info)

    # 根据状态码 返回 固定数据格式
    def handler_error_message(self, status_code, msg):

        responseObj = {
            "data": "",
            "result": status_code,
            "msg": msg
        }
        return responseObj

    # 封装错误返回数据
    def handler_packge(self, msg, status_code):
        kwargs = {
            "status_code": status_code,
            "msg": msg
        }
        responseObj = self.handler_error_message(**kwargs)
        # 序列化 josn 格式
        self.write(json.dumps(responseObj))

    # 请求成功的数据返回格式
    def success_response(self, msg, data):
        responseObj = {
            "data": data,
            "result": 1,
            "msg": msg
        }
        self.write(json.dumps(responseObj))

        # 请求失败或者错误的数据返回格式
    def failure_response(self, msg, data=""):
        responseObj = {
            "data": data,
            "result": -1,
            "msg": msg
        }
        self.write(json.dumps(responseObj))

    # 查询数据 根据查询结果 添加相应的返回值
    def query(self, sql):
        try:
            result = self.cur.execute(sql)
        except pymysql.Error as error:
            print('查询数据错误:', error)
            self.error_code = error.args[0]
            result = False
        return result

    # 更新数据 数据更新失败:回滚
    def update(self, sql):
        try:
            result = self.cur.execute(sql)
            self.db.commit()

        except pymysql.Error as error:
            # print("根数数据错误:", error)
            self.error_code = error.args[0]
            result = False
            self.rollback()
        return result

    # 插入输入 数据插入失败:回滚
    def insert(self, sql):
        try:
            result = self.cur.execute(sql)
            self.db.commit()
        except pymysql.Error as error:
            # print("插入数据错误:",error)
            self.error_code = error.args[0]
            result = False
            self.rollback()
        return result

    # 删除数据 数据删除失败:回滚
    def delete(self, sql):
        try:
            result = self.cur.execute(sql)
            self.db.commit()
        except pymysql.Error as error:
            # print("删除数据错误:",error)
            self.error_code = error.args[0]
            result = False
            self.rollback()
        return result

    # 获取所有数据
    def fetchall(self):
        return self.cur.fetchall()

    # 回滚: 遇到错误或者其他情况
    def rollback(self):
        self.db.rollback()

    # 关闭数据库
    def close(self):
        try:
            self.cur.close()
            self.db.close()
        except pymysql.Error as error:
            print(error)

class MTTLogFormatter(tornado.log.LogFormatter):
    def __init__(self):
        super(MTTLogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
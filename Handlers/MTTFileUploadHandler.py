# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 上午10:51
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTFileUploadHandler.py
# @Software: PyCharm

from Handlers import MTTBaseHandler
import tornado.web
import os


class MTTFileUploadHandler(MTTBaseHandler.MTTBaseHandler):

    # get请求方法
    def get(self, *args, **kwargs):
        msg = "上传文件只支持post请求"
        data = ""
        kwargs_ = {"msg": msg, "data": data}
        self.success_response(**kwargs_)

    # post请求
    def post(self, *args, **kwargs):
        # 文件暂存路径
        upload_path = os.path.join(os.path.dirname(__file__), 'files')
        # print("file path:", upload_path)

        # print("file list:", self.request.files)

        # 提取表单中'name'为file的文件元数据
        file_metas = self.request.files.get('file2', None)

        # print("file:", self.request.files)

        # print("body", self.request.body)

        file_path = ''

        if not file_metas:
            msg = "文件上传失败"
            data = ""
            kwargs_ = {"msg": msg, "data": data}
            self.success_response(**kwargs_)
        for meta in file_metas:
            filename = meta['filename']

            # print("file name:", filename)

            file_path = os.path.join(upload_path, filename)
            # print("file full path:", file_path)

            with open(file_path, 'wb') as up:
                up.write(meta['body'])
                # print("file update success path:", file_path)

        msg = "文件上传成功!"
        data = {"file_path": file_path}
        self.success_response(msg=msg, data=data)










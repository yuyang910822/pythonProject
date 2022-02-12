# -*- coding: utf-8 -*- 
# @Time : 2022/1/20 16:15 
# @Author : Yu yang
# @File : runtest.py
import time

import jsonpath
import requests


class Main:

    def re(self, loc):
        """

        :param loc:
        :return:
        """
        method, url, headers, json = loc

        r = requests.request(method=method, url=url, headers=headers, json=json)

        return r

    def setProperties(self, name):
        """
        用于测试依赖的随机数，可以是任务号也可以是其他
        :param name:实例变量名称
        :return:
        """
        t = int(((time.time())+60*10)*1000)
        setattr(self, name, t)
        return t

    def getToken(self, username):
        """
        从配置文件读取登录数据，生成Token
        :param username：登录需要的用户名&密码
        :return:
        """
        r = self.re(username)
        return jsonpath.jsonpath(r.json(), '$..token')[0]

    @staticmethod
    def getDate():
        """
        获取日期
        :return:
        """
        return time.strftime("%Y-%m-%d")

    @staticmethod
    def getDateTime():
        """
        获取日期时间
        :return:
        """
        return time.strftime("%Y-%m-%d|%H:%M:%S")
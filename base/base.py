# -*- coding: utf-8 -*- 
# @Time : 2022/1/20 16:15 
# @Author : Yu yang
# @File : runtiest.py
import os
import time

import jsonpath
import requests
from requests import Response

from common.log import Cluster_log
from common.path import mysql_dir, jd_log_dir, jd_api_dir, dirs
from common.readYaml import readYaml


class Base(object):
    """
    公共方法层,业务层继承基类，方便调用
    """

    def __init__(self, db_name: str, log_name: str, url_file_name: str):
        """
        为base类提供基础能力，但不局限日志，数据库，测试数据等

        :param db_name: 数据库名称 ../config/mysql.yaml
        :param log_name: 日志名称 生成日志文件时必传
        :param url_file_name: 接口测试数据文件名称 ../config/****
        """
        self.mysql = readYaml(mysql_dir)[db_name]
        self.log = Cluster_log(file=log_name)
        self.url = readYaml(os.path.join(dirs, r'data\{}.yaml'.format(url_file_name)))

    # def re(self, loc):
    #     """
    #     通过字典
    #     :param loc: 接口依赖数据：请求方式，请求地址，请求头，请求体
    #     :return:
    #     """
    #     method, url, headers, json = loc
    #     self.log.info(f'接口入参：\n{method}，{url}\n{headers}\n{json}')
    #     r = requests.request(method=method, url=url, headers=headers, json=json)
    #     self.log.info(f'响应体:{r.json()}')
    #     return r

    def re1(self, info: dict) -> Response:
        """
        封装接口请求
        :return: 响应信息
        """
        times = int(time.time()*1000)
        self.log.info(f'{info["url"]}--|{times}|>>>>>{info["json"]}')
        r = requests.request(**info)
        self.log.info(f'{info["url"]}--|{times}|<<<<<{r.json()}')
        return r

    def setProperties(self, name: str) -> int:
        """
        设置属性
        :param name:实例变量名称
        :return:
        """
        t = int(((time.time()) + 60 * 10) * 1000)
        setattr(self, name, t)
        return t

    def getToken(self, login_info) -> str:
        """
        登录获取对应token
        :param login_info: 登录接口请求信息
        :return:
        """
        r = self.re1(**login_info)
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


if __name__ == '__main__':
    f = Base('mysql', '1', 'jd_api')
    ff ={"method": "post","url": "http://gateway.jd.test.be.hwc.forwardx.com/user-center/user/login",
   "headers": {"Content-Type": "application/json"},
   "json": {"timeout":3000,"userName":"jd_admin","password":"02880bed5d3fd6216821a16b1346213cc5f284ce32181b907bf0150cc474f325"}
  }
    f.re1(ff)
    f.re1(ff)
    f.re1(ff)
    f.re1(ff)

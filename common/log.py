# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/7/6 16:39 
  @Auth : 于洋
  @File : log.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
-------------------------------------------------
"""

import logging
from logging.handlers import TimedRotatingFileHandler

from common.path import log_dir


class Cluster_log(logging.Logger):
    """
    集群日志收集器
    """

    def __init__(self, name, level='DEBUG', file=None):
        super().__init__(name, level)
        # 日志格式
        fmt = logging.Formatter("%(levelname)s - %(asctime)s - %(filename)s[line:%(lineno)d] : %(message)s")
        # 日志处理器
        p = logging.StreamHandler()
        p.setFormatter(fmt)
        self.addHandler(p)
        # 文件处理器
        if file:
            f = TimedRotatingFileHandler(file, when='D', backupCount=7, encoding='utf-8')
            f.setFormatter(fmt)
            self.addHandler(f)


if __name__ == '__main__':
    a = Cluster_log('jd',file=log_dir + r'\标签拣选11111.log')

    a.error('111')



















































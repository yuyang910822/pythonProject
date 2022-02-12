# -*- coding: utf-8 -*-
# @Time : 2022/1/20 22:52
# @Author : Yu yang
# @File : test_01.py
import unittest
from item.jd import Jd_Class


class Test01(unittest.TestCase):
    """JD 标签拣选"""

    item = Jd_Class()
    unittest.skip()
    def test_01(self):
        """下单"""
        self.item.operateRobot_4()
        self.assertTrue(self.item.receivePicking(1, 1), 1)

    def test_03(self):
        """前往拣货点"""
        self.assertTrue(self.item.getstatusDesc('拣选中'), '拣选中')

    def test_04(self):
        """到达拣货点"""
        self.assertTrue(self.item.operateRobot_10(), 1)

    def test_05(self):
        """拣货完成"""
        self.assertTrue(self.item.pickStationFinish(), 1)

    def test_06(self):
        """到达卸货"""
        self.item.operateRobot_10()  # 到达卸货查询点
        self.item.operateRobot_10()  # 前往卸货点
        self.assertTrue(self.item.operateRobot_10(), 1)
        
    def test_07(self):
        """卸货完成"""
        self.assertTrue(self.item.freedAMR(), 1)


if __name__ == '__main__':
    unittest.main(verbosity=3)

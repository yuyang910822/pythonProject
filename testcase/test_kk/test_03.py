# -*- coding: utf-8 -*- 
# @Time : 2022/1/21 13:55 
# @Author : Yu yang
# @File : test_03.py
import allure
import pytest

from item.jd import Jd_Class


@allure.feature("JD-非合流拣选")
class Test02:
    """
    非合流拣选
    """

    item = Jd_Class()

    def test_01(self):
        """下单"""
        self.item.operateRobot_4()
        assert self.item.receivePicking(1, 1) == 1

    def test_02(self):
        """到达上箱查询点"""
        assert self.item.operateRobot_10() == 1

    def test_03(self):
        """上箱异常"""
        assert self.item.operateRobot_10() == 1

    def test_04(self):
        """异常处理"""
        assert self.item.operateRobot_10() == 1

    def test_05(self):
        """前往拣货点"""
        assert self.item.pickStationFinish() == 1

    def test_06(self):
        """到达拣货点"""
        self.item.operateRobot_10()  # 到达卸货查询点
        self.item.operateRobot_10()  # 前往卸货点
        self.item.operateRobot_10()  # 到达卸货点

    def test_07(self):
        """拣货完成"""
        assert self.item.freedAMR() == 1

    def test_08(self):
        """前往卸货点"""
        assert self.item.freedAMR() == 1

    def test_09(self):
        """到达卸货点"""
        assert self.item.freedAMR() == 1

    def test_10(self):
        """卸货完成"""
        assert self.item.freedAMR() == 1


if __name__ == '__main__':
    pytest.main('-s')

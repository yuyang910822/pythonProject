# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/7/6 15:39
  @Auth : 于洋
  @File : core_competence.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
-------------------------------------------------
"""
import json

import jsonpath as jsonpath
import time
from common.log import Cluster_log
from common.path import mysql_dir, jd_log_dir, jd_api_dir
from common.readYaml import readYaml
from common.main import Main


class Jd_Class:
    """
        京东项目: 中间层。
        使用项目的配置数据来填充commom模块
        中间层用于连接公共方法层和业务逻辑层，实现了代码分层更为清晰，业务逻辑层调用更为简洁可读性更高
    """

    # 数据库
    mysql = readYaml(mysql_dir)['mysql']
    # 日志收集
    log = Cluster_log('JD', file=jd_log_dir)
    # 读取接口数据
    url = readYaml('{}'.format(jd_api_dir))
    # 依赖方法
    module = Main()
    # 反射
    taskNo = ''

    def receivePicking(self, tag, loading=1):
        """
        京东下单
        :param tag: 任务类型 1：标签拣选 2:合流拣选 3：非合流拣选
        :param loading: 1：自动上箱 2：手动上箱
        :return:
        """
        self.log.info('开始下单')
        # 重组请求体
        data = self.url['receivePicking'][3]
        data['taskNo'] = str(self.module.setProperties('taskNo'))
        data['tagType'] = str(tag)
        data['loadingType'] = str(loading)
        data['cutOffTime'] = str(self.module.setProperties('taskNo'))

        # 发送请求
        r = self.module.re(self.url['receivePicking'])
        try:

            if r.json()['status']['statusCode'] == 0:
                self.log.info('下单成功')
            else:
                self.log.error('请求地址：{}'.format(r.request.url))
                self.log.error('请求入参：{}'.format(r.request.body))
                self.log.error(f'下单失败原因：{r.json()}')
                raise
        except (KeyError, RuntimeError) as e:
            self.log.error('下单失败：{}'.format(e))
            return 0
        else:
            setattr(self, 'taskNo', jsonpath.jsonpath(data, '$..taskNo'))
            return 1

    def getRobotNo(self):
        """
        通过taskNo获取车号
        :return:
        """
        self.log.info('开始获取车号')
        data = self.url['getListWithPage'][3]
        data['originalWaveNo'] = str(self.taskNo)
        head = self.url['getListWithPage'][2]
        head['token'] = self.module.getToken(self.url['login'])

        r = self.module.re(self.url['getListWithPage'])
        self.log.info(r.json())
        return jsonpath.jsonpath(r.json(), '..robotCode')

    def getstationName(self):
        """获取当前拣货点"""
        data = self.mysql.select("select t1.robot_code as robotCode,t2.internal_station_name as stationName,(select "
                                 "t_wave.original_wave_no from t_wave where t_wave.id=t1.wave_id) taskNo from "
                                 "t_robot_task t1,t_robot_task_detail t2 where t1.id=t2.task_id and t1.`status`=200 "
                                 "and t2.`status`=100 and t2.arrival_time is not null", fetch=False)
        self.log.info(f'查询机器人点位：{data[1]}')
        return data[1]

    def getstatusDesc(self, value):
        """
        获取任务状态
        :param value: 任务状态：创建&拣货中&拣货完成
        :return: 查询到的任务状态
        """
        self.log.info('查询任务状态')
        for i in range(1, 200):
            time.sleep(5)
            self.url['getListWithPage'][3]['originalWaveNo'] = self.taskNo
            r = self.module.re(self.url['getListWithPage'])
            if jsonpath.jsonpath(r.json(), '$..statusDesc')[0] == value:
                self.log.info('{}任务状态{}'.format(self.taskNo, jsonpath.jsonpath(r.json(), '$..statusDesc')[0]))
                break
        return jsonpath.jsonpath(r.json(), '$..statusDesc')[0]

    def operateRobot_10(self):
        """提前到达"""
        self.log.info('点击提前到达')
        time.sleep(5)
        self.url['operateRobot_10'][3]['robotCode'] = self.getRobotNo()
        try:
            r = self.module.re(self.url['operateRobot_10'])
            if jsonpath.jsonpath(r.json(),"$..statusCode")[0] == 0:
                self.log.info('提前到达完成')
        except:
            self.log.info('{}提前到达结果{}'.format(self.getRobotNo(), r.json()))
            return 0
        else:
            time.sleep(5)
            return 1

    def pickStationFinish(self):
        """拣货完成"""
        self.log.info('开始拣货')
        self.url['pickStationFinish'][3]['robotCode'] = self.getRobotNo()
        self.url['pickStationFinish'][3]['stationName'] = self.getstationName()
        r = self.module.re(self.url['pickStationFinish'])
        self.log.info('拣货完成结果：{}'.format(r.json()))
        return 1

    def freedAMR(self):
        """卸货完成"""
        self.log.info('开始卸货')
        self.url['freedAMR'][3]['robotCode'] = self.getRobotNo()
        r = self.module.re(self.url['freedAMR'])
        try:
            if jsonpath.jsonpath(r.json(), "$..statusCode") == 0:
                self.log.info('卸货完成')
            else:
                self.log.error('请求入参：{}'.format(r.request.body))
                self.log.error('请求地址：{}'.format(r.request.url))

                raise
        except:
            self.log.error('卸货失败结果：{}'.format(r.json()))

        else:
            return 1

    def operateRobot_4(self):
        """释放点位"""
        self.log.info('开始释放点位')
        time.sleep(5)
        self.url['operateRobot_4'][3]['robotCode'] = self.getRobotNo()
        r = self.module.re(self.url['operateRobot_4'])
        self.log.info('{}释放点位结果{}'.format(self.getRobotNo(), r.json()))
        time.sleep(5)

    def handle(self):
        """
        异常处理
        :return:
        """
        for i in range(1, 100):
            self.log.info('准备异常处理')
            time.sleep(5)
            self.url['handlePage'][2]['token'] = self.module.getToken(self.url['login'])
            page_data = self.module.re(self.url['handlePage']).json()['result']['items'][0]
            self.url['handle'][3]['id'] = page_data['id']
            self.url['handle'][3]['exceptionEventCode'] = page_data['exceptionEventCode']
            self.url['handle'][3]['exceptionType'] = page_data['exceptionType']
            self.url['handle'][3]['exceptionTypeDesc'] = page_data['exceptionTypeDesc']
            self.url['handle'][3]['exceptionLocation'] = page_data['exceptionLocation']
            self.url['handle'][3]['robotCode'] = page_data['robotCode']
            self.url['handle'][3]['containerCode'] = page_data['containerCode']
            self.url['handle'][3]['createTime'] = page_data['createTime']
            self.url['handle'][3]['updateTime'] = page_data['updateTime']

            self.url['handle'][2]['token'] = self.module.getToken(self.url['login'])
            r = self.module.re(self.url['handle'])
            self.log.info('{}异常处理结果{}'.format(self.getRobotNo(), r.json()))
            time.sleep(5)


if __name__ == '__main__':
    a = Jd_Class()
    print(a.getRobotNo())

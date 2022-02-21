# -*- coding: utf-8 -*- 
# @Time : 2022/1/20 22:55 
# @Author : Yu yang
# @File : help.py


"""
命令行找不到自定义模块路径： Extertnal Libraries -- site-packages下创建.fth写入项目根目录

目录结构：
common：封装公共模块及常用常用方法
config：存放配置文件
data：存放测试护具
item：存放项目项目基类，保证各项目隔离性
log：存放项目测试过程的日志
testcase：存放测试用例

通过不同项目封装对应项目业务方法存放于item目录，测试用例类中实例化对应项目类

"""


from selenium import webdriver

driver = webdriver.Chrome()
driver.get(r'C:\Users\yuyang\PycharmProjects\pythonProject\report\2022-02-10 19~04~11result.html')
driver.maximize_window()
# driver.get_screenshot_as_png(r'C:\Users\yuyang\PycharmProjects\pythonProject\png\1.jpg')
driver.get_screenshot_as_file(r'C:\Users\yuyang\PycharmProjects\pythonProject\png\1.png')

import time
import unittest
import HTMLTestRunner
from common.path import test_dir


def runtest():
    # 定义测试用例路径

    # 存放报告的文件夹
    report_dir = './report'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern="test22.py", top_level_dir=None)
    # 报告命名时间格式化
    now = time.strftime("%Y-%m-%d %H~%M~%S")
    # 报告文件完整路径
    report_name = report_dir + '/' + now + 'result.html'
    with open(report_name, 'wb')as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title=' 测试结果如下：', description='用例执行情况：')
        # 执行测试用例文件
        runner.run(discover)


if __name__ == '__main__':
    runtest()
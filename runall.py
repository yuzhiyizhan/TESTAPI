import unittest
from Testapi.Commom.HTMLTestRunner3 import HTMLTestRunner
from Testapi.config.config import REPORT_PATH
from Testapi.config.config import TESTCASE

if __name__ == '__main__':
    cszx = unittest.defaultTestLoader.discover(start_dir=TESTCASE)
    with open(f'{REPORT_PATH}', 'wb') as f:
        runner = HTMLTestRunner(
            stream=f,
            title='测试',
            description='免费api接口测试报告',
            verbosity=2
        )
        runner.run(cszx)

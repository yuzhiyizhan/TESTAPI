import os
import time

# 项目路径
PATH = os.path.join(os.getcwd(), 'Testapi')
# 日志存放路径
LOG_PATH = os.path.join(PATH, 'log')
# 日志名默认为时期
LOG_NAME = os.path.join(LOG_PATH, f'{time.strftime("%Y-%m-%d", time.localtime())}.log')
# 测试用例文档(格式需为.xls)
FILES_NAME = 'APi.xls'
# 接口文档存放路径
FILES_PATH = os.path.join(PATH, 'files')
# 测试文件
FILES = os.path.join(FILES_PATH, FILES_NAME)
# 测试报告路径
SAVE_CASE = os.path.join(PATH, 'report')
# 测试报告文件名(默认为时间)
REPORT_NAME = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
# 测试报告保存文件名
REPORT_PATH = os.path.join(SAVE_CASE, f'{REPORT_NAME}' + '.html')
#.xls报告路径
REPORT_SAVE = os.path.join(SAVE_CASE, f'{time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())}.xls')
#操作第几张表
TABLE = 0
#测试用例存放路径
TESTCASE = os.path.join(PATH, 'testcase')

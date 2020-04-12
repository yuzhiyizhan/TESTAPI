import re
import ast
from loguru import logger
import xlrd
import requests
from xlutils.copy import copy
from Testapi.config.config import TABLE
from Testapi.config.config import FILES
from Testapi.config.config import RESPONSE_TIME
from Testapi.config.config import RESPONSE_MESSAGE
from Testapi.Commom.log import Log


class Reques(object):

    def __init__(self):

        # 打开.xls表
        self.work_book = xlrd.open_workbook(FILES, formatting_info=True)
        # 复制表
        self.work_book_copy = copy(self.work_book)
        # 选择打开后的文件里面的第几张表
        self.work_sheet = self.work_book.sheet_by_name(self.work_book.sheet_names()[TABLE])
        # 复制表后新建一张表
        self.work_book_sheet = self.work_book_copy.get_sheet(0)
        # 查看表有多少列
        self.num = self.work_sheet.nrows
        # 将列保存起来调用一次用例就删掉一列
        self.work = list(range(1, self.num))

    def subb(self, string, *args):
        '''
        将中文‘’转化成英文''
        :param string: 要转化的字符串
        :param args: 将什么转化成'
        :return: None
        '''
        s = args
        p = []
        for i in s:
            rp = re.sub(str(i), "'", str(string))
            string = rp
            p.append(string)
        return p[-1]

    def IF_json(self, test, response_result):
        '''
        对比字典KEY的值是否一致
        :param test: 要关注的参数(自己写的字典)
        :param response_result: 响应的字典
        :return: 测试通过不返回,失败返回'NONE'
        '''
        IF_list = list(test.keys())
        for i in IF_list:
            if i in response_result:
                if str(test[i]) == str(response_result[i]):
                    log = f'参数返回{response_result[i]}True'
                    Log(log)
                    print(log)
                    continue
                else:
                    log = f'参数返回{test[i]}False'
                    Log(log)
                    print(log)
                    self.work_book_sheet.write(self.rows, 6, 'False')
                    return 'NONE'
            else:
                Log(f'{test[i]}需要关注的参数不在响应中,测试不通过')
                print(f'{test[i]}需要关注的参数不在响应中,测试不通过')
                self.work_book_sheet.write(self.rows, 6, 'False')
                return 'NONE'

        try:
            self.work_book_sheet.write(self.rows, 6, 'True')
        except:
            pass

    def Request(self, test=None, skip=None):
        '''
        操作打开的测试用例
        :param test: 需要关注的参数,此处填写将不再关注全局参数,目前只支持字典格式
        :param skip: 此处天'skip'时将跳过用例
        :return: 测试用例成功返回'NONE',失败返回默认值None
        '''
        if skip == 'skip':
            self.rows = self.work.pop(0)
            self.name = self.work_sheet.cell_value(self.rows, 1)
            self.url = self.work_sheet.cell_value(self.rows, 3)
            log = f'跳过用例名为:{self.name},接口为{self.url}'
            print(log)
            Log(log)
            self.work_book_sheet.write(self.rows, 6, log)
        else:
            self.rows = self.work.pop(0)
            self.name = self.work_sheet.cell_value(self.rows, 1)
            Request_way = self.work_sheet.cell_value(self.rows, 2)
            self.url = self.work_sheet.cell_value(self.rows, 3)
            try:
                self.data = ast.literal_eval(
                    self.subb(re.sub(' ', '', self.work_sheet.cell_value(self.rows, 4)), '‘', '’'))
            except:
                self.data = self.work_sheet.cell_value(self.rows, 4)
            try:
                response_result = ast.literal_eval(
                    self.subb(re.sub(' ', '', self.work_sheet.cell_value(self.rows, 5)), '‘', '’'))
            except:
                response_result = self.work_sheet.cell_value(self.rows, 5)
            Log(f'正在运行第{self.rows}条接口')
            print(f'正在运行第{self.rows}条接口')
            Log(f'接口名{self.name}')
            print(f'接口名{self.name}')
            Log(f'接口url为{self.url}')
            print(f'接口url为{self.url}')
            if 'GET' in Request_way:
                response = requests.get(url=self.url, verify=False)
                seconds = response.elapsed.total_seconds()  # 响应时间,单位/s
                Log(f'接口响应时间为{seconds}')
                print(f'接口响应时间为{seconds}')
                status_code = response.status_code
                Log(f'接口响应码为{status_code}')
                print(f'接口响应码为{status_code}')
                try:
                    text = response.json()
                except:
                    text = response.text
                self.work_book_sheet.write(self.rows, 7, str(seconds) + '/s')
                if RESPONSE_TIME > seconds:
                    Log(f'响应时间小于{RESPONSE_TIME}')
                    print(f'响应时间小于{RESPONSE_TIME}')
                else:
                    Log(f'响应时间大于{RESPONSE_TIME}')
                    print(f'响应时间大于{RESPONSE_TIME}')
                if len(response_result) > 0:
                    if type(response_result) == dict:
                        if type(text) == dict:
                            NONE = self.IF_json(text, response_result)
                            if NONE == None:
                                return 'NONE'
                        else:
                            if text > 0:
                                Log(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                print(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')
                            else:

                                Log(f'{self.name}接口无返回,文档为json,测试不通过')
                                print(f'{self.name}接口无返回,文档为json,测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')

                    else:
                        if type(text) == dict:
                            Log(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                            print(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                            self.work_book_sheet.write(self.rows, 6, 'False')
                        else:
                            if text in response_result:
                                Log(f'接口:{self.name}测试通过')
                                print(f'接口:{self.name}测试通过')
                                self.work_book_sheet.write(self.rows, 6, 'True')
                                return 'NONE'
                            else:
                                Log(f'接口:{self.name}响应与文档不对应,测试不通过')
                                print(f'接口:{self.name}响应与文档不对应,测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')
                if len(response_result) == 0:
                    if test:
                        if type(text) == dict:
                            NONE = self.IF_json(test, text)
                            if NONE == None:
                                return 'NONE'
                        else:
                            Log(f'{self.name}接口响应为文本类型,测试不通过')
                            print(f'{self.name}接口响应为文本类型,测试不通过')
                            self.work_book_sheet.write(self.rows, 6, 'False')
                    else:
                        if RESPONSE_MESSAGE:
                            if type(text) == dict:
                                NONE = self.IF_json(RESPONSE_MESSAGE, text)
                                if NONE == None:
                                    return 'NONE'
                            else:
                                Log(f'{self.name}接口响应为文本类型,测试不通过')
                                print(f'{self.name}接口响应为文本类型,测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')
                        else:
                            if status_code == 200:
                                Log(f'{self.name}接口测试通过')
                                print(f'{self.name}接口测试通过')
                                self.work_book_sheet.write(self.rows, 6, 'True')
                                return 'NONE'

                            else:
                                Log(f'{self.name}接口测试不通过')
                                print(f'{self.name}接口测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')
            if 'POST' in Request_way:
                if self.data:
                    if type(self.data) == dict:
                        response = requests.post(url=self.url, data=self.data, verify=False)
                        seconds = response.elapsed.total_seconds()  # 响应时间,单位/s
                        Log(f'接口响应时间为{seconds}')
                        print(f'接口响应时间为{seconds}')
                        status_code = response.status_code
                        Log(f'接口响应码为{status_code}')
                        print(f'接口响应码为{status_code}')
                        try:
                            text = response.json()
                        except:
                            text = response.text
                        self.work_book_sheet.write(self.rows, 7, str(seconds) + '/s')
                        if RESPONSE_TIME > seconds:
                            Log(f'响应时间小于{RESPONSE_TIME}')
                            print(f'响应时间小于{RESPONSE_TIME}')
                        else:
                            Log(f'响应时间大于{RESPONSE_TIME}')
                            print(f'响应时间大于{RESPONSE_TIME}')
                        if len(response_result) > 0:
                            if type(response_result) == dict:
                                if type(text) == dict:
                                    NONE = self.IF_json(text, response_result)
                                    if NONE == None:
                                        return 'NONE'
                                else:
                                    if text > 0:
                                        Log(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                        print(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                        self.work_book_sheet.write(self.rows, 6, 'False')
                                    else:
                                        Log(f'{self.name}接口无返回,文档为json,测试不通过')
                                        print(f'{self.name}接口无返回,文档为json,测试不通过')
                                        self.work_book_sheet.write(self.rows, 6, 'False')

                            else:
                                if type(text) == dict:
                                    Log(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                    print(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                else:
                                    if text in response_result:
                                        Log(f'接口:{self.name}测试通过')
                                        print(f'接口:{self.name}测试通过')
                                        self.work_book_sheet.write(self.rows, 6, 'True')
                                        return 'NONE'
                                    else:
                                        Log(f'接口:{self.name}响应与文档不对应,测试不通过')
                                        print(f'接口:{self.name}响应与文档不对应,测试不通过')
                                        self.work_book_sheet.write(self.rows, 6, 'False')
                        if len(response_result) == 0:
                            if test:
                                if type(text) == dict:
                                    NONE = self.IF_json(test, text)
                                    if NONE == None:
                                        return 'NONE'
                                else:
                                    Log(f'{self.name}接口响应为文本类型,测试不通过')
                                    print(f'{self.name}接口响应为文本类型,测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')
                            else:
                                if RESPONSE_MESSAGE:
                                    if type(text) == dict:
                                        NONE = self.IF_json(RESPONSE_MESSAGE, text)
                                        if NONE == None:
                                            return 'NONE'
                                    else:
                                        Log(f'{self.name}接口响应为文本类型,测试不通过')
                                        print(f'{self.name}接口响应为文本类型,测试不通过')
                                        self.work_book_sheet.write(self.rows, 6, 'False')
                                else:
                                    if status_code == 200:
                                        Log(f'{self.name}接口测试通过')
                                        print(f'{self.name}接口测试通过')
                                        self.work_book_sheet.write(self.rows, 6, 'True')
                                        return 'NONE'

                                    else:
                                        Log(f'{self.name}接口测试不通过')
                                        print(f'{self.name}接口测试不通过')
                                        self.work_book_sheet.write(self.rows, 6, 'False')
                                        if len(response_result) > 0:
                                            if type(response_result) == dict:
                                                if type(text) == dict:
                                                    NONE = self.IF_json(text, response_result)
                                                    if NONE == None:
                                                        return 'NONE'
                                                else:
                                                    if text > 0:
                                                        Log(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                                        print(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'False')
                                                    else:
                                                        Log(f'{self.name}接口无返回,文档为json,测试不通过')
                                                        print(f'{self.name}接口无返回,文档为json,测试不通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'False')

                                            else:
                                                if type(text) == dict:
                                                    Log(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                                    print(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                                else:
                                                    if text in response_result:
                                                        Log(f'接口:{self.name}测试通过')
                                                        print(f'接口:{self.name}测试通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'True')
                                                        return 'NONE'
                                                    else:
                                                        Log(f'接口:{self.name}响应与文档不对应,测试不通过')
                                                        print(f'接口:{self.name}响应与文档不对应,测试不通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'False')
                                        if len(response_result) == 0:
                                            if test:
                                                if type(text) == dict:
                                                    NONE = self.IF_json(test, text)
                                                    if NONE == None:
                                                        return NONE
                                                else:
                                                    Log(f'{self.name}接口响应为文本类型,测试不通过')
                                                    print(f'{self.name}接口响应为文本类型,测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                            else:
                                                if RESPONSE_MESSAGE:
                                                    if type(text) == dict:
                                                        NONE = self.IF_json(RESPONSE_MESSAGE, text)
                                                        if NONE == None:
                                                            return 'NONE'
                                                    else:
                                                        Log(f'{self.name}接口响应为文本类型,测试不通过')
                                                        print(f'{self.name}接口响应为文本类型,测试不通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'False')
                                                else:
                                                    if status_code == 200:
                                                        Log(f'{self.name}接口测试通过')
                                                        print(f'{self.name}接口测试通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'True')
                                                        return 'NONE'

                                                    else:
                                                        Log(f'{self.name}接口测试不通过')
                                                        print(f'{self.name}接口测试不通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'False')
                    else:
                        log = f'文档data不为json类型,{self.name}接口测试失败'
                        Log(log)
                        print(log)
                        self.work_book_sheet.write(self.rows, 6, 'False')
                else:
                    response = requests.post(url=self.url, verify=False)
                    seconds = response.elapsed.total_seconds()  # 响应时间,单位/s

                    try:
                        text = response.json()
                    except:
                        text = response.text
                    self.work_book_sheet.write(self.rows, 7, str(seconds) + '/s')
                    if RESPONSE_TIME > seconds:
                        Log(f'响应时间小于{RESPONSE_TIME}')
                        print(f'响应时间小于{RESPONSE_TIME}')
                    else:
                        Log(f'响应时间大于{RESPONSE_TIME}')
                        print(f'响应时间大于{RESPONSE_TIME}')
                    Log(f'接口响应时间为{seconds}')
                    print(f'接口响应时间为{seconds}')
                    status_code = response.status_code
                    Log(f'接口响应码为{status_code}')
                    print(f'接口响应码为{status_code}')
                    if len(response_result) > 0:
                        if type(response_result) == dict:
                            if type(text) == dict:
                                NONE = self.IF_json(text, response_result)
                                if NONE == None:
                                    return 'NONE'
                            else:
                                if text > 0:
                                    Log(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                    print(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                else:
                                    Log(f'{self.name}接口无返回,文档为json,测试不通过')
                                    print(f'{self.name}接口无返回,文档为json,测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')

                        else:
                            if type(text) == dict:
                                Log(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                print(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')
                            else:
                                if text in response_result:
                                    Log(f'接口:{self.name}测试通过')
                                    print(f'接口:{self.name}测试通过')
                                    self.work_book_sheet.write(self.rows, 6, 'True')
                                    return 'NONE'
                                else:
                                    Log(f'接口:{self.name}响应与文档不对应,测试不通过')
                                    print(f'接口:{self.name}响应与文档不对应,测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')
                    if len(response_result) == 0:
                        if test:
                            if type(text) == dict:
                                NONE = self.IF_json(test, text)
                                if NONE == None:
                                    return 'NONE'
                            else:
                                Log(f'{self.name}接口响应为文本类型,测试不通过')
                                print(f'{self.name}接口响应为文本类型,测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')
                        else:
                            if RESPONSE_MESSAGE:
                                if type(text) == dict:
                                    NONE = self.IF_json(RESPONSE_MESSAGE, text)
                                    if NONE == None:
                                        return 'NONE'
                                else:
                                    Log(f'{self.name}接口响应为文本类型,测试不通过')
                                    print(f'{self.name}接口响应为文本类型,测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')
                            else:
                                if status_code == 200:
                                    Log(f'{self.name}接口测试通过')
                                    print(f'{self.name}接口测试通过')
                                    self.work_book_sheet.write(self.rows, 6, 'True')
                                    return 'NONE'

                                else:
                                    Log(f'{self.name}接口测试不通过')
                                    print(f'{self.name}接口测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                    if len(response_result) > 0:
                                        if type(response_result) == dict:
                                            if type(text) == dict:
                                                NONE = self.IF_json(text, response_result)
                                                if NONE == None:
                                                    return 'NONE'
                                            else:
                                                if text > 0:
                                                    Log(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                                    print(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                                else:
                                                    Log(f'{self.name}接口无返回,文档为json,测试不通过')
                                                    print(f'{self.name}接口无返回,文档为json,测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')

                                        else:
                                            if type(text) == dict:
                                                Log(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                                print(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                                self.work_book_sheet.write(self.rows, 6, 'False')
                                            else:
                                                if text in response_result:
                                                    Log(f'接口:{self.name}测试通过')
                                                    print(f'接口:{self.name}测试通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'True')
                                                    return 'NONE'
                                                else:
                                                    Log(f'接口:{self.name}响应与文档不对应,测试不通过')
                                                    print(f'接口:{self.name}响应与文档不对应,测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                    if len(response_result) == 0:
                                        if test:
                                            if type(text) == dict:
                                                NONE = self.IF_json(test, text)
                                                if NONE == None:
                                                    return 'NONE'
                                            else:
                                                Log(f'{self.name}接口响应为文本类型,测试不通过')
                                                print(f'{self.name}接口响应为文本类型,测试不通过')
                                                self.work_book_sheet.write(self.rows, 6, 'False')
                                        else:
                                            if RESPONSE_MESSAGE:
                                                if type(text) == dict:
                                                    NONE = self.IF_json(RESPONSE_MESSAGE, text)
                                                    if NONE == None:
                                                        return 'NONE'
                                                else:
                                                    Log(f'{self.name}接口响应为文本类型,测试不通过')
                                                    print(f'{self.name}接口响应为文本类型,测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                            else:
                                                if status_code == 200:
                                                    Log(f'{self.name}接口测试通过')
                                                    print(f'{self.name}接口测试通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'True')
                                                    return 'NONE'

                                                else:
                                                    Log(f'{self.name}接口测试不通过')
                                                    print(f'{self.name}接口测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')

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
from unittest.util import (strclass, _count_diff_all_purpose,
                           _count_diff_hashable, _common_shorten_repr)

__unittest = True
_subtest_msg_sentinel = object()
_MAX_LENGTH = 80


def safe_repr(obj, short=False):
    try:
        result = repr(obj)
    except Exception:
        result = object.__repr__(obj)
    if not short or len(result) < _MAX_LENGTH:
        return result
    return result[:_MAX_LENGTH] + ' [truncated]...'


class Reques(object):
    longMessage = True
    failureException = AssertionError

    @logger.catch
    def __init__(self):
        self.work_book = xlrd.open_workbook(FILES, formatting_info=True)
        self.work_book_copy = copy(self.work_book)
        self.work_sheet = self.work_book.sheet_by_name(self.work_book.sheet_names()[TABLE])
        self.work_book_sheet = self.work_book_copy.get_sheet(0)
        self.num = self.work_sheet.nrows
        self.work = list(range(1, self.num))
        self._type_equality_funcs = {}

    @logger.catch
    def _formatMessage(self, msg, standardMsg):
        """Honour the longMessage attribute when generating failure messages.
        If longMessage is False this means:
        * Use only an explicit message if it is provided
        * Otherwise use the standard message for the assert

        If longMessage is True:
        * Use the standard message
        * If an explicit message is provided, plus ' : ' and the explicit message
        """
        if not self.longMessage:
            return msg or standardMsg
        if msg is None:
            return standardMsg
        try:
            # don't switch to '{}' formatting in Python 2.X
            # it changes the way unicode input is handled
            return '%s : %s' % (standardMsg, msg)
        except UnicodeDecodeError:
            return '%s : %s' % (safe_repr(standardMsg), safe_repr(msg))

    @logger.catch
    def fail(self, msg=None):
        """Fail immediately, with the given message."""
        raise self.failureException(msg)

    @logger.catch
    def assertIn(self, member, container, msg=None):
        """Just like self.assertTrue(a in b), but with a nicer default message."""
        if member not in container:
            standardMsg = '%s not found in %s' % (safe_repr(member),
                                                  safe_repr(container))
            self.fail(self._formatMessage(msg, standardMsg))

    @logger.catch
    def assertGreater(self, a, b, msg=None):
        """Just like self.assertTrue(a > b), but with a nicer default message."""
        if not a > b:
            standardMsg = '%s not greater than %s' % (safe_repr(a), safe_repr(b))
            self.fail(self._formatMessage(msg, standardMsg))

    @logger.catch
    def assertEqual(self, first, second, msg=None):
        """Fail if the two objects are unequal as determined by the '=='
           operator.
        """
        assertion_func = self._getAssertEqualityFunc(first, second)
        assertion_func(first, second, msg=msg)

    @logger.catch
    def assertIsNone(self, obj, msg=None):
        """Same as self.assertTrue(obj is None), with a nicer default message."""
        if obj is not None:
            standardMsg = '%s is not None' % (safe_repr(obj),)
            self.fail(self._formatMessage(msg, standardMsg))

    @logger.catch
    def _getAssertEqualityFunc(self, first, second):
        """Get a detailed comparison function for the types of the two args.

        Returns: A callable accepting (first, second, msg=None) that will
        raise a failure exception if first != second with a useful human
        readable error message for those types.
        """
        #
        # NOTE(gregory.p.smith): I considered isinstance(first, type(second))
        # and vice versa.  I opted for the conservative approach in case
        # subclasses are not intended to be compared in detail to their super
        # class instances using a type equality func.  This means testing
        # subtypes won't automagically use the detailed comparison.  Callers
        # should use their type specific assertSpamEqual method to compare
        # subclasses if the detailed comparison is desired and appropriate.
        # See the discussion in http://bugs.python.org/issue2578.
        #
        if type(first) is type(second):
            asserter = self._type_equality_funcs.get(type(first))
            if asserter is not None:
                if isinstance(asserter, str):
                    asserter = getattr(self, asserter)
                return asserter

        return self._baseAssertEqual

    @logger.catch
    def _baseAssertEqual(self, first, second, msg=None):
        """The default assertEqual implementation, not type specific."""
        if not first == second:
            standardMsg = '%s != %s' % _common_shorten_repr(first, second)
            msg = self._formatMessage(msg, standardMsg)
            raise self.failureException(msg)

    @logger.catch
    def subb(self, string, *args):
        s = args
        p = []
        for i in s:
            rp = re.sub(str(i), "'", str(string))
            string = rp
            p.append(string)
        return p[-1]

    @logger.catch
    def IF_json(self, test, response_result):
        IF_list = list(test.keys())
        for i in IF_list:
            if i in response_result:
                self.assertEqual(test[i], response_result[i])
                if str(test[i]) == str(response_result[i]):
                    log = f'参数返回{response_result[i]}True'
                    Log(log)
                    print(log)
                if str(test[i]) != str(response_result[i]):
                    log = f'参数返回{test[i]}False'
                    Log(log)
                    print(log)
                    self.work_book_sheet.write(self.rows, 6, 'False')
                    break
            else:
                self.assertIsNone(f'{test[i]}需要关注的参数不在响应中,测试不通过')
                Log(f'{test[i]}需要关注的参数不在响应中,测试不通过')
                print(f'{test[i]}需要关注的参数不在响应中,测试不通过')
                self.work_book_sheet.write(self.rows, 6, 'False')
                break
        try:
            self.work_book_sheet.write(self.rows, 6, 'True')
        except:
            pass

    @logger.catch
    def Request(self, test=None, skip=None):
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
            Log(f'正在运行{self.rows}条接口')
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
                self.assertGreater(RESPONSE_TIME, seconds)
                if RESPONSE_TIME > seconds:
                    Log(f'响应时间小于{RESPONSE_TIME}')
                    print(f'响应时间小于{RESPONSE_TIME}')
                else:
                    Log(f'响应时间大于{RESPONSE_TIME}')
                    print(f'响应时间大于{RESPONSE_TIME}')
                if len(response_result) > 0:
                    if type(response_result) == dict:
                        if type(text) == dict:
                            self.IF_json(text, response_result)
                        else:
                            if text > 0:
                                self.assertIsNone(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                Log(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                print(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')
                            else:
                                self.assertIsNone(f'{self.name}接口无返回,文档为json,测试不通过')
                                Log(f'{self.name}接口无返回,文档为json,测试不通过')
                                print(f'{self.name}接口无返回,文档为json,测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')

                    else:
                        if type(text) == dict:
                            self.assertIsNone(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                            Log(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                            print(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                            self.work_book_sheet.write(self.rows, 6, 'False')
                        else:
                            self.assertIn(text, response_result)
                            if text in response_result:
                                Log(f'接口:{self.name}测试通过')
                                print(f'接口:{self.name}测试通过')
                                self.work_book_sheet.write(self.rows, 6, 'True')
                            else:
                                Log(f'接口:{self.name}响应与文档不对应,测试不通过')
                                print(f'接口:{self.name}响应与文档不对应,测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')
                if len(response_result) == 0:
                    if test:
                        if type(text) == dict:
                            self.IF_json(test, text)
                        else:
                            self.assertIsNone(f'{self.name}接口响应为文本类型,测试不通过')
                            Log(f'{self.name}接口响应为文本类型,测试不通过')
                            print(f'{self.name}接口响应为文本类型,测试不通过')
                            self.work_book_sheet.write(self.rows, 6, 'False')
                    else:
                        if RESPONSE_MESSAGE:
                            if type(text) == dict:
                                self.IF_json(RESPONSE_MESSAGE, text)
                            else:
                                self.assertIsNone(f'{self.name}接口响应为文本类型,测试不通过')
                                Log(f'{self.name}接口响应为文本类型,测试不通过')
                                print(f'{self.name}接口响应为文本类型,测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')
                        else:
                            self.assertEqual(status_code, 200)
                            if status_code == 200:
                                Log(f'{self.name}接口测试通过')
                                print(f'{self.name}接口测试通过')
                                self.work_book_sheet.write(self.rows, 6, 'True')

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
                        self.assertGreater(RESPONSE_TIME, seconds)
                        if RESPONSE_TIME > seconds:
                            Log(f'响应时间小于{RESPONSE_TIME}')
                            print(f'响应时间小于{RESPONSE_TIME}')
                        else:
                            Log(f'响应时间大于{RESPONSE_TIME}')
                            print(f'响应时间大于{RESPONSE_TIME}')
                        if len(response_result) > 0:
                            if type(response_result) == dict:
                                if type(text) == dict:
                                    self.IF_json(text, response_result)
                                else:
                                    if text > 0:
                                        self.assertIsNone(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                        Log(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                        print(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                        self.work_book_sheet.write(self.rows, 6, 'False')
                                    else:
                                        self.assertIsNone(f'{self.name}接口无返回,文档为json,测试不通过')
                                        Log(f'{self.name}接口无返回,文档为json,测试不通过')
                                        print(f'{self.name}接口无返回,文档为json,测试不通过')
                                        self.work_book_sheet.write(self.rows, 6, 'False')

                            else:
                                if type(text) == dict:
                                    self.assertIsNone(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                    Log(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                    print(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                else:
                                    self.assertIn(text, response_result)
                                    if text in response_result:
                                        Log(f'接口:{self.name}测试通过')
                                        print(f'接口:{self.name}测试通过')
                                        self.work_book_sheet.write(self.rows, 6, 'True')
                                    else:
                                        Log(f'接口:{self.name}响应与文档不对应,测试不通过')
                                        print(f'接口:{self.name}响应与文档不对应,测试不通过')
                                        self.work_book_sheet.write(self.rows, 6, 'False')
                        if len(response_result) == 0:
                            if test:
                                if type(text) == dict:
                                    self.IF_json(test, text)
                                else:
                                    self.assertIsNone(f'{self.name}接口响应为文本类型,测试不通过')
                                    Log(f'{self.name}接口响应为文本类型,测试不通过')
                                    print(f'{self.name}接口响应为文本类型,测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')
                            else:
                                if RESPONSE_MESSAGE:
                                    if type(text) == dict:
                                        self.IF_json(RESPONSE_MESSAGE, text)
                                    else:
                                        self.assertIsNone(f'{self.name}接口响应为文本类型,测试不通过')
                                        Log(f'{self.name}接口响应为文本类型,测试不通过')
                                        print(f'{self.name}接口响应为文本类型,测试不通过')
                                        self.work_book_sheet.write(self.rows, 6, 'False')
                                else:
                                    self.assertEqual(status_code, 200)
                                    if status_code == 200:
                                        Log(f'{self.name}接口测试通过')
                                        print(f'{self.name}接口测试通过')
                                        self.work_book_sheet.write(self.rows, 6, 'True')

                                    else:
                                        Log(f'{self.name}接口测试不通过')
                                        print(f'{self.name}接口测试不通过')
                                        self.work_book_sheet.write(self.rows, 6, 'False')
                                        if len(response_result) > 0:
                                            if type(response_result) == dict:
                                                if type(text) == dict:
                                                    self.IF_json(text, response_result)
                                                else:
                                                    if text > 0:
                                                        self.assertIsNone(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                                        Log(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                                        print(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'False')
                                                    else:
                                                        self.assertIsNone(f'{self.name}接口无返回,文档为json,测试不通过')
                                                        Log(f'{self.name}接口无返回,文档为json,测试不通过')
                                                        print(f'{self.name}接口无返回,文档为json,测试不通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'False')

                                            else:
                                                if type(text) == dict:
                                                    self.assertIsNone(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                                    Log(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                                    print(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                                else:
                                                    self.assertIn(text, response_result)
                                                    if text in response_result:
                                                        Log(f'接口:{self.name}测试通过')
                                                        print(f'接口:{self.name}测试通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'True')
                                                    else:
                                                        Log(f'接口:{self.name}响应与文档不对应,测试不通过')
                                                        print(f'接口:{self.name}响应与文档不对应,测试不通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'False')
                                        if len(response_result) == 0:
                                            if test:
                                                if type(text) == dict:
                                                    self.IF_json(test, text)
                                                else:
                                                    self.assertIsNone(f'{self.name}接口响应为文本类型,测试不通过')
                                                    Log(f'{self.name}接口响应为文本类型,测试不通过')
                                                    print(f'{self.name}接口响应为文本类型,测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                            else:
                                                if RESPONSE_MESSAGE:
                                                    if type(text) == dict:
                                                        self.IF_json(RESPONSE_MESSAGE, text)
                                                    else:
                                                        self.assertIsNone(f'{self.name}接口响应为文本类型,测试不通过')
                                                        Log(f'{self.name}接口响应为文本类型,测试不通过')
                                                        print(f'{self.name}接口响应为文本类型,测试不通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'False')
                                                else:
                                                    self.assertEqual(status_code, 200)
                                                    if status_code == 200:
                                                        Log(f'{self.name}接口测试通过')
                                                        print(f'{self.name}接口测试通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'True')

                                                    else:
                                                        Log(f'{self.name}接口测试不通过')
                                                        print(f'{self.name}接口测试不通过')
                                                        self.work_book_sheet.write(self.rows, 6, 'False')
                    else:
                        log = f'文档data不为json类型,{self.name}接口测试失败'
                        self.assertIsNone(log)
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
                    self.assertGreater(RESPONSE_TIME, seconds)
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
                                self.IF_json(text, response_result)
                            else:
                                if text > 0:
                                    self.assertIsNone(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                    Log(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                    print(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                else:
                                    self.assertIsNone(f'{self.name}接口无返回,文档为json,测试不通过')
                                    Log(f'{self.name}接口无返回,文档为json,测试不通过')
                                    print(f'{self.name}接口无返回,文档为json,测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')

                        else:
                            if type(text) == dict:
                                self.assertIsNone(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                Log(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                print(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')
                            else:
                                self.assertIn(text, response_result)
                                if text in response_result:
                                    Log(f'接口:{self.name}测试通过')
                                    print(f'接口:{self.name}测试通过')
                                    self.work_book_sheet.write(self.rows, 6, 'True')
                                else:
                                    Log(f'接口:{self.name}响应与文档不对应,测试不通过')
                                    print(f'接口:{self.name}响应与文档不对应,测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')
                    if len(response_result) == 0:
                        if test:
                            if type(text) == dict:
                                self.IF_json(test, text)
                            else:
                                self.assertIsNone(f'{self.name}接口响应为文本类型,测试不通过')
                                Log(f'{self.name}接口响应为文本类型,测试不通过')
                                print(f'{self.name}接口响应为文本类型,测试不通过')
                                self.work_book_sheet.write(self.rows, 6, 'False')
                        else:
                            if RESPONSE_MESSAGE:
                                if type(text) == dict:
                                    self.IF_json(RESPONSE_MESSAGE, text)
                                else:
                                    self.assertIsNone(f'{self.name}接口响应为文本类型,测试不通过')
                                    Log(f'{self.name}接口响应为文本类型,测试不通过')
                                    print(f'{self.name}接口响应为文本类型,测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')
                            else:
                                self.assertEqual(status_code, 200)
                                if status_code == 200:
                                    Log(f'{self.name}接口测试通过')
                                    print(f'{self.name}接口测试通过')
                                    self.work_book_sheet.write(self.rows, 6, 'True')

                                else:
                                    Log(f'{self.name}接口测试不通过')
                                    print(f'{self.name}接口测试不通过')
                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                    if len(response_result) > 0:
                                        if type(response_result) == dict:
                                            if type(text) == dict:
                                                self.IF_json(text, response_result)
                                            else:
                                                if text > 0:
                                                    self.assertIsNone(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                                    Log(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                                    print(f'{self.name}接口响应为文本类型,文档为json,测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                                else:
                                                    self.assertIsNone(f'{self.name}接口无返回,文档为json,测试不通过')
                                                    Log(f'{self.name}接口无返回,文档为json,测试不通过')
                                                    print(f'{self.name}接口无返回,文档为json,测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')

                                        else:
                                            if type(text) == dict:
                                                self.assertIsNone(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                                Log(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                                print(f'{self.name}接口响应为json类型,文档为其他类型,测试不通过')
                                                self.work_book_sheet.write(self.rows, 6, 'False')
                                            else:
                                                self.assertIn(text, response_result)
                                                if text in response_result:
                                                    Log(f'接口:{self.name}测试通过')
                                                    print(f'接口:{self.name}测试通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'True')
                                                else:
                                                    Log(f'接口:{self.name}响应与文档不对应,测试不通过')
                                                    print(f'接口:{self.name}响应与文档不对应,测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                    if len(response_result) == 0:
                                        if test:
                                            if type(text) == dict:
                                                self.IF_json(test, text)
                                            else:
                                                self.assertIsNone(f'{self.name}接口响应为文本类型,测试不通过')
                                                Log(f'{self.name}接口响应为文本类型,测试不通过')
                                                print(f'{self.name}接口响应为文本类型,测试不通过')
                                                self.work_book_sheet.write(self.rows, 6, 'False')
                                        else:
                                            if RESPONSE_MESSAGE:
                                                if type(text) == dict:
                                                    self.IF_json(RESPONSE_MESSAGE, text)
                                                else:
                                                    self.assertIsNone(f'{self.name}接口响应为文本类型,测试不通过')
                                                    Log(f'{self.name}接口响应为文本类型,测试不通过')
                                                    print(f'{self.name}接口响应为文本类型,测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')
                                            else:
                                                self.assertEqual(status_code, 200)
                                                if status_code == 200:
                                                    Log(f'{self.name}接口测试通过')
                                                    print(f'{self.name}接口测试通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'True')

                                                else:
                                                    Log(f'{self.name}接口测试不通过')
                                                    print(f'{self.name}接口测试不通过')
                                                    self.work_book_sheet.write(self.rows, 6, 'False')

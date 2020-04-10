import unittest
from Testapi.Commom.log import Log
from Testapi.config.config import FILES
from xlutils.copy import copy
import xlrd
from Testapi.config.config import REPORT_SAVE
from Testapi.config.config import TABLE
import requests


class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.work_book = xlrd.open_workbook(FILES, formatting_info=True)
        cls.work_book_copy = copy(cls.work_book)
        cls.work_sheet = cls.work_book.sheet_by_name(cls.work_book.sheet_names()[TABLE])
        cls.work_book_sheet = cls.work_book_copy.get_sheet(0)
        cls.num = cls.work_sheet.nrows
        cls.work = list(range(1, cls.num))
        Log('测试开始')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.work_book_copy.save(REPORT_SAVE)
        Log('测试结束')

    def Request(self):
        self.rows = self.work.pop(0)
        self.Request_way = self.work_sheet.cell_value(self.rows, 2)
        self.url = self.work_sheet.cell_value(self.rows, 3)
        self.data = self.work_sheet.cell_value(self.rows, 4)
        self.response_result = self.work_sheet.cell_value(self.rows, 5)
        if 'GET' in self.Request_way:
            response = requests.get(url=self.url)
            if len(self.response_result) > 0:
                self.assertIn(str(response.text), str(self.response_result))
                self.assertIn(str(response.status_code), str(200))
                if str(response.text) in str(self.response_result) and str(response.status_code) == str(200):
                    self.work_book_sheet.write(self.rows, 6, 'pass')
                else:
                    self.work_book_sheet.write(self.rows, 6, 'fail')
            else:
                self.assertIn(str(response.status_code), str(200))
                if str(response.status_code) == str(200):
                    self.work_book_sheet.write(self.rows, 6, 'pass')
                else:
                    self.work_book_sheet.write(self.rows, 6, 'fail')
            if 'POST' in self.Request_way:
                if len(self.data) > 0:
                    response = requests.post(url=self.url, data=self.data)
                    if len(self.response_result) > 0:
                        self.assertIn(str(response.text), str(self.response_result))
                        self.assertIn(str(response.status_code), str(200))
                        if str(response.text) in str(self.response_result) and str(response.status_code) == str(200):
                            self.work_book_sheet.write(self.rows, 6, 'pass')
                        else:
                            self.work_book_sheet.write(self.rows, 6, 'fail')
                    else:
                        self.assertIn(str(response.status_code), str(200))
                        if str(response.status_code) == str(200):
                            self.work_book_sheet.write(self.rows, 6, 'pass')
                        else:
                            self.work_book_sheet.write(self.rows, 6, 'fail')
                else:
                    response = requests.post(url=self.url)
                    if len(self.response_result) > 0:
                        self.assertIn(str(response.text), str(self.response_result))
                        self.assertIn(str(response.status_code), str(200))
                        if str(response.text) in str(self.response_result) and str(response.status_code) == str(200):
                            self.work_book_sheet.write(self.rows, 6, 'pass')
                        else:
                            self.work_book_sheet.write(self.rows, 6, 'fail')
                    else:
                        self.assertIn(str(response.status_code), str(200))
                        if str(response.status_code) == str(200):
                            self.work_book_sheet.write(self.rows, 6, 'pass')
                        else:
                            self.work_book_sheet.write(self.rows, 6, 'fail')

        if 'POST' in self.Request_way:
            if len(self.data) > 0:
                response = requests.post(url=self.url, data=self.data)
                if len(self.response_result) > 0:
                    self.assertIn(str(response.text), str(self.response_result))
                    self.assertIn(str(response.status_code), str(200))
                    if str(response.text) in str(self.response_result) and str(response.status_code) == str(200):
                        self.work_book_sheet.write(self.rows, 6, 'pass')
                    else:
                        self.work_book_sheet.write(self.rows, 6, 'fail')
                else:
                    self.assertIn(str(response.status_code), str(200))
                    if str(response.status_code) == str(200):
                        self.work_book_sheet.write(self.rows, 6, 'pass')
                    else:
                        self.work_book_sheet.write(self.rows, 6, 'fail')
            else:
                response = requests.post(url=self.url)
                if len(self.response_result) > 0:
                    self.assertIn(str(response.text), str(self.response_result))
                    self.assertIn(str(response.status_code), str(200))
                    if str(response.text) in str(self.response_result) and str(response.status_code) == str(200):
                        self.work_book_sheet.write(self.rows, 6, 'pass')
                    else:
                        self.work_book_sheet.write(self.rows, 6, 'fail')
                else:
                    self.assertIn(str(response.status_code), str(200))
                    if str(response.text) in str(self.response_result) and str(response.status_code) == str(200):
                        self.work_book_sheet.write(self.rows, 6, 'pass')
                    else:
                        self.work_book_sheet.write(self.rows, 6, 'fail')

    def test_01(self):
        self.Request()

    def test_02(self):
        self.Request()

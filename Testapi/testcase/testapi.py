import unittest
from Testapi.Commom.log import Log
from Testapi.config.config import FILES
from xlutils.copy import copy
import xlrd
from Testapi.config.config import REPORT_SAVE
from Testapi.config.config import TABLE
from Testapi.Commom.Request import Reques


class TestAPI(unittest.TestCase, Reques):

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

    def test_01(self):
        self.Request()

    def test_02(self):
        self.Request()

    def test_03(self):
        self.Request()

    def test_04(self):
        self.Request()

    def test_05(self):
        self.Request()

    def test_06(self):
        self.Request()

    def test_07(self):
        self.Request()

    def test_08(self):
        self.Request()

    def test_09(self):
        self.Request()

    def test_10(self):
        self.Request()

    def test_11(self):
        self.Request()

    def test_12(self):
        self.Request()

    def test_13(self):
        self.Request()

    def test_14(self):
        self.Request()

    def test_15(self):
        self.Request()

    def test_16(self):
        self.Request()

    def test_17(self):
        self.Request()

    def test_18(self):
        self.Request()

    def test_19(self):
        self.Request()

    def test_20(self):
        self.Request()

    def test_21(self):
        self.Request()

    def test_22(self):
        self.Request()

    def test_23(self):
        self.Request()

    def test_24(self):
        self.Request()

    def test_25(self):
        self.Request()

    def test_26(self):
        self.Request()

    def test_27(self):
        self.Request()

    def test_28(self):
        self.Request()

    def test_29(self):
        self.Request()

    def test_30(self):
        self.Request()

    def test_31(self):
        self.Request()

    def test_32(self):
        self.Request()

    def test_33(self):
        self.Request()

    def test_34(self):
        self.Request()

    def test_35(self):
        self.Request()

    def test_36(self):
        self.Request()

    def test_37(self):
        self.Request()

    def test_38(self):
        self.Request()

    def test_39(self):
        self.Request()

    def test_40(self):
        self.Request()

    def test_41(self):
        self.Request()

    def test_42(self):
        self.Request()

    def test_43(self):
        self.Request()

    def test_44(self):
        self.Request()

    def test_45(self):
        self.Request()

    def test_46(self):
        self.Request()

    def test_47(self):
        self.Request()

    def test_48(self):
        self.Request()

    def test_49(self):
        self.Request()

    def test_50(self):
        self.Request()

    def test_51(self):
        self.Request()

    def test_52(self):
        self.Request()

    def test_53(self):
        self.Request()

    def test_54(self):
        self.Request()

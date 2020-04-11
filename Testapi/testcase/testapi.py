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
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_02(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_03(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_04(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_05(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_06(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_07(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_08(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_09(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_10(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_11(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_12(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_13(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_14(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_15(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_16(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_17(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_18(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_19(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_20(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_21(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_22(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_23(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_24(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_25(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_26(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_27(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_28(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_29(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_30(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_31(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_32(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_33(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_34(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_35(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_36(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_37(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_38(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_39(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_40(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_41(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_42(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_43(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_44(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_45(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_46(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_47(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_48(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_49(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_50(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_51(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_52(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_53(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

    def test_54(self):
        NONE = self.Request()
        self.assertIsNotNone(NONE)

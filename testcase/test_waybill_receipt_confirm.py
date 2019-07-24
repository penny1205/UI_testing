# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_waybill_receipt import PageWaybillReceipt
from util.common.myunit import MyTest
from util.file.fileutil import FileUtil


class TestWaybillReceiptConfirm(MyTest):
    '''回单确认'''

    def setUp(self):
        MyTest.setUp(self)

    def test_waybill_receipt_confirm(self):
        '''回单确认'''
        PageWaybillReceipt(self.driver).login()
        waybillId,tmsBillCode = PageWaybillReceipt(self.driver).get_arrived_waybill(driverConfirm='1')[:2]
        receipt0 = FileUtil.getProjectObsPath() + '/image/receipt.jpg'
        PageWaybillReceipt(self.driver).receipt_confirm(tmsBillCode=tmsBillCode,waybillId=waybillId,receipt0=receipt0)
        self.assertEqual(PageWaybillReceipt(self.driver).receipt_confirm_waybill_success(), '回单确认成功')
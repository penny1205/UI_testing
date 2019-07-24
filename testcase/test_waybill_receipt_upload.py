# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_waybill_receipt import PageWaybillReceipt
from util.common.myunit import MyTest


class TestWaybillReceiptUpload(MyTest):
    '''回单上传'''

    def setUp(self):
        MyTest.setUp(self)

    def test_waybill_receipt_upload(self):
        '''回单上传'''
        PageWaybillReceipt(self.driver).login()
        tmsBillCode = PageWaybillReceipt(self.driver).get_arrived_waybill(driverConfirm='1')[1]
        PageWaybillReceipt(self.driver).receipt_upload(tmsBillCode=tmsBillCode,abnormal='1',remark='丢失一件')
        self.assertEqual(PageWaybillReceipt(self.driver).receipt_upload_waybill_success(), '提交成功')

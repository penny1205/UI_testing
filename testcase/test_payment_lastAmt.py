# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_payment_lastAmt import PagePaymentLastAmt
from util.common.myunit import MyTest


class TesPaymentLastAmt(MyTest):
    '''尾款支付'''

    def setUp(self):
        MyTest.setUp(self)

    def test_payment_lastAmt_singlePay_KEKING_TO_DRIVER(self):
        '''尾款支付 单条支付 白条付司机'''
        PagePaymentLastAmt(self.driver).login()
        tmsBillCode = PagePaymentLastAmt(self.driver).get_payment_lastAmt_waybill()[1]
        PagePaymentLastAmt(self.driver).singlePay_KEKING_TO_DRIVER(tmsBillCode=tmsBillCode)
        self.assertEqual(PagePaymentLastAmt(self.driver).payment_waybill_success(), '成功')

    def test_payment_lastAmt_singlePay_OFFLINE(self):
        '''尾款支付 单条支付 线下支付'''
        PagePaymentLastAmt(self.driver).login()
        tmsBillCode = PagePaymentLastAmt(self.driver).get_payment_lastAmt_waybill()[1]
        PagePaymentLastAmt(self.driver).singlePay_OFFLINE(tmsBillCode=tmsBillCode)
        self.assertEqual(PagePaymentLastAmt(self.driver).payment_waybill_success(), '线下支付成功')

    def test_payment_lastAmt_singlePay_WALLET_TO_DRIVER(self):
        '''尾款支付 单条支付 余额付司机'''
        PagePaymentLastAmt(self.driver).login()
        tmsBillCode = PagePaymentLastAmt(self.driver).get_payment_lastAmt_waybill()[1]
        PagePaymentLastAmt(self.driver).singlePay_WALLET_TO_DRIVER(tmsBillCode=tmsBillCode)
        self.assertEqual(PagePaymentLastAmt(self.driver).payment_waybill_success(), '支付成功')

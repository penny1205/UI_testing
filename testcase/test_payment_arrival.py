# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_payment_arrival import PagePaymentArrival
from util.common.myunit import MyTest


class TesPaymentArrival(MyTest):
    '''到达支付'''

    def setUp(self):
        MyTest.setUp(self)

    def test_payment_arrival_singlePay_KEKING_TO_DRIVER(self):
        '''到达支付 单条支付 白条付司机'''
        PagePaymentArrival(self.driver).login()
        tmsBillCode = PagePaymentArrival(self.driver).get_payment_arrival_waybill()[1]
        PagePaymentArrival(self.driver).singlePay_KEKING_TO_DRIVER(tmsBillCode=tmsBillCode)
        self.assertEqual(PagePaymentArrival(self.driver).payment_waybill_success(), '成功')

    def test_payment_arrival_singlePay_OFFLINE(self):
        '''到达支付 单条支付 线下支付'''
        PagePaymentArrival(self.driver).login()
        tmsBillCode = PagePaymentArrival(self.driver).get_payment_arrival_waybill()[1]
        PagePaymentArrival(self.driver).singlePay_OFFLINE(tmsBillCode=tmsBillCode)
        self.assertEqual(PagePaymentArrival(self.driver).payment_waybill_success(), '线下支付成功')

    def test_payment_arrival_singlePay_WALLET_TO_DRIVER(self):
        '''到达支付 单条支付 余额付司机'''
        PagePaymentArrival(self.driver).login()
        tmsBillCode = PagePaymentArrival(self.driver).get_payment_arrival_waybill()[1]
        PagePaymentArrival(self.driver).singlePay_WALLET_TO_DRIVER(tmsBillCode=tmsBillCode)
        self.assertEqual(PagePaymentArrival(self.driver).payment_waybill_success(), '支付成功')

# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_payment_departure import PagePaymentDeparture
from util.common.myunit import MyTest


class TesPaymentDeparture(MyTest):
    '''发车支付'''

    def setUp(self):
        MyTest.setUp(self)

    def test_payment_departure_singlePay_KEKING_TO_COMPANY(self):
        '''发车支付 单条支付 贷款付商户'''
        PagePaymentDeparture(self.driver).login()
        tmsBillCode = PagePaymentDeparture(self.driver).get_payment_departure_waybill()[1]
        PagePaymentDeparture(self.driver).singlePay_KEKING_TO_COMPANY(tmsBillCode=tmsBillCode)
        self.assertEqual(PagePaymentDeparture(self.driver).payment_waybill_success(), '成功')

    def test_payment_departure_singlePay_KEKING_TO_DRIVER(self):
        '''发车支付 单条支付 白条付司机'''
        PagePaymentDeparture(self.driver).login()
        tmsBillCode = PagePaymentDeparture(self.driver).get_payment_departure_waybill()[1]
        PagePaymentDeparture(self.driver).singlePay_KEKING_TO_DRIVER(tmsBillCode=tmsBillCode)
        self.assertEqual(PagePaymentDeparture(self.driver).payment_waybill_success(), '成功')

    def test_payment_departure_singlePay_OFFLINE(self):
        '''发车支付 单条支付 线下支付'''
        PagePaymentDeparture(self.driver).login()
        tmsBillCode = PagePaymentDeparture(self.driver).get_payment_departure_waybill()[1]
        PagePaymentDeparture(self.driver).singlePay_OFFLINE(tmsBillCode=tmsBillCode)
        self.assertEqual(PagePaymentDeparture(self.driver).payment_waybill_success(), '线下支付成功')

    def test_payment_departure_singlePay_WALLET_TO_DRIVER(self):
        '''发车支付 单条支付 余额付司机'''
        PagePaymentDeparture(self.driver).login()
        tmsBillCode = PagePaymentDeparture(self.driver).get_payment_departure_waybill()[1]
        PagePaymentDeparture(self.driver).singlePay_WALLET_TO_DRIVER(tmsBillCode=tmsBillCode)
        self.assertEqual(PagePaymentDeparture(self.driver).payment_waybill_success(), '支付成功')

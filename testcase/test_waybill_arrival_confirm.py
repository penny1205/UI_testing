# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_waybill_arrival import PageWaybillArrival
from util.common.myunit import MyTest


class TestWaybillArrivalConfirm(MyTest):
    '''到达确认'''

    def setUp(self):
        MyTest.setUp(self)

    def test_waybill_arrival_confirm(self):
        '''到达确认 司机发车确认'''
        PageWaybillArrival(self.driver).login()
        tmsBillCode = PageWaybillArrival(self.driver).get_arrived_waybill()[1]
        PageWaybillArrival(self.driver).arrival_confirm(tmsBillCode=tmsBillCode)
        self.assertEqual(PageWaybillArrival(self.driver).arrival_confirm_success(), '到达确认成功')

    def test_waybill_arrival_confirm2(self):
        '''到达确认 货主发车确认'''
        PageWaybillArrival(self.driver).login()
        tmsBillCode = PageWaybillArrival(self.driver).get_arrived_waybill2()[1]
        PageWaybillArrival(self.driver).arrival_confirm2(tmsBillCode=tmsBillCode)
        self.assertEqual(PageWaybillArrival(self.driver).arrival_confirm_success(), '到达确认成功')

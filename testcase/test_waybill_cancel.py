# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_waybill_departure import PageWaybillDeparture
from util.common.myunit import MyTest


class TestWaybillCancel(MyTest):
    '''取消运单'''

    def setUp(self):
        MyTest.setUp(self)

    def test_waybill_cancel(self):
        '''取消运单'''
        PageWaybillDeparture(self.driver).login()
        waybillId, tmsBillCode = PageWaybillDeparture(self.driver).get_wait_departure_waybill()
        PageWaybillDeparture(self.driver).cancel_waybill(tmsBillCode=tmsBillCode)
        self.assertEqual(PageWaybillDeparture(self.driver).cancel_waybill_success(), '成功')


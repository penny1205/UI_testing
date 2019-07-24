# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_waybill_departure import PageWaybillDeparture
from util.common.myunit import MyTest


class TestWaybillDepartureConfirm(MyTest):
    '''发车确认'''

    def setUp(self):
        MyTest.setUp(self)


    def test_waybill_departure_confirm(self):
        '''发车确认'''
        PageWaybillDeparture(self.driver).login()
        tmsBillCode = PageWaybillDeparture(self.driver).get_wait_departure_waybill()[1]
        PageWaybillDeparture(self.driver).departure_confirm(tmsBillCode=tmsBillCode)
        self.assertEqual(PageWaybillDeparture(self.driver).departure_confirm_success(), '成功')


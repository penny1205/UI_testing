# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_order_select import PageOrderSelect
from util.common.myunit import MyTest

class TestOrderCancel(MyTest):
    '''取消订单'''

    def setUp(self):
        MyTest.setUp(self)

    def test_order_cancel(self):
        '''取消订单'''
        PageOrderSelect(self.driver).login()
        planNo = PageOrderSelect(self.driver).get_noSend_order()
        PageOrderSelect(self.driver).cancel_order(planNo=planNo)
        self.assertIn(PageOrderSelect(self.driver).cancel_order_success(),'成功')
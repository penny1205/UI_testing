# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_order_select import PageOrderSelect
from util.common.myunit import MyTest

class TestOrderSend(MyTest):
    '''订单派车'''

    def setUp(self):
        MyTest.setUp(self)

    def test_order_copy(self):
        '''订单派车'''
        PageOrderSelect(self.driver).login()
        planNo = PageOrderSelect(self.driver).get_noSend_order()
        PageOrderSelect(self.driver).send_order(planNo=planNo)
        self.assertIn(PageOrderSelect(self.driver).send_order_success(),'创建成功')
# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_order_select import PageOrderSelect
from util.common.myunit import MyTest

class TestOrderCopy(MyTest):
    '''复制订单'''

    def setUp(self):
        MyTest.setUp(self)

    def test_order_copy(self):
        '''复制订单'''
        PageOrderSelect(self.driver).login()
        planNo = PageOrderSelect(self.driver).get_send_order()
        PageOrderSelect(self.driver).copy_order(planNo=planNo)
        self.assertIn(PageOrderSelect(self.driver).copy_order_success(),'成功')
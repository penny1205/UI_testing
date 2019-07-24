# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_order_create import PageOrderCreate
from util.common.myunit import MyTest

class TestOrderCreate(MyTest):
    '''创建订单'''

    def setUp(self):
        MyTest.setUp(self)

    def test_order_create(self):
        '''创建订单'''
        PageOrderCreate(self.driver).login()
        PageOrderCreate(self.driver).open_order_manage()
        PageOrderCreate(self.driver).input_order(orderRemark='订单备注',upOrderPlanNo='orderPlanNo123456')
        PageOrderCreate(self.driver).submit()
        self.assertIn(PageOrderCreate(self.driver).create_order_success(),'成功')
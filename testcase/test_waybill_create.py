# __author__ = ‘pan‘
# -*-coding:utf-8-*-


from src.page.page_waybill_create import PageWaybillCreate
from util.common.myunit import MyTest


class TestWaybillCreate(MyTest):
    '''创建运单'''

    def setUp(self):
        MyTest.setUp(self)

    def test_fee_car_waybill_create(self):
        '''创建外请车运单'''
        PageWaybillCreate(self.driver).login()
        PageWaybillCreate(self.driver).open_waybill_manage()
        PageWaybillCreate(self.driver).input_fee_car_waybill(driver='刘新宇',index='1',totalAmt='100',income='100',preAmt='0.01',
                                                             photoAirWay='',content='运单备注')
        PageWaybillCreate(self.driver).submit()
        self.assertIn(PageWaybillCreate(self.driver).create_waybill_success(),
                      ('创建成功','此手机号已有未确认的订单,不可重复提交，请发车确认后再录单'))

    def test_own_car_waybill_create(self):
        '''创建自有车运单'''
        PageWaybillCreate(self.driver).login()
        PageWaybillCreate(self.driver).open_waybill_manage()
        PageWaybillCreate(self.driver).input_own_car_waybill(index='1',totalAmt='100',income='100',preAmt='0.01',
                                                             photoAirWay='',content='运单备注')
        PageWaybillCreate(self.driver).submit()
        self.assertIn(PageWaybillCreate(self.driver).create_waybill_success(),
                      ('创建成功', '此手机号已有未确认的订单,不可重复提交，请发车确认后再录单'))

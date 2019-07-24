# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.page.page_waybill_select import PageWaybillSelect
from util.common.myunit import MyTest


class TestWaybillDelete(MyTest):
    '''删除运单'''

    def setUp(self):
        MyTest.setUp(self)

    def test_waybill_delete(self):
        '''删除运单'''
        PageWaybillSelect(self.driver).login()
        tmsBillCode = PageWaybillSelect(self.driver).get_waybill()[1]
        PageWaybillSelect(self.driver).delete_waybill(tmsBillCode=tmsBillCode)
        self.assertEqual(PageWaybillSelect(self.driver).delete_waybill_success(), '删除成功')

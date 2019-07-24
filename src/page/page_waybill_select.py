# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from selenium.webdriver.support.select import Select
from src.helper.hepler_waybill import HeplerWaybill
from src.helper.is_have_waybill import ISHaveWaybill
from src.page.page import Page
from src.page.page_waybill_create import PageWaybillCreate


class PageWaybillSelect(Page):
    '''运单查询页面'''

    def get_waybill(self,driver=''):
        '''获取运单查询页面可删除的运单号'''
        try:
            waybillId,tmsBillCode = ISHaveWaybill().is_have_waybill(driver=driver)[:2]
            # 打开运单管理模块
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/label/a')

            if waybillId == None:
                waybillId,tmsBillCode = PageWaybillCreate(self.driver).create_waybill_submit(driver=driver)
                # 打开运单查询页面
                HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/div/ul/li[1]/a/span')
                # 输入查询内容查询运单
                Select(self.driver.get_element('id->TMS-dateInterval')).select_by_index(1)
                HeplerWaybill().fuzzy_query(self.driver,'id->normalCondition','id->TMS-waybillIndex-normalSearch-',tmsBillCode)
                return waybillId,tmsBillCode
            else:
                # 打开运单查询页面
                HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/div/ul/li[1]/a/span')
                # 输入查询内容查询运单
                Select(self.driver.get_element('id->TMS-dateInterval')).select_by_index(1)
                HeplerWaybill().fuzzy_query(self.driver, 'id->normalCondition', 'TMS-normalSearch-', tmsBillCode)
                cName = self.driver.driver.find_element_by_id('TMS-showDialog-').get_attribute("class")
                if  cName == 'btn btn-danger':
                    return waybillId, tmsBillCode
                else:
                    waybillId, tmsBillCode = PageWaybillCreate(self.driver).create_waybill_submit(driver=driver)
                    # 打开运单查询页面
                    HeplerWaybill().open_menu(self.driver,
                                              'xpath->//*[@id="menu"]/div/nav/ul/li[4]/div/ul/li[1]/a/span')
                    return waybillId, tmsBillCode
        except Exception as e:
            self.logger.error('获取运单查询页面可删除的运单号发生异常:{0}'.format(e))
            return None

    def delete_waybill(self,tmsBillCode=''):
        '''删除运单'''
        try:
            self.logger.info("删除运单的运单编号是:{0}".format(tmsBillCode))
            # 找到需要删除的运单删除
            self.driver.retry_find_click('id->TMS-showDialog-')
            self.driver.element_is_visible('class->xcConfirm')
            self.driver.retry_find_click('xpath->//*[@class="xcConfirm"]/div[2]/div[3]/div/a[1]')
        except Exception as e:
            self.logger.error('删除运单发生异常:{0}'.format(e))
            return None


    def Modify_button(self):
        '''修改按钮'''
        self.driver.click('xpath->//*[@id="waybillIndexDiv"]/div[2]/div[2]/table/tbody/tr[1]/td[27]/div[2]/a')

    def delete_waybill_success(self):
        '''删除运单成功'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        return self.driver.get_text('xpath->//*[@id="myModal"]/div/div/div[2]')
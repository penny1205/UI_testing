# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from selenium.webdriver.support.select import Select
from src.helper.hepler_waybill import HeplerWaybill
from src.helper.is_have_waybill import ISHaveWaybill
from src.page.page import Page
from src.page.page_waybill_create import PageWaybillCreate

class PageWaybillDetail(Page):
    '''运单详情页面'''

    def get_waybill(self, driver=''):
        '''获取运单详情页面的运单号'''
        try:
            waybillId, tmsBillCode = ISHaveWaybill().is_have_waybill(driver=driver)[:2]
            # 打开运单管理模块
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/label/a')

            if waybillId == None:
                waybillId, tmsBillCode = PageWaybillCreate(self.driver).create_waybill_submit(driver=driver)
                return waybillId, tmsBillCode
            else:
                return waybillId, tmsBillCode
        except Exception as e:
            self.logger.error('获取运单号的运单详情发生异常:{0}'.format(e))
            return None

    def waybill_detail(self,tmsBillCode=''):
        '''运单详情'''
        try:
            self.logger.info("获取运单号:{0}的运单详情".format(tmsBillCode))
            # 打开运单查询页面
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/div/ul/li[1]/a/span')
            # 输入查询内容查询运单
            Select(self.driver.get_element('id->TMS-dateInterval')).select_by_index(1)
            HeplerWaybill().fuzzy_query(self.driver, 'id->normalCondition', 'id->TMS-normalSearch-', tmsBillCode)
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 点击运单编号获取运单详情
            self.driver.move_to_click('id->TMS-toDetail-')
            self.driver.element_is_not_visible('class->loading-bar-background')
        except Exception as e:
            self.logger.error('获取运单号{1}的运单详情发生异常:{0}'.format(e,tmsBillCode))
            return None

    def get_amt(self,tmsBillCode):
        '''获取到付金额\尾款金额'''
        try:
            self.waybill_detail(tmsBillCode)
            destAmt = self.driver.get_text('id->TMS-bill-transportCash.destAmt')
            lastAmt = self.driver.get_text('id->TMS-bill-transportCash.retAmt')
            return destAmt,lastAmt
        except Exception as e:
            self.logger.error('获取运单的到付金额、尾款金额发生异常:{0}'.format(e))
        finally:
            # 点击返回按钮
            self.driver.retry_find_click('xpath->//*[@id="detailDiv"]/div[2]/div/button[2]')
            self.driver.element_is_not_visible('class->loading-bar-background')
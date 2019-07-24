# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from selenium.webdriver.support.select import Select
from src.helper.hepler_waybill import HeplerWaybill
from src.helper.is_have_waybill import ISHaveWaybill
from src.helper.driver_confirm_api import DriverConfirmApi
from src.page.page import Page
from src.page.page_waybill_departure import PageWaybillDeparture


class PagePaymentSelect(Page):
    '''支付查询页面'''

    def get_payment_select_waybill(self, driver='', driverConfirm='1'):
        '''获取支付查询页面的运单号'''
        try:
            self.login()
            payment_select_waybillId, payment_select_tmsBillCode = ISHaveWaybill().is_have_payment_arrival_waybill(
                driver=driver, driverConfirm=driverConfirm)[:2]
            if payment_select_waybillId != None:
                waybillId, tmsBillCode = str(payment_select_waybillId[0]), str(payment_select_tmsBillCode[0])
                return waybillId, tmsBillCode
            else:
                waybillId, tmsBillCode = PageWaybillDeparture(self.driver).get_wait_departure_waybill(driver=driver)
                if driverConfirm == '1':
                    # 司机发车确认
                    DriverConfirmApi().driver_confirm_api(billId=waybillId, totalAmt='1000', preAmt='0.01', oilAmt='0.01',
                                                      destAmt='0.01', lastAmt='0.01', receiverId='')
                elif driverConfirm == '0':
                    PageWaybillDeparture(self.driver).departure_confirm(tmsBillCode=tmsBillCode)
                else:
                    self.logger.error('是否司机发车确认输入参数错误:{0}'.format(driverConfirm))
                return waybillId, tmsBillCode
        except Exception as e:
            self.logger.error('获取支付查询页面的运单号:{0}'.format(e))
            return None

    def payment_detail(self,tmsBillCode=''):
        '''支付详情'''
        try:
            # 打开支付查询页面
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[5]/label',
                                      'xpath->//*[@id="menu"]/div/nav/ul/li[5]/div/ul/li[1]')
            # 输入查询内容查询运单
            Select(self.driver.get_element('xpath->TMS-dateInterval')).select_by_index(0)
            HeplerWaybill().date_query(self.driver,index=all)
            HeplerWaybill().fuzzy_query(self.driver,'id->normalCondition','xpath->TMS-payList-globalSearch-',tmsBillCode)
            # 点击详情按钮，打开支付详情页面
            self.driver.retry_find_click('xpath->//*[@id="page-wrapper"]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[34]/div/a')
            self.driver.element_is_not_visible('class->loading-bar-background')
        except Exception as e:
            self.logger.error('打开支付详情页面发生异常:{0}'.format(e))
            return None

    def payment_schedule(self,content):
        '''返回支付进度'''
        self.payment_detail(content)
        return self.driver.text('xpath->//*[@id="mainTable"]/tbody/tr[1]/td[5]')
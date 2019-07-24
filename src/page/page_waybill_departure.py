# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.helper.hepler_waybill import HeplerWaybill
from src.helper.is_have_waybill import ISHaveWaybill
from src.page.page import Page
from src.page.page_waybill_create import PageWaybillCreate

class PageWaybillDeparture(Page):
    '''发车确认页面'''

    def get_wait_departure_waybill(self,driver=''):
        '''获取待发车确认的运单号'''
        try:
            wait_departure_waybillId,wait_departure_tmsBillCode = ISHaveWaybill().is_have_wait_departure_waybill(driver=driver)[:2]
            # 打开运单管理模块
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/label/a')

            if wait_departure_waybillId == None:
                waybillId,tmsBillCode = PageWaybillCreate(self.driver).create_waybill_submit(driver=driver)
                return waybillId,tmsBillCode
            else:
                waybillId = str(wait_departure_waybillId[0])
                tmsBillCode = str(wait_departure_tmsBillCode[0])
                return waybillId,tmsBillCode
        except Exception as e:
            self.logger.error('获取待发车确认的运单号发生异常:{0}'.format(e))
            return None

    def departure_confirm(self,tmsBillCode=''):
        '''发车确认'''
        try:
            self.logger.info('发车确认的运单号:{0}'.format(tmsBillCode))
            # 打开发车确认页面
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/div/ul/li[3]/a/span')
            # 输入查询内容查询运单
            HeplerWaybill().fuzzy_query(self.driver, 'id->normalCondition', 'id->normalConditionButton', tmsBillCode)
            # 点击发车确认
            self.driver.retry_find_click('id->TMS-sendCarConfirm-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            self.driver.retry_find_click('xpath->//*[@id="sendCarTips"]/div/div/div[3]/button[1]')
            return tmsBillCode
        except Exception as e:
            self.logger.error('发车确认发生异常:{0}'.format(e))
            return None

    def cancel_waybill(self,tmsBillCode=''):
        '''取消运单'''
        try:
            self.logger.info('取消运单的运单运单号:{0}'.format(tmsBillCode))
            # 跳转至发车确认页面
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/div/ul/li[3]/a/span')
            # 输入查询内容查询运单
            HeplerWaybill().fuzzy_query(self.driver, 'id->normalCondition', 'id->normalConditionButton', tmsBillCode)
            # 点击取消运单
            self.driver.retry_find_click('id->TMS-confirmShow-')
            self.driver.element_is_visible('class->xcConfirm')
            self.driver.retry_find_click('xpath->//*[@class="xcConfirm"]/div[2]/div[3]/div/a[1]')
            return tmsBillCode
        except Exception as e:
            self.logger.error('取消运单发生异常:{0}'.format(e))
            return None


    def departure_confirm_success(self):
        '''发车确认成功'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        return self.driver.get_text('xpath->//*[@id="myModal"]/div/div/div[2]')

    def cancel_waybill_success(self):
        '''取消运单成功'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        return self.driver.get_text('xpath->//*[@id="myModal"]/div/div/div[2]')

    def Modify_button(self):
        '''修改按钮'''
        self.driver.click('xpath->//*[@id="waybillTable"]/tbody/tr[1]/td[30]/div/a[1]')
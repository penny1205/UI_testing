# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from src.helper.driver_confirm_api import DriverConfirmApi
from src.helper.hepler_waybill import HeplerWaybill
from src.helper.is_have_waybill import ISHaveWaybill
from src.page.page import Page
from src.page.page_waybill_create import PageWaybillCreate
from src.page.page_waybill_departure import PageWaybillDeparture
from src.page.page_waybill_detail import PageWaybillDetail


class PageWaybillArrival(Page):
    '''到达确认页面'''

    def get_arrived_waybill(self,driver='',driverConfirm= '1'):
        '''获取到达确认页面司机发车确认的运单号'''
        try:
            in_transit_waybillId,in_transit_tmsBillCode = ISHaveWaybill().is_have_in_transit_waybill(driver=driver,driverConfirm=driverConfirm)[:2]
            wait_departure_waybillId, wait_departure_tmsBillCode = ISHaveWaybill().is_have_wait_departure_waybill(driver=driver)[:2]
            # 打开运单管理模块
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/label/a')

            if in_transit_waybillId != None:
                waybillId, tmsBillCode = str(in_transit_waybillId[0]), str(in_transit_tmsBillCode[0])
                return waybillId, tmsBillCode
            elif wait_departure_waybillId != None:
                waybillId, tmsBillCode = str(wait_departure_waybillId[0]), str(wait_departure_tmsBillCode[0])
                # 司机发车确认
                DriverConfirmApi().driver_confirm_api(billId=waybillId, totalAmt='1000', preAmt='0.01', oilAmt='0.01',
                                                      destAmt='0.01', lastAmt='0.01', receiverId='')
                return waybillId, tmsBillCode
            else:
                waybillId, tmsBillCode = PageWaybillCreate(self.driver).create_waybill_submit(driver=driver)
                # 司机发车确认
                DriverConfirmApi().driver_confirm_api(billId=waybillId, totalAmt='1000', preAmt='0.01', oilAmt='0.01',
                                                      destAmt='0.01', lastAmt='0.01', receiverId='')
                return waybillId, tmsBillCode
        except Exception as e:
            self.logger.error('获取到达确认页面司机发车确认的运单号:{0}'.format(e))
            return None


    def get_arrived_waybill2(self,driver='',driverConfirm='0'):
        '''获取到达确认页面货主发车确认的运单号'''
        try:
            in_transit_waybillId, in_transit_tmsBillCode = ISHaveWaybill().is_have_in_transit_waybill(driver=driver,driverConfirm=driverConfirm)[:2]
            wait_departure_waybillId, wait_departure_tmsBillCode = ISHaveWaybill().is_have_wait_departure_waybill(driver=driver)[:2]
            # 打开运单管理模块
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/label/a')

            if in_transit_waybillId != None:
                waybillId, tmsBillCode = str(in_transit_waybillId[0]), str(in_transit_tmsBillCode[0])
                return waybillId, tmsBillCode
            elif wait_departure_waybillId != None:
                waybillId, tmsBillCode = str(wait_departure_waybillId[0]), str(wait_departure_tmsBillCode[0])
                # 货主发车确认
                tmsBillCode = PageWaybillDeparture(self.driver).departure_confirm(tmsBillCode=tmsBillCode)
                return waybillId, tmsBillCode
            else:
                waybillId, tmsBillCode = PageWaybillCreate(self.driver).create_waybill_submit(driver=driver)
                # 货主发车确认
                tmsBillCode = PageWaybillDeparture(self.driver).departure_confirm(tmsBillCode=tmsBillCode)
                return waybillId, tmsBillCode
        except Exception as e:
            self.logger.error('获取到达确认页面司机发车确认的运单号:{0}'.format(e))
            return None


    def arrival_confirm(self,tmsBillCode=''):
        '''到达确认 司机发车确认'''
        try:
            self.logger.info('到达确认页面,选择到达确认的运单号:{0}'.format(tmsBillCode))
            # 获取到付金额
            destAmt = PageWaybillDetail(self.driver).get_amt(tmsBillCode)[0]
            # 打开到达确认页面
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/div/ul/li[5]/a/span')
            # 输入查询内容查询运单
            HeplerWaybill().fuzzy_query(self.driver, 'id->confirmNormalCondition', 'id->confirmNormalConditionButton', tmsBillCode)
            # 点击目的地到达按钮
            self.driver.move_to_click('id->TMS-judgeSendCar-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 确认到达
            if destAmt == '':
                self.driver.move_to_click('id->TMS-submitConfirmWay-')
            else:
                # 修改到达确认金额
                self.driver.clear_type('id->TMS-bill-actualPay','0.02')
                self.driver.type('id->TMS-bill-memo','修改到达金额')
                self.driver.move_to_click('id->TMS-submitConfirmWay-')
            self.driver.element_is_not_visible('class->loading-bar-background')
        except Exception as e:
            self.logger.error('到达确认 司机发车确认发生异常:{0}'.format(e))
            return None

    def arrival_confirm2(self,tmsBillCode=''):
        '''到达确认 货主发车确认'''
        try:
            self.logger.info('到达确认页面,选择到达确认的运单号:{0}'.format( tmsBillCode))
            # 获取到付金额
            destAmt = PageWaybillDetail(self.driver).get_amt(tmsBillCode)[0]
            # 打开到达确认页面
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/div/ul/li[5]/a/span')
            #输入查询内容查询运单
            HeplerWaybill().fuzzy_query(self.driver,  'id->confirmNormalCondition', 'id->confirmNormalConditionButton', tmsBillCode)
            #点击到达确认按钮
            self.driver.move_to_click('id->TMS-judgeSendCar-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            #到达确认
            self.driver.move_to_click('id->TMS-openDetail-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            if destAmt == '':
                self.driver.move_to_click('id->TMS-submitConfirmWay-')
            else:
                # 修改到达确认金额
                self.driver.clear_type('id->TMS-bill-actualPay','0.02')
                self.driver.type('id->TMS-bill-memo','修改到达金额')
                self.driver.move_to_click('id->TMS-submitConfirmWay-')
            self.driver.element_is_not_visible('class->loading-bar-background')
        except Exception as e:
            self.logger.error('到达确认 货主发车确认发生异常:{0}'.format(e))
            return None
    #
    # def batch_arrival_confirm(self,tmsBillCode= ''):
    #     '''批量到达'''
    #     try:
    #         self.logger.info('批量到达的运单号:{0}'.format(tmsBillCode))
    #         #输入查询内容查询运单
    #         self.driver.click('//*[@id="confirmBill"]/div[1]/form[1]/div/div[2]/button[1]')
    #         HeplerWaybill().select_query(tmsBillCode, 'xpath->//*[@id="confirmBill"]/div[1]/form[2]/div/div/div[3]/div/select', index='2')
    #         #点击到达确认按钮
    #         self.driver.retry_find_click('xpath->//*[@id="confirmWayTable"]/tbody/tr[1]/td[29]/div/a')
    #         self.driver.element_is_not_visible('class->loading-bar-background')
    #         #修改到达确认金额
    #         self.driver.click('xpath->//*[@id="sendCarTips"]/div/div/div[3]/button[1]')
    #     except Exception as e:
    #         self.logger.error('到达确认 货主发车确认发生异常:{0}'.format(e))
    #         return None


    def arrival_confirm_success(self):
        '''到达确认成功'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        return self.driver.get_text('xpath->//*[@id="myModal"]/div/div/div[2]')

    def waybill_arrival_confirm(self):
        '''到达确认成功 确定按钮'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        self.driver.retry_find_click('xpath->//*[@id="myModal"]/div/div/div[3]/button')
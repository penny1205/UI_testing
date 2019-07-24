# __author__ = ‘pan‘
# -*-coding:utf-8-*-

import time
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil
from src.helper.hepler_waybill import HeplerWaybill
from src.helper.is_have_waybill import ISHaveWaybill
from src.helper.driver_confirm_api import DriverConfirmApi
from src.page.page import Page
from src.page.page_waybill_departure import PageWaybillDeparture


class PagePaymentDeparture(Page):
    '''发车支付页面'''

    def get_payment_departure_waybill(self, driver='', driverConfirm='1'):
        '''获取发车支付页面的运单号'''
        try:
            payment_departure_waybillId, payment_departure_tmsBillCode = ISHaveWaybill().is_have_payment_departure_waybill(
                driver=driver, driverConfirm=driverConfirm)[:2]

            if payment_departure_waybillId != None:
                waybillId, tmsBillCode = str(payment_departure_waybillId[0]), str(payment_departure_tmsBillCode[0])
                return waybillId, tmsBillCode
            else:
                waybillId, tmsBillCode = PageWaybillDeparture(self.driver).get_wait_departure_waybill(driver=driver)
                PageWaybillDeparture(self.driver).departure_confirm(tmsBillCode=tmsBillCode)
                if driverConfirm == '1':
                    # 司机发车确认
                    DriverConfirmApi().driver_confirm_api(billId=waybillId, totalAmt='1000', preAmt='0.01', oilAmt='0.01',
                                                      destAmt='0.01', lastAmt='0.01', receiverId='')
                return waybillId, tmsBillCode
        except Exception as e:
            self.logger.error('获取发车支付页面的运单号:{0}'.format(e))
            return None, None
        finally:
            # 打开运费支付模块
            HeplerWaybill().open_menu(self.driver,'xpath->//*[@id="menu"]/div/nav/ul/li[5]/label/a')

    def payment_KEKING_TO_comment(self,tmsBillCode='',payMethod=''):
        '''发车支付页面 选择除余额支付以外支付方式支付'''
        try:
            # 打开发车支付页面
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[5]/div/ul/li[2]/a/span')
            # 输入运单号查询运单
            HeplerWaybill().fuzzy_query(self.driver, 'id->globalCondition', 'id->globalConditionButton', tmsBillCode)
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 选择运单
            self.driver.click('id->TMS-selectCheckbox-')
            # 点击支付按钮，打开支付弹窗
            self.driver.click('id->TMS-toWayBillPay-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 选择除余额支付以外支付方式
            self.driver.click('{0}'.format(payMethod))
            # 确认支付
            self.driver.click('id->TMS-toPursePay-')
            self.driver.element_is_not_visible('class->loading-bar-background')
        except Exception as e:
            self.logger.error('发车支付页面 选择除余额支付以外支付方式支付:{0}'.format(e))
            return None

    def singlePay_KEKING_TO_COMPANY(self,tmsBillCode=''):
        '''发车支付页面 单条运单选择贷款付商户支付'''
        try:
            self.payment_KEKING_TO_comment(tmsBillCode=tmsBillCode,payMethod='xpath->//*[@id="wayBillPay"]/div/div/div[2]/div/form/div[2]/div[2]/table/tbody/tr[2]/td[2]/span/label')
        except Exception as e:
            self.logger.error('发车支付页面 选择贷款付商户支付发生异常:{0}'.format(e))
            return None

    def singlePay_KEKING_TO_DRIVER(self,tmsBillCode=''):
        '''发车支付页面 单条运单选择白条付司机支付'''
        try:
            self.payment_KEKING_TO_comment(tmsBillCode=tmsBillCode,payMethod='xpath->//*[@id="wayBillPay"]/div/div/div[2]/div/form/div[2]/div[2]/table/tbody/tr[2]/td[3]/span/label')
        except Exception as e:
            self.logger.error('发车支付页面 单条运单选择白条付司机支付发生异常:{0}'.format(e))
            return None

    def singlePay_OFFLINE(self,tmsBillCode=''):
        '''发车支付页面 单条运单选择线下支付支付'''
        try:
            self.payment_KEKING_TO_comment(tmsBillCode=tmsBillCode,payMethod='xpath->//*[@id="wayBillPay"]/div/div/div[2]/div/form/div[2]/div[2]/table/tbody/tr[2]/td[5]/span/label')
        except Exception as e:
            self.logger.error('发车支付页面 单条运单选择白条付司机支付发生异常:{0}'.format(e))
            return None

    def singlePay_WALLET_TO_DRIVER(self,tmsBillCode=''):
        '''发车支付页面 选择除余额支付方式支付'''
        try:
            # 打开发车支付页面
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[5]/div/ul/li[2]/a/span')
            # 输入运单号查询运单
            HeplerWaybill().fuzzy_query(self.driver, 'id->globalCondition', 'id->globalConditionButton', tmsBillCode)
            # 选择运单
            self.driver.click('id->TMS-selectCheckbox-')
            # 点击支付按钮，打开支付弹窗
            self.driver.click('id->TMS-toWayBillPay-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 选择余额支付
            self.driver.click('xpath->//*[@id="wayBillPay"]/div/div/div[2]/div/form/div[2]/div[2]/table/tbody/tr[2]/td[4]/span/label')
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 确认支付
            self.driver.click('id->TMS-toPursePay-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 输入支付密码并确认支付
            self.config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
            self.driver.type('id->sendcreate',self.config['payPassword'])
            self.driver.click('id->TMS-lianLianPay-')
            self.driver.element_is_not_visible('class->loading-bar-background')
        except Exception as e:
            self.logger.error('发车支付页面 选择除余额支付方式支付:{0}'.format(e))
            return None

    def create_waybill_confirm(self):
        '''支付记录 确认按钮 '''
        self.driver.click('xpath->//*[@id="promptInfo"]/div/div/div[3]/button')
        self.driver.element_is_not_visible('class->loading-bar-background')

    def payment_waybill_success(self):
        '''支付成功'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        return self.driver.get_text('xpath->//*[@id="promptInfo"]/div/div/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[7]')
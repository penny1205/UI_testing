# __author__ = ‘pan‘
# -*-coding:utf-8-*-
import time
from selenium.webdriver.support.select import Select
from src.helper.hepler_waybill import HeplerWaybill
from src.helper.is_have_waybill import ISHaveWaybill
from src.helper.query_waybill import QueryWaybill
from src.helper.driver_upload_receipt_api import DriverUploadReceiptApi
from src.page.page import Page
from src.page.page_waybill_create import PageWaybillCreate
from src.page.page_waybill_departure import PageWaybillDeparture
from src.page.page_waybill_arrival import PageWaybillArrival

class PageWaybillReceipt(Page):
    '''回单录入页面'''

    def get_arrived_waybill(self,driver='',driverConfirm=''):
        '''获取回单录入页面的运单号'''
        try:
            in_transit_waybillId, in_transit_tmsBillCode = ISHaveWaybill().is_have_in_transit_waybill(driver=driver,driverConfirm=driverConfirm)[:2]
            wait_departure_waybillId, wait_departure_tmsBillCode = ISHaveWaybill().is_have_wait_departure_waybill(driver=driver)[:2]
            # 打开运单管理模块
            HeplerWaybill().open_menu(self.driver,'xpath->//*[@id="menu"]/div/nav/ul/li[4]/label/a')

            if in_transit_waybillId != None:
                waybillId, tmsBillCode = str(in_transit_waybillId[0]), str(in_transit_tmsBillCode[0])
                if driverConfirm == '1':
                    PageWaybillArrival(self.driver).arrival_confirm(tmsBillCode=tmsBillCode)
                    self.driver.move_to_click('xpath->//*[@id="myModal"]/div/div/div[3]/button')
                    self.driver.element_is_not_visible('class->loading-bar-background')
                    self.logger.info('司机发车确认的运单 到达确认:{0}'.format(tmsBillCode))
                elif driverConfirm == '0':
                    PageWaybillArrival(self.driver).arrival_confirm2(tmsBillCode=tmsBillCode)
                    self.driver.move_to_click('xpath->//*[@id="myModal"]/div/div/div[3]/button')
                    self.driver.element_is_not_visible('class->loading-bar-background')
                    self.logger.info('货主发车确认的运单 到达确认:{0}'.format(tmsBillCode))
                else:
                    self.logger.error('请确认运单是否发车确认:{0}'.format(tmsBillCode))
                return waybillId, tmsBillCode
            elif wait_departure_waybillId != None:
                waybillId, tmsBillCode = str(wait_departure_waybillId[0]), str(wait_departure_tmsBillCode[0])
                PageWaybillDeparture(self.driver).departure_confirm(tmsBillCode=tmsBillCode)
                PageWaybillArrival(self.driver).arrival_confirm2(tmsBillCode=tmsBillCode)
                self.driver.move_to_click('xpath->//*[@id="myModal"]/div/div/div[3]/button')
                self.driver.element_is_not_visible('class->loading-bar-background')
                self.logger.info('待发车的运单 货主发车确认 到达确认:{0}'.format(tmsBillCode))
                return waybillId, tmsBillCode
            else:
                waybillId, tmsBillCode = PageWaybillCreate(self.driver).create_waybill_submit(driver=driver)
                PageWaybillDeparture(self.driver).departure_confirm(tmsBillCode=tmsBillCode)
                PageWaybillArrival(self.driver).arrival_confirm2(tmsBillCode=tmsBillCode)
                self.driver.move_to_click('xpath->//*[@id="myModal"]/div/div/div[3]/button')
                self.driver.element_is_not_visible('class->loading-bar-background')
                self.logger.info('新建运单 货主发车确认 到达确认:{0}'.format(tmsBillCode))
                return waybillId, tmsBillCode
        except Exception as e:
            self.logger.error('获取回单录入页面的运单号:{0}'.format(e))
            return None,None

    def receipt_upload(self,tmsBillCode='',abnormal='0',remark='',actualAmt='',amtRemark='',receiptRemark=''):
        '''上传回单'''
        try:
            self.logger.info('回单录入页面,选择上传回单的运单号:{0}'.format(tmsBillCode))
            # 判断运单是否已到达
            trans_status = QueryWaybill().query_waybill_status(tmsBillCode)
            if trans_status != 'A':
                self.logger.info('选择上传的运单号:{0}运单状态不是已到达'.format(tmsBillCode))
            # 打开回单录入页面
            HeplerWaybill().open_menu(self.driver,'xpath->//*[@id="menu"]/div/nav/ul/li[4]/div/ul/li[6]/a/span')
            # 输入查询内容查询运单
            HeplerWaybill().fuzzy_query(self.driver, 'id->normalCondition', 'id->normalConditionButton',tmsBillCode)
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 点击回单上传按钮
            self.driver.move_to_click('id->TMS-showConfirm-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 打开回单上传页面
            # 选择没有异常
            if abnormal == '0':
                Select(self.driver.get_element('id->TMS-bill-abnormal')).select_by_index(1)
            # 选择有异常
            elif abnormal == '1':
                time.sleep(5)
                Select(self.driver.get_element('id->TMS-bill-abnormal')).select_by_index(0)
                self.driver.move_to_click('id->lostedforHW')
                self.driver.type('id->TMS-bill-damagedMemo', remark)
            else:
                self.logger.error('请确认上传回单输入的参数abnormal是否正确:{0}'.format(abnormal))
            self.driver.type('id->billShowActulAmt', actualAmt)
            self.driver.type('id->TMS-bill-memo',amtRemark)
            ###不上传回单照片
            self.driver.type('id->TMS-bill-receptRemarks',receiptRemark)
            self.driver.move_to_click('id->upLoadImgSubMit')
            self.driver.element_is_not_visible('class->loading-bar-background')
            self.driver.move_to_click('xpath->//*[@id="myModal"]/div/div/div[3]/button')
            self.driver.element_is_not_visible('class->loading-bar-background')
        except Exception as e:
            self.logger.error('上传回单发生异常:{0}'.format(e))
            return None

    def receipt_confirm(self,tmsBillCode='',waybillId='',receipt0='',actualAmt='',amtRemark='',receiptRemark=''):
        '''回单确认'''
        try:
            self.logger.info('回单录入页面,选择回单确认的运单号:{0}'.format(tmsBillCode))
            # 判断运单是否已到达
            trans_status = QueryWaybill().query_waybill_status(tmsBillCode)
            if trans_status == 'A':
                DriverUploadReceiptApi().driver_upload_receipt_api(waybillId=waybillId, receipt0=receipt0)
            else:
                self.logger.info('选择回单确认的运单号:{0}运单状态不是已到达'.format(tmsBillCode))
            # 打开回单录入页面
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/div/ul/li[6]/a/span')
            # 输入查询内容查询运单
            HeplerWaybill().fuzzy_query(self.driver, 'id->normalCondition', 'id->normalConditionButton', tmsBillCode)
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 点击回单确认按钮
            self.driver.move_to_click('id->TMS-getReceiptMsg-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 打开回单确认页面
            self.driver.type('id->actualAmtConfirm', actualAmt)
            self.driver.type('id->TMS-recept-memo', amtRemark)
            ###不上传回单照片
            self.driver.type('id->TMS-recept-receptRemarks',receiptRemark)
            self.driver.move_to_click('id->TMS-confirmReceip-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            self.driver.move_to_click('xpath->//*[@id="myModal"]/div/div/div[3]/button')
            self.driver.element_is_not_visible('class->loading-bar-background')
        except Exception as e:
            self.logger.error('回单确认发生异常:{0}'.format(e))
            return None

    def batch_check(self,billNos=''):
        '''批量核对'''
        try:
            # 打开批量核对窗口
            self.driver.click('id->TMS-showBatchCheckDialog-')
            # 输入核对的单号
            self.driver.type('id->billNos',billNos)
            # 点击确认按钮
            self.driver.move_to_click('id->TMS-batchCheckBillNos-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 核对成功，核对失败
        except Exception as e:
            self.logger.error('批量核对发生异常:{0}'.format(e))
            return None

    def receipt_confirm_waybill_success(self):
        '''回单确认成功'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        return self.driver.get_text('xpath->//*[@id="myModal"]/div/div/div[2]')

    def receipt_upload_waybill_success(self):
        '''回单上传成功'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        return self.driver.get_text('xpath->//*[@id="myModal"]/div/div/div[2]')
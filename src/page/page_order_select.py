# __author__ = ‘pan‘
# -*-coding:utf-8-*-

import time
from util.db.dbutil import DBUtil
from src.helper.hepler_waybill import HeplerWaybill
from src.helper.is_have_order import ISHaveOrder
from src.page.page import Page
from src.page.page_order_create import PageOrderCreate
from src.page.page_waybill_create import PageWaybillCreate

class PageOrderSelect(Page):
    '''订单查询页面'''

    def get_select_order(self):
        '''获取订单查询页面的订单号'''
        try:
            planNo = ISHaveOrder().is_have_order(orderStatus='all')
            # 打开订单管理模块
            HeplerWaybill().open_menu(self.driver,'xpath->//*[@id="menu"]/div/nav/ul/li[3]/label/a')

            if planNo != None:
                return planNo
            else:
                planNo = PageOrderCreate(self.driver).create_order_submit()
                return planNo
        except Exception as e:
            self.logger.error('获取订单查询页面的订单号发生异常:{0}'.format(e))
            return None

    def get_noSend_order(self):
        '''获取未派车的订单号'''
        try:
            planNo = ISHaveOrder().is_have_order(orderStatus='0')
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[3]/label/a')

            if planNo != None:
                return planNo
            else:
                planNo = PageOrderCreate(self.driver).create_order_submit()
                return planNo
        except Exception as e:
            self.logger.error('获取未派车的订单号发生异常:{0}'.format(e))
            return None

    def get_sending_order(self):
        '''获取派车中的订单号'''
        try:
            planNo_sending = ISHaveOrder().is_have_order(orderStatus='1')
            planNo_noSend = ISHaveOrder().is_have_order(orderStatus='0')
            # 打开订单管理模块
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[3]/label/a')

            if planNo_sending != None:
                return planNo_sending
            elif planNo_noSend != None:
                self.send_order(planNo=planNo_noSend)
                return planNo_noSend
            else:
                planNo = PageOrderCreate(self.driver).create_order_submit()
                self.send_order(planNo=planNo)
                return planNo
        except Exception as e:
            self.logger.error('获取未派车的订单号发生异常:{0}'.format(e))
            return None

    def get_send_order(self):
        '''获取已派车的订单号'''
        try:
            planNo_send = ISHaveOrder().is_have_order(orderStatus='2')
            planNo_sending = ISHaveOrder().is_have_order(orderStatus='1')
            planNo_noSend = ISHaveOrder().is_have_order(orderStatus='0')
            # 打开订单管理模块
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[3]/label/a')

            if planNo_send != None:
                return planNo_send
            elif planNo_sending != None:
                self.send_order(planNo=planNo_sending)
                return planNo_noSend
            elif planNo_noSend != None:
                self.send_order(planNo=planNo_noSend)
                return planNo_noSend
            else:
                planNo = PageOrderCreate(self.driver).create_order_submit()
                self.send_order(planNo=planNo)
                return planNo
        except Exception as e:
            self.logger.error('获取已派车的订单号发生异常:{0}'.format(e))
            return None


    def cancel_order(self,planNo=''):
        '''取消订单'''
        try:
            self.logger.info('取消订单的运单号:{0}'.format(planNo))
            # 打开订单查询页面
            HeplerWaybill().open_menu(self.driver,'xpath->//*[@id="menu"]/div/nav/ul/li[3]/div/ul/li[1]/a/span')
            # 输入订单号查询订单
            HeplerWaybill().input_query(self.driver, 'id->TMS-param-planNo',
                                        planNo,'xpath->//*[@id="TMS-search-"]/span')
            # 点击取消按钮
            self.driver.retry_find_click('id->TMS-confirmShowByTitle-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            self.driver.retry_find_click('xpath->//*[@class="xcConfirm"]/div[2]/div[3]/div/a[1]')
            return planNo
        except Exception as e:
            self.logger.error('取消订单发生异常:{0}'.format(e))
            return None

    def copy_order(self,planNo='',project=''):
        '''复制订单'''
        try:
            self.logger.info('复制订单的运单号:{0}'.format(planNo))
            # 打开订单查询页面
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[3]/div/ul/li[1]/a/span')
            # 输入订单号查询订单
            HeplerWaybill().input_query(self.driver, 'id->TMS-param-planNo',
                                        planNo, 'xpath->//*[@id="TMS-search-"]/span')
            # 点击复制按钮
            self.driver.move_to_click('id->TMS-copyPlanInfoToCreatePage-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 重新选择项目
            self.driver.move_to_click('id->projectId')
            self.driver.element_is_not_visible('class->loading-bar-background')
            self.driver.type('id->TMS-queryProjects-selectProject', project)
            self.driver.move_to_click('id->TMS-selectProject-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            time.sleep(5)
            # 创建订单页面点击提交按钮
            current_window = self.driver.driver.current_window_handle
            self.driver.move_to_click('id->TMS-saveOrderPlan-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            all_windows = self.driver.driver.window_handles
            for window in all_windows:
                if window != current_window:
                    self.driver.driver.switch_to.window(window)
            self.driver.retry_find_click('xpath->//*[@id="myModal"]/div/div/div[3]/button', secs=10)
            return planNo
        except Exception as e:
            self.logger.error('复制订单发生异常:{0}'.format(e))
            return None

    def send_order(self,planNo=''):
        '''订单派车'''
        try:
            self.logger.info('订单派车的运单号:{0}'.format(planNo))
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[3]/div/ul/li[1]/a/span')
            # 输入订单号查询订单
            HeplerWaybill().input_query(self.driver, 'id->TMS-param-planNo',
                                        planNo, 'xpath->//*[@id="TMS-search-"]/span')
            # 点击派车按钮
            self.driver.retry_find_click('id->TMS-listCargo-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            self.driver.retry_find_click('id->TMS-dispatchedAndUpdateCargo-')
            self.driver.element_is_not_visible('class->loading-bar-background')
            # 打开运单管理模块
            HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/label/a')
            # 生成运单
            waybillId, tmsBillCode = PageWaybillCreate(self.driver).jump_waybill_submit(driver='18056070532',index='1',
                                totalAmt='100',income='100',preAmt='0.01',photoAirWay='',content='运单备注')
            return  planNo, waybillId, tmsBillCode
        except Exception as e:
            self.logger.error('订单派车发生异常:{0}'.format(e))
            return None,None,None


    def cancel_order_success(self):
        '''取消订单成功'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        return self.driver.get_text('xpath->//*[@id="myModal"]/div/div/div[2]')

    def copy_order_success(self):
        '''复制订单成功'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        return self.driver.get_text('xpath->//*[@id="myModal"]/div/div/div[2]')

    def send_order_success(self):
        '''订单派车成功'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        return self.driver.get_text('xpath->//*[@id="myModal"]/div/div/div[2]')
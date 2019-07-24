# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from util.db.dbutil import DBUtil
from src.helper.hepler_waybill import HeplerWaybill
from src.page.page import Page

class PageOrderCreate(Page):
    '''新建订单页面'''

    def open_order_manage(self):
        # 打开订单管理模块
        HeplerWaybill().open_menu(self.driver,'xpath->//*[@id="menu"]/div/nav/ul/li[3]/label/a')

    def input_cargo(self,cargoName='',cargoWeight='',cargoVolume='',cargoCount='',unit='',cargoNo='',cargoWorth='',
                    insuranceCosts=''):
        # 输入货物明细
        HeplerWaybill().set_value_cargo(self.driver, cargoName, cargoWeight, cargoVolume, cargoCount, unit, cargoNo,
                                        cargoWorth, insuranceCosts)

    def input_order(self,project='',orderRemark='',upOrderPlanNo=''):
        # 打开新建订单页面
        HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[3]/div/ul/li[2]/a/span')
        # 选择项目
        self.driver.retry_find_click('id->projectId')
        self.driver.element_is_not_visible('class->loading-bar-background')
        self.driver.type('id->TMS-queryProjects-selectProject',project)
        self.driver.move_to_click('id->TMS-selectProject-')

        self.driver.type('id->planRemark',orderRemark)
        self.driver.type('id->TMS-billModel-upOrderPlanNo',upOrderPlanNo)

    def submit(self):
        '''提交按钮'''
        self.driver.click('id->TMS-saveOrderPlan-')

    def cancel(self):
        '''取消按钮'''
        self.driver.click('id->TMS-clearParams-')

    def create_order_confirm(self):
        '''创建订单成功 确定按钮'''
        current_window = self.driver.driver.current_window_handle
        self.driver.click('id->TMS-saveOrderPlan-', secs=10)
        self.driver.element_is_not_visible('class->loading-bar-background')
        all_windows = self.driver.driver.window_handles
        for window in all_windows:
            if window != current_window:
                self.driver.driver.switch_to.window(window)
        self.driver.retry_find_click('xpath->//*[@id="myModal"]/div/div/div[3]/button',secs = 10)

    def create_order_success(self):
        '''创建订单成功'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        return self.driver.get_text('xpath->//*[@id="myModal"]/div/div/div[2]')


    def create_order_submit(self,project='',orderRemark='',upOrderPlanNo=''):
        '''创建订单'''
        self.input_order(project=project,orderRemark=orderRemark,upOrderPlanNo=upOrderPlanNo)
        self.create_order_confirm()
        # 获取创建运单的订单号
        self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                             user=self.config['db_user'], passwd=self.config['db_passwd'],
                             dbname=self.config['db_dbname'], charset=self.config['db_charset'])
        sql = 'SELECT planNo FROM YD_TMS_ORDERPLAN WHERE orderStatus = \'0\' and partnerNo = \'{0}\''.format(self.config['partnerNo'])
        planNo = self.DBUtil.excute_select_one_record(sql)
        return planNo
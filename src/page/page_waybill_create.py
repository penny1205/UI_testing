# __author__ = ‘pan‘
# -*-coding:utf-8-*-

import re,time
from util.db.dbutil import DBUtil
from src.helper.departure_confirm_api import DepartureConfirmApi
from src.page.page import Page
from src.helper.hepler_waybill import HeplerWaybill
from src.helper.is_have_waybill import ISHaveWaybill

class PageWaybillCreate(Page):
    '''我要录单页面'''

    def open_waybill_manage(self):
        # 打开运单管理模块
        HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/label/a')

    def input_default_field(self,project,index,totalAmt,income,preAmt,oilAmt,destAmt,lastAmt,photoAirWay,content):
        '''输入默认字段'''

        #输入用车日期
        self.driver.retry_find_click("id->applyDate")
        self.driver.retry_find_click("xpath->//*[@id='waybillAddForm']/div[1]/div[2]/div/div[2]/div/div/div/div/div/ul/li[2]/span/button[1]")

        #选择项目
        HeplerWaybill().set_value_select_input(self.driver,"id->projectId",project)
        #输入始发地
        HeplerWaybill().set_value_address(self.driver,"id->sendProvince",
                                          "xpath->//*[@id='_citys0']/a[1]",
                                          "xpath->//*[@id='_citys1']/a",
                                          "xpath->//*[@id='_citys2']/a[1]")
        #输入到达地
        HeplerWaybill().set_value_address(self.driver, "id->arriveProvince",
                                          "xpath->//*[@id='_citys0']/a[2]",
                                          "xpath->//*[@id='_citys1']/a",
                                          "xpath->//*[@id='_citys2']/a[1]")

        #输入途径地1
        self.driver.click('xpath->//*[@id="TMS-addStation-"]/span')
        HeplerWaybill().set_value_address(self.driver, "id->showStationA",
                                          "xpath->//*[@id='_citys0']/a[3]",
                                          "xpath->//*[@id='_citys1']/a[1]",
                                          "xpath->//*[@id='_citys2']/a[1]")
        #输入途径地2
        self.driver.click('xpath->//*[@id="TMS-addStation-"]/span')
        HeplerWaybill().set_value_address(self.driver, "id->showStationB",
                                          "xpath->//*[@id='_citys0']/a[3]",
                                          "xpath->//*[@id='_citys1']/a[2]",
                                          "xpath->//*[@id='_citys2']/a[1]")

        # 输入总运费
        self.driver.type('id->totalAmt',totalAmt)
        # 输入发车收入
        self.driver.type('id->incomeId', income)
        # 输入预付
        self.driver.type('id->TMS-billModel-preAmt', preAmt)
        # 输入油卡
        self.driver.type('id->TMS-billModel-oilAmt', oilAmt)
        # 输入到付
        self.driver.type('id->TMS-billModel-destAmt', destAmt)
        # 输入尾款'''
        self.driver.type('id->TMS-billModel-lastAmt', lastAmt)
        # 输入运输协议照片
        self.driver.type('xpath->//*[@id="picOfTransport"]/div/div/div',photoAirWay)
        # 输入运单备注
        self.driver.type('id->TMS-billModel-content',content)


    def input_system_defined_field(self,order='',oilCardNo='',handlingFee='',deliveryFee='',oilCardDeposit='',otherFee='',):
        '''输入预设字段'''
        #订单号
        self.driver.type("id->upWayBillId", order)
        #油卡卡号
        self.driver.type('id->oilCardNo',oilCardNo)
        #装卸费
        self.driver.type('id->TMS-billModel-handlingFee',handlingFee)
        #送货费
        self.driver.type('id->TMS-billModel-deliveryFee',deliveryFee)
        #油卡押金
        self.driver.type('id->TMS-billModel-oilCardDeposit',oilCardDeposit)
        #其他费用
        self.driver.type('id->TMS-billModel-otherFee', otherFee)


    def input_user_defined_field(self):
        '''输入自定义字段'''
        return None

    def input_cargo(self,cargoName='',cargoWeight='',cargoVolume='',cargoCount='',unit='',cargoNo='',cargoWorth='',
                    insuranceCosts=''):
        # 输入货物明细
        HeplerWaybill().set_value_cargo(self.driver, cargoName, cargoWeight, cargoVolume, cargoCount, unit, cargoNo,
                                        cargoWorth, insuranceCosts)


    def input_own_car_waybill(self,project='',driver='',carNo='',index='0',totalAmt='',income='',preAmt='',oilAmt='',
                              destAmt='',lastAmt='',photoAirWay='',content=''):
        '''选择自有车录单'''
        # 打开我要录单页面
        HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/div/ul/li[2]/a/span')
        #选择公司车
        self.driver.click("xpath->//*[@id='carOne']/i")
        #输入默认字段
        self.input_default_field(project, index, totalAmt, income, preAmt, oilAmt, destAmt, lastAmt,photoAirWay, content)
        #选择司机
        HeplerWaybill().set_value_select_input(self.driver,"id->realName",driver)
        #选择车辆
        HeplerWaybill().set_value_select_input(self.driver,"id->innerCarNoId",carNo)
        # 输入有无回单
        self.driver.select('id->TMS-billModel-hasReceipt',"index->{0}".format(index))


    def input_fee_car_waybill(self,project='',driver='',supplier='',index='0',totalAmt='',income='',preAmt='',oilAmt='',
                              destAmt='',lastAmt='',photoAirWay='',content=''):
        '''选择外请车录单'''
        # 打开我要录单页面
        HeplerWaybill().open_menu(self.driver, 'xpath->//*[@id="menu"]/div/nav/ul/li[4]/div/ul/li[2]/a/span')

        self.input_default_field(project,index,totalAmt,income,preAmt,oilAmt,destAmt,lastAmt,photoAirWay,content)
        #选择司机、车辆
        HeplerWaybill().set_value_select_input(self.driver, "id->realName",driver)
        # 选择供应商
        HeplerWaybill().set_value_select_input(self.driver,'id->TMS-billModel-supplierName',supplier)
        # 输入有无回单
        self.driver.select('id->TMS-billModel-hasReceipt',"index->{0}".format(index))


    def update_car(self,carNo,carLength,carModel):
        '''修改车辆信息'''
        self.driver.type("id->innerCarNoId",carNo)
        self.driver.type("id->selectCarLengthId", carLength)
        self.driver.type("id->selectCarModelId", carModel)

    def submit(self):
        '''提交按钮'''
        self.driver.click('id->onlySubmit')

    def continue_submit(self):
        '''继续提交按钮'''
        self.driver.click('id->SubmitAndContinue')

    def empty_content(self):
        '''清空内容'''
        self.driver.click('id->TMS-清空内容')

    def cancel(self):
        '''取消按钮'''
        self.driver.click('xpath->//*[@id="addWayBillDiv"]/div/form/div[5]/div/button[3]')

    def create_waybill_confirm(self):
        '''创建运单成功 确定按钮'''
        current_window = self.driver.driver.current_window_handle
        self.driver.click('id->onlySubmit', secs=10)
        self.driver.element_is_not_visible('class->loading-bar-background')
        time.sleep(5)
        all_windows = self.driver.driver.window_handles
        for window in all_windows:
            if window != current_window:
                self.driver.driver.switch_to.window(window)
        self.driver.retry_find_click('xpath->//*[@id="myModal"]/div/div/div[3]/button',secs = 10)

    def create_waybill_success(self):
        '''创建运单成功'''
        self.driver.element_is_not_visible('class->loading-bar-background')
        return self.driver.get_text('xpath->//*[@id="myModal"]/div/div/div[2]')



    def create_waybill_submit(self,project='',driver='',supplier='',index='1',totalAmt='1000',income='2000',preAmt='0.01',
                              oilAmt='0.01',destAmt='0.01',lastAmt='0.01',photoAirWay='',content=''):
        '''创建运单'''
        waybillId, tmsBillCode ,driver_mobile= ISHaveWaybill().is_have_wait_departure_waybill(driver=driver)
        # 判断是否存在未发车的运单
        if waybillId != None:
            self.logger.info("已认证外请车存在未发车确认的运单ID:{0}".format(waybillId))
            DepartureConfirmApi().departure_confirm_api(str(waybillId[0]))

        # 创建运单
        self.input_fee_car_waybill(project, driver_mobile, supplier, index, totalAmt, income, preAmt, oilAmt, destAmt,
                                   lastAmt, photoAirWay, content)
        self.create_waybill_confirm()

        # 获取创建运单运单号、运单ID
        self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                             user=self.config['db_user'], passwd=self.config['db_passwd'],
                             dbname=self.config['db_dbname'], charset=self.config['db_charset'])
        sql = 'SELECT airWayBillNo ,tmsBillCode FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and billStatus = \'W\' ' \
              'and delStatus = \'0\' and partnerNo = \'{1}\''.format(driver_mobile, self.config['partnerNo'])
        waybillId,tmsBillCode = self.DBUtil.excute_select_one_record(sql)
        return waybillId,tmsBillCode

    def jump_waybill_submit(self,project='',driver='',supplier='',index='1',totalAmt='1000',income='2000',preAmt='0.01',
                              oilAmt='0.01',destAmt='0.01',lastAmt='0.01',photoAirWay='',content=''):
        '''创建运单'''
        waybillId, tmsBillCode ,driver_mobile= ISHaveWaybill().is_have_wait_departure_waybill(driver=driver)
        # 判断是否存在未发车的运单
        if waybillId != None:
            self.logger.info("存在未发车确认的运单ID:{0}".format(waybillId))
            DepartureConfirmApi().departure_confirm_api(str(waybillId[0]))

        self.input_default_field(project, index, totalAmt, income, preAmt, oilAmt, destAmt, lastAmt, photoAirWay,
                                 content)
        # 选择司机、车辆
        HeplerWaybill().set_value_select_input(self.driver, "id->realName", driver)
        # 选择供应商
        HeplerWaybill().set_value_select_input(self.driver, 'id->TMS-billModel-supplierName', supplier)
        # 输入有无回单
        self.driver.select('id->TMS-billModel-hasReceipt', "index->{0}".format(index))
        self.submit()

        # 获取创建运单运单号、运单ID
        self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                             user=self.config['db_user'], passwd=self.config['db_passwd'],
                             dbname=self.config['db_dbname'], charset=self.config['db_charset'])
        sql1 = 'SELECT airWayBillNo ,tmsBillCode FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and billStatus = \'W\' ' \
               'and delStatus = \'0\' and partnerNo = \'{1}\''.format(driver_mobile, self.config['partnerNo'])
        waybillId,tmsBillCode = self.DBUtil.excute_select_one_record(sql1)
        return waybillId, tmsBillCode

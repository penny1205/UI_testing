# __author__ = ‘pan‘
# -*-coding:utf-8-*-

import re
from util.db.dbutil import DBUtil
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil
from util.log.log import Log
from src.helper.driver_select_api import DriverSelectApi

class ISHaveWaybill(object):
    '''查询是否存在运单'''
    def __init__(self):
        self.config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
        self.logger = Log()

    def select_driver_mobile(self,driver):
        '''
        选择司机
        @driver: 货运司机
        '''
        try:
            mobile = re.compile(
                '^1(30|31|32|33|34|35|36|37|38|39|45|47|50|51|52|53|55|56|57|58|59|66|70|71|73|75|76|77|78|80|81|82|83|84|85|86|87|88|89|98|99)[0-9]{8}$')
            if driver == mobile:
                driver_mobile = driver
            elif driver == '' or driver == '18056070532':
                driver_mobile = self.config['driver_mobile']
            else:
                driver_mobile = DriverSelectApi().driver_select_api(name=driver).json()['content']['dataList']['mobile']
            self.logger.info("选择司机的手机号:{0}".format(driver_mobile))
            return driver_mobile
        except Exception as e:
            self.logger.error('选择司机的手机号发生异常:{0}'.format(e))
            return None

    def is_have_waybill(self, driver, driverConfirm='' ):
        '''
        查询司机是否有运单
         driverConfirm  '0'司机未发车确认 '1'司机发车确认  ''不区分是否司机发车确认
        '''
        try:
            driver_mobile = self.select_driver_mobile(driver)
            self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                                 user=self.config['db_user'], passwd=self.config['db_passwd'],
                                 dbname=self.config['db_dbname'], charset=self.config['db_charset'])
            if driverConfirm == '0' or driverConfirm == '1' :
                sql = 'SELECT id FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and delStatus = \'0\' and ' \
                      'partnerNo = \'{1}\' and driverConfirm = \'{2}\' ORDER BY id desc'.format(
                    driver_mobile, self.config['partnerNo'], driverConfirm)
                waybillId = self.DBUtil.excute_select_one_record(sql)
                sql2 = 'SELECT tmsBillCode FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and delStatus = \'0\' and ' \
                       'partnerNo = \'{1}\'and driverConfirm = \'{2}\' ORDER BY id desc'.format(
                    driver_mobile, self.config['partnerNo'], driverConfirm)
                tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            else:
                sql = 'SELECT id FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and delStatus = \'0\' and ' \
                      'partnerNo = \'{1}\' ORDER BY id desc'.format(driver_mobile, self.config['partnerNo'])
                waybillId = self.DBUtil.excute_select_one_record(sql)
                sql2 = 'SELECT tmsBillCode FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and delStatus = \'0\' and ' \
                       'partnerNo = \'{1}\' ORDER BY id desc'.format(driver_mobile, self.config['partnerNo'])
                tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            self.logger.info('查询司机是否有运单query result, waybillId:{0},tmsBillCode:{1}'.format(waybillId, tmsBillCode))
            return waybillId,tmsBillCode,driver_mobile
        except Exception as e:
            self.logger.error('查询司机是否有运单发生异常:{0}'.format(e))
            return None

    def is_have_wait_departure_waybill(self, driver):
        '''查询司机是否有未发车的运单'''
        try:
            driver_mobile = self.select_driver_mobile(driver)
            self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                                 user=self.config['db_user'], passwd=self.config['db_passwd'],
                                 dbname=self.config['db_dbname'], charset=self.config['db_charset'])
            sql = 'SELECT id FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'D\' and ' \
                  'delStatus = \'0\' and partnerNo = \'{1}\''.format(driver_mobile, self.config['partnerNo'])
            waybillId = self.DBUtil.excute_select_one_record(sql)
            sql2 = 'SELECT tmsBillCode FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'D\' and ' \
                   'delStatus = \'0\' and partnerNo = \'{1}\''.format(driver_mobile, self.config['partnerNo'])
            tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            self.logger.info('查询司机是否有未发车的运单query result, waybillId:{0},tmsBillCode:{1}'.format(waybillId, tmsBillCode))
            return waybillId,tmsBillCode,driver_mobile
        except Exception as e:
            self.logger.error('查询司机是否有未发车的运单发生异常:{0}'.format(e))
            return None

    def is_have_in_transit_waybill(self, driver, driverConfirm='' ):
        '''司机是否有运输中的运单'''
        try:
            driver_mobile = self.select_driver_mobile(driver)
            self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                                 user=self.config['db_user'], passwd=self.config['db_passwd'],
                                 dbname=self.config['db_dbname'], charset=self.config['db_charset'])
            if driverConfirm == '0' or driverConfirm == '1':
                sql = 'SELECT id FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'E\' and ' \
                      'delStatus = \'0\' and partnerNo = \'{1}\'and driverConfirm = \'{2}\' ORDER BY id desc'.format(
                    driver_mobile, self.config['partnerNo'], driverConfirm)
                waybillId = self.DBUtil.excute_select_one_record(sql)
                sql2 = 'SELECT tmsBillCode FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'E\' and ' \
                       'delStatus = \'0\' and partnerNo = \'{1}\'and driverConfirm = \'{2}\' ORDER BY id desc'.format(
                    driver_mobile, self.config['partnerNo'], driverConfirm)
                tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            else:
                sql = 'SELECT id FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'E\' and ' \
                      'delStatus = \'0\' and partnerNo = \'{1}\' ORDER BY id desc'.format(driver_mobile, self.config['partnerNo'])
                waybillId = self.DBUtil.excute_select_one_record(sql)
                sql2 = 'SELECT tmsBillCode FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'E\' and ' \
                       'delStatus = \'0\' and partnerNo = \'{1}\' ORDER BY id desc'.format(driver_mobile, self.config['partnerNo'])
                tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            self.logger.info('查询司机是否有运输中运单query result, waybillId:{0},tmsBillCode:{1}'.format(waybillId, tmsBillCode))
            return waybillId,tmsBillCode,driver_mobile
        except Exception as e:
            self.logger.error('司机是否有运输中的运单发生异常:{0}'.format(e))
            return None

    def is_have_arrived_waybill(self, driver,  driverConfirm=''):
        '''司机是否有已到达的运单'''
        try:
            driver_mobile = self.select_driver_mobile(driver)
            self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                                 user=self.config['db_user'], passwd=self.config['db_passwd'],
                                 dbname=self.config['db_dbname'], charset=self.config['db_charset'])
            if driverConfirm == '0' or driverConfirm == '1':
                sql = 'SELECT id FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'A\' and ' \
                      'delStatus = \'0\' and partnerNo = \'{1}\'and driverConfirm = \'{2}\' ORDER BY id desc'.format(
                       driver_mobile, self.config['partnerNo'], driverConfirm)
                waybillId = self.DBUtil.excute_select_one_record(sql)
                sql2 = 'SELECT tmsBillCode FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'A\' and ' \
                       'delStatus = \'0\' and partnerNo = \'{1}\'and driverConfirm = \'{2}\' ORDER BY id desc'.format(
                        driver_mobile, self.config['partnerNo'], driverConfirm)
                tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            else:
                sql = 'SELECT id FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'A\' and ' \
                      'delStatus = \'0\' and partnerNo = \'{1}\' ORDER BY id desc'.format(driver_mobile, self.config['partnerNo'])
                waybillId = self.DBUtil.excute_select_one_record(sql)
                sql2 = 'SELECT tmsBillCode FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'A\' and ' \
                       'delStatus = \'0\' and partnerNo = \'{1}\' ORDER BY id desc'.format(driver_mobile, self.config['partnerNo'])
                tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            self.logger.info('查询司机是否有已到达的运单query result, waybillId:{0},tmsBillCode:{1}'.format(waybillId, tmsBillCode))
            return waybillId, tmsBillCode,driver_mobile
        except Exception as e:
            self.logger.error('司机是否有已到达的运单发生异常:{0}'.format(e))
            return None

    def is_have_completed_waybill(self, driver , driverConfirm=''):
        '''司机是否有已完成的运单'''
        try:
            driver_mobile = self.select_driver_mobile(driver)
            self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                                 user=self.config['db_user'], passwd=self.config['db_passwd'],
                                 dbname=self.config['db_dbname'], charset=self.config['db_charset'])
            if driverConfirm == '0' or driverConfirm == '1':
                sql = 'SELECT id FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'C\' and ' \
                      'delStatus = \'0\' and partnerNo = \'{1}\' and driverConfirm = \'{2}\' ORDER BY id desc'.format(
                       driver_mobile, self.config['partnerNo'], driverConfirm)
                waybillId = self.DBUtil.excute_select_one_record(sql)
                sql2 = 'SELECT tmsBillCode FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'C\' and ' \
                       'delStatus = \'0\' and partnerNo = \'{1}\' and driverConfirm = \'{2}\' ORDER BY id desc'.format(
                        driver_mobile, self.config['partnerNo'], driverConfirm)
                tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            else:
                sql = 'SELECT id FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'C\' and ' \
                      'delStatus = \'0\' and partnerNo = \'{1}\' ORDER BY id desc'.format(driver_mobile, self.config['partnerNo'])
                waybillId = self.DBUtil.excute_select_one_record(sql)
                sql2 = 'SELECT tmsBillCode FROM YD_APP_TRANSPORTCASH WHERE mobile = \'{0}\' and transStatus = \'C\' and ' \
                       'delStatus = \'0\' and partnerNo = \'{1}\' ORDER BY id desc'.format(driver_mobile, self.config['partnerNo'])
                tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            self.logger.info('查询司机是否有已完成的运单query result, waybillId:{0},tmsBillCode:{1}'.format(waybillId, tmsBillCode))
            return waybillId, tmsBillCode,driver_mobile
        except Exception as e:
            self.logger.error('司机是否有已完成的运单发生异常:{0}'.format(e))
            return None

    def is_have_payment_departure_waybill(self, driver, driverConfirm='1'):
        '''司机是否有可发车支付的运单'''
        try:
            driver_mobile = self.select_driver_mobile(driver)
            self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                                 user=self.config['db_user'], passwd=self.config['db_passwd'],
                                 dbname=self.config['db_dbname'], charset=self.config['db_charset'])
            sql = 'SELECT t.id FROM YD_APP_TRANSPORTCASH t ' \
                  'LEFT JOIN YD_TMS_PAY_DETAIL pd ON t.id = pd.wayBillId ' \
                  'WHERE (t.partnerNo =\'{0}\' AND t.mobile = \'{1}\' AND t.delStatus = 0 ' \
                  'AND t.billStatus != \'W\' AND t.billStatus != \'Q\' ' \
                  'AND (pd.cashPayStatus = \'UNPAID\' OR pd.cashPayStatus = \'FAIL\') ' \
                  'AND (((pd.cashLoanSchedule != \'FAIL\' OR pd.cashLoanSchedule IS NULL) ' \
                  'AND (pd.oilFeeLoanSchedule != \'FAIL\' OR pd.oilFeeLoanSchedule IS NULL) ' \
                  'AND (pd.destAmtLoanSchedule != \'FAIL\' OR pd.destAmtLoanSchedule IS NULL) ' \
                  'AND (pd.retAmtLoanSchedule != \'FAI\L\' OR pd.retAmtLoanSchedule IS NULL)' \
                  'AND t.driverConfirm = {2}))) ORDER BY t.id desc'.format(self.config['partnerNo'],driver_mobile,driverConfirm)
            waybillId = self.DBUtil.excute_select_one_record(sql)
            sql2 = 'SELECT t.tmsBillCode FROM YD_APP_TRANSPORTCASH t ' \
                  'LEFT JOIN YD_TMS_PAY_DETAIL pd ON t.id = pd.wayBillId ' \
                  'WHERE (t.partnerNo =\'{0}\' AND t.mobile = \'{1}\' AND t.delStatus = 0 ' \
                  'AND t.billStatus != \'W\' AND t.billStatus != \'Q\' ' \
                  'AND (pd.cashPayStatus = \'UNPAID\' OR pd.cashPayStatus = \'FAIL\') ' \
                  'AND (((pd.cashLoanSchedule != \'FAIL\' OR pd.cashLoanSchedule IS NULL) ' \
                  'AND (pd.oilFeeLoanSchedule != \'FAIL\' OR pd.oilFeeLoanSchedule IS NULL) ' \
                  'AND (pd.destAmtLoanSchedule != \'FAIL\' OR pd.destAmtLoanSchedule IS NULL) ' \
                  'AND (pd.retAmtLoanSchedule != \'FAI\L\' OR pd.retAmtLoanSchedule IS NULL)' \
                  'AND t.driverConfirm = {2}))) ORDER BY t.id desc'.format(self.config['partnerNo'], driver_mobile, driverConfirm)
            tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            self.logger.info('查询司机是否有可发车支付的运单query result, waybillId:{0},tmsBillCode:{1}'.format(waybillId, tmsBillCode))
            return waybillId, tmsBillCode,driver_mobile
        except Exception as e:
            self.logger.error('机是否有可发车支付的运单发生异常:{0}'.format(e))
            return None

    def is_have_payment_arrival_waybill(self, driver,driverConfirm='1'):
        '''司机是否有可到达支付的运单'''
        try:
            driver_mobile = self.select_driver_mobile(driver)
            self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                                 user=self.config['db_user'], passwd=self.config['db_passwd'],
                                 dbname=self.config['db_dbname'], charset=self.config['db_charset'])
            sql = 'SELECT t.id FROM YD_APP_TRANSPORTCASH t ' \
                  'LEFT JOIN YD_TMS_PAY_DETAIL pd ON t.id = pd.wayBillId ' \
                  'WHERE (t.partnerNo =\'{0}\' AND t.mobile = \'{1}\' AND t.delStatus = 0 ' \
                  'AND t.destAmtConfirm IS NOT NULL AND pd.cashPayStatus = \'SUCCESS\' ' \
                  'AND (pd.destAmtPayStatus = \'UNPAID\' OR pd.destAmtPayStatus = \'FAIL\') ' \
                  'AND (((pd.cashLoanSchedule != \'FAIL\' OR pd.cashLoanSchedule IS NULL) ' \
                  'AND (pd.oilFeeLoanSchedule != \'FAIL\' OR pd.oilFeeLoanSchedule IS NULL) ' \
                  'AND (pd.destAmtLoanSchedule != \'FAIL\' OR pd.destAmtLoanSchedule IS NULL) ' \
                  'AND (pd.retAmtLoanSchedule != \'FAI\L\' OR pd.retAmtLoanSchedule IS NULL)' \
                  'AND t.driverConfirm = {2}))) ORDER BY t.id desc'.format(self.config['partnerNo'], driver_mobile, driverConfirm)
            waybillId = self.DBUtil.excute_select_one_record(sql)
            sql2 = 'SELECT t.tmsBillCode FROM YD_APP_TRANSPORTCASH t ' \
                  'LEFT JOIN YD_TMS_PAY_DETAIL pd ON t.id = pd.wayBillId ' \
                  'WHERE (t.partnerNo =\'{0}\' AND t.mobile = \'{1}\' AND t.delStatus = 0 ' \
                  'AND t.destAmtConfirm IS NOT NULL AND pd.cashPayStatus = \'SUCCESS\' ' \
                  'AND (pd.destAmtPayStatus = \'UNPAID\' OR pd.destAmtPayStatus = \'FAIL\') ' \
                  'AND (((pd.cashLoanSchedule != \'FAIL\' OR pd.cashLoanSchedule IS NULL) ' \
                  'AND (pd.oilFeeLoanSchedule != \'FAIL\' OR pd.oilFeeLoanSchedule IS NULL) ' \
                  'AND (pd.destAmtLoanSchedule != \'FAIL\' OR pd.destAmtLoanSchedule IS NULL) ' \
                  'AND (pd.retAmtLoanSchedule != \'FAI\L\' OR pd.retAmtLoanSchedule IS NULL)' \
                  'AND t.driverConfirm = {2}))) ORDER BY t.id desc'.format(self.config['partnerNo'], driver_mobile, driverConfirm)
            tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            return waybillId, tmsBillCode,driver_mobile
        except Exception as e:
            self.logger.error('司机是否有已完成的运单发生异常:{0}'.format(e))
            return None


    def is_have_payment_lastAmt_waybill(self, driver,driverConfirm='1'):
        '''司机是否有可尾款支付的运单'''
        try:
            driver_mobile = self.select_driver_mobile(driver)
            self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                                 user=self.config['db_user'], passwd=self.config['db_passwd'],
                                 dbname=self.config['db_dbname'], charset=self.config['db_charset'])
            sql = 'SELECT t.id FROM YD_APP_TRANSPORTCASH t ' \
                  'LEFT JOIN YD_TMS_PAY_DETAIL pd ON t.id = pd.wayBillId ' \
                  'WHERE (t.partnerNo =\'{0}\' AND t.mobile = \'{1}\' AND t.delStatus = 0 ' \
                  'AND t.retAmtConfirm IS NOT NULL AND pd.retAmtPayStatus = \'SUCCESS\' ' \
                  'AND (pd.retAmtPayStatus = \'UNPAID\' OR pd.retAmtPayStatus = \'FAIL\') ' \
                  'AND (((pd.cashLoanSchedule != \'FAIL\' OR pd.cashLoanSchedule IS NULL) ' \
                  'AND (pd.oilFeeLoanSchedule != \'FAIL\' OR pd.oilFeeLoanSchedule IS NULL) ' \
                  'AND (pd.destAmtLoanSchedule != \'FAIL\' OR pd.destAmtLoanSchedule IS NULL) ' \
                  'AND (pd.retAmtLoanSchedule != \'FAI\L\' OR pd.retAmtLoanSchedule IS NULL)' \
                  'AND t.driverConfirm = {2}))) ORDER BY t.id desc'.format(self.config['partnerNo'], driver_mobile, driverConfirm)
            waybillId = self.DBUtil.excute_select_one_record(sql)
            sql2 = 'SELECT t.id, t.tmsBillCode FROM YD_APP_TRANSPORTCASH t ' \
                  'LEFT JOIN YD_TMS_PAY_DETAIL pd ON t.id = pd.wayBillId ' \
                  'WHERE (t.partnerNo =\'{0}\' AND t.mobile = \'{1}\' AND t.delStatus = 0 ' \
                  'AND t.retAmtConfirm IS NOT NULL AND pd.retAmtPayStatus = \'SUCCESS\' ' \
                  'AND (pd.retAmtPayStatus = \'UNPAID\' OR pd.retAmtPayStatus = \'FAIL\') ' \
                  'AND (((pd.cashLoanSchedule != \'FAIL\' OR pd.cashLoanSchedule IS NULL) ' \
                  'AND (pd.oilFeeLoanSchedule != \'FAIL\' OR pd.oilFeeLoanSchedule IS NULL) ' \
                  'AND (pd.destAmtLoanSchedule != \'FAIL\' OR pd.destAmtLoanSchedule IS NULL) ' \
                  'AND (pd.retAmtLoanSchedule != \'FAI\L\' OR pd.retAmtLoanSchedule IS NULL)' \
                  'AND t.driverConfirm = {2}))) ORDER BY t.id desc'.format(self.config['partnerNo'], driver_mobile,driverConfirm)
            tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            return waybillId, tmsBillCode,driver_mobile
        except Exception as e:
            self.logger.error('司机是否有可尾款支付的运单发生异常:{0}'.format(e))
            return None

    def is_have_payment_select_waybill(self, driver ,driverConfirm = '1'):
        '''司机是否有支付查询的运单'''
        try:
            driver_mobile = self.select_driver_mobile(driver)
            self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                                 user=self.config['db_user'], passwd=self.config['db_passwd'],
                                 dbname=self.config['db_dbname'], charset=self.config['db_charset'])
            sql = 'SELECT t.id FROM YD_APP_TRANSPORTCASH t ' \
                  'LEFT JOIN YD_TMS_PAY_DETAIL pd ON t.id = pd.wayBillId ' \
                  'WHERE (t.partnerNo =\'{0}\' AND t.mobile = \'{1}\' AND t.delStatus = 0 ' \
                  'AND t.driverConfirm = {2}))) ORDER BY t.id desc'.format(self.config['partnerNo'], driver_mobile, driverConfirm)
            waybillId = self.DBUtil.excute_select_one_record(sql)
            sql2 = 'SELECT t.id, t.tmsBillCode FROM YD_APP_TRANSPORTCASH t ' \
                  'LEFT JOIN YD_TMS_PAY_DETAIL pd ON t.id = pd.wayBillId ' \
                  'WHERE (t.partnerNo =\'{0}\' AND t.mobile = \'{1}\' AND t.delStatus = 0 ' \
                  'AND t.driverConfirm = {2}))) ORDER BY t.id desc'.format(self.config['partnerNo'], driver_mobile,
                                                                           driverConfirm)
            tmsBillCode = self.DBUtil.excute_select_one_record(sql2)
            return waybillId, tmsBillCode,driver_mobile
        except Exception as e:
            self.logger.error('司机是否有支付查询的运单发生异常:{0}'.format(e))
            return None
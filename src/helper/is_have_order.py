# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from util.db.dbutil import DBUtil
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil
from util.log.log import Log

class ISHaveOrder(object):
    '''查询是否存在订单'''
    def __init__(self):
        self.config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
        self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                             user=self.config['db_user'], passwd=self.config['db_passwd'],
                             dbname=self.config['db_dbname'], charset=self.config['db_charset'])
        self.logger = Log()

    def is_have_order(self,orderStatus='0'):
        '''查询企业是否有订单'''
        try:
            if orderStatus =='0':
                # 查询企业是否有未派车的订单
                sql = 'SELECT planNo FROM YD_TMS_ORDERPLAN WHERE orderStatus = \'0\' and partnerNo = \'{0}\' ' \
                      'ORDER BY id desc '.format(self.config['partnerNo'])
                planNo = self.DBUtil.excute_select_one_record(sql)
                self.logger.info('Query result:{0}'.format(planNo))
                return planNo
            elif orderStatus == '1':
                # 查询企业是否有派车中的订单
                sql = 'SELECT planNo FROM YD_TMS_ORDERPLAN WHERE orderStatus = \'1\' and partnerNo = \'{0}\'' \
                      'ORDER BY id desc '.format(self.config['partnerNo'])
                planNo = self.DBUtil.excute_select_one_record(sql)
                self.logger.info('Query result:{0}'.format(planNo))
                return planNo
            elif orderStatus == '2':
                # 查询企业是否有已派车的订单
                sql = 'SELECT planNo FROM YD_TMS_ORDERPLAN WHERE orderStatus = \'2\' and partnerNo = \'{0}\'' \
                      'ORDER BY id desc '.format(self.config['partnerNo'])
                planNo = self.DBUtil.excute_select_one_record(sql)
                self.logger.info('Query result:{0}'.format(planNo))
                return planNo
            elif orderStatus == '-1':
                # 查询企业是否有已取消的订单
                sql = 'SELECT planNo FROM YD_TMS_ORDERPLAN WHERE orderStatus = \'-1\' and partnerNo = \'{0}\'' \
                      'ORDER BY id desc '.format(self.config['partnerNo'])
                planNo = self.DBUtil.excute_select_one_record(sql)
                self.logger.info('Query result:{0}'.format(planNo))
                return planNo
            elif orderStatus == 'all':
                # 查询企业是否有订单
                sql = 'SELECT planNo FROM YD_TMS_ORDERPLAN WHERE partnerNo = \'{0}\' ORDER BY id desc '.format(
                    self.config['partnerNo'])
                planNo = self.DBUtil.excute_select_one_record(sql)
                self.logger.info('Query result:{0}'.format(planNo))
                return planNo
            else:
                self.logger.error('查询企业的订单状态错误:{0}'.format(orderStatus))
        except Exception as e:
            self.logger.error('查询企业是否有订单发生异常:{0}'.format(e))
            return None

    # def is_have_noSend_order(self):
    #     '''查询企业是否有未派车的订单'''
    #     try:
    #         sql = 'SELECT planNo FROM YD_TMS_ORDERPLAN WHERE orderStatus = \'0\' and partnerNo = \'{0}\''.format(
    #             self.config['partnerNo'])
    #         planNo = self.DBUtil.excute_select_one_record(sql)
    #         return planNo
    #     except Exception as e:
    #         self.logger.error('查询企业是否有未派车的订单发生异常:{0}'.format(e))
    #         return None
    #
    # def is_have_sending_order(self):
    #     '''查询企业是否有派车中的订单'''
    #     try:
    #         sql = 'SELECT planNo FROM YD_TMS_ORDERPLAN WHERE orderStatus = \'1\' and partnerNo = \'{0}\''.format(
    #             self.config['partnerNo'])
    #         planNo = self.DBUtil.excute_select_one_record(sql)
    #         return planNo
    #     except Exception as e:
    #         self.logger.error('查询企业是否有未派车的订单发生异常:{0}'.format(e))
    #         return None
    #
    # def is_have_sent_order(self):
    #     '''查询企业是否有已派车的订单'''
    #     try:
    #         sql = 'SELECT planNo FROM YD_TMS_ORDERPLAN WHERE orderStatus = \'2\' and partnerNo = \'{0}\''.format(
    #             self.config['partnerNo'])
    #         planNo = self.DBUtil.excute_select_one_record(sql)
    #         return planNo
    #     except Exception as e:
    #         self.logger.error('查询企业是否有已派车的订单发生异常:{0}'.format(e))
    #         return None
    #
    # def is_have_canceled_order(self):
    #     '''查询企业是否有已取消的订单'''
    #     try:
    #         sql = 'SELECT planNo FROM YD_TMS_ORDERPLAN WHERE orderStatus = \'-1\' and partnerNo = \'{0}\''.format(
    #             self.config['partnerNo'])
    #         planNo = self.DBUtil.excute_select_one_record(sql)
    #         return planNo
    #     except Exception as e:
    #         self.logger.error('查询企业是否有已取消的订单发生异常:{0}'.format(e))
    #         return None
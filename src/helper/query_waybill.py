import re
from util.db.dbutil import DBUtil
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil
from util.log.log import Log

class QueryWaybill(object):
    '''查询运单'''
    def __init__(self):
        self.config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
        self.logger = Log()

    def query_waybill_status(self,tmsBillCode):
        '''查询运单状态'''
        try:
            self.DBUtil = DBUtil(host=self.config['db_host'], port=self.config['db_port'],
                                 user=self.config['db_user'], passwd=self.config['db_passwd'],
                                 dbname=self.config['db_dbname'], charset=self.config['db_charset'])
            sql = 'SELECT transStatus FROM YD_APP_TRANSPORTCASH WHERE tmsBillCode = \'{0}\''.format(tmsBillCode)
            trans_status = self.DBUtil.excute_select_one_record(sql)
            return trans_status
        except Exception as e:
            self.logger.error('查询运单状态发生异常:{0}'.format(e))
            return None
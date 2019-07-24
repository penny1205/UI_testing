#__author__ = 'pan'
# -*- coding:utf-8 -*-

from util.http.httpclient import HttpClient
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil
from util.log.log import Log

class DriverSelectApi(object):
    '''
    我的外请车列表,查询结果是已关联的外请车
    /api/tms/driver/listTmsAppDriver
    '''
    __slots__ = ('__driverSelectApiUrl','partnerNo', '__head_dict','logger')

    def __init__(self):
        config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
        self.__driverSelectApiUrl = "https://{0}:{1}{2}/api/tms/driver/listTmsAppDriver".format(
            config['tms_api_host'],config['tms_api_port'],config['tms_api_path'])
        self.__head_dict = {
            'token': config['tms_api_token'],
            'yd_oauth': config['tms_api_token'],
        }
        self.partnerNo = config['partnerNo']
        self.logger = Log()


    def driver_select_api(self,currentPage='1',rows='10',mobile ='',name='',carNo='',recentLineStart='',recentLineEnd=''):
         '''查询已关联的外请车'''
         self.logger.info('#####  {0}  #####'.format(__name__))
         try:
             payload ={
                 'currentPage': currentPage,
                 'rows': rows,
                 'partnerNo': self.partnerNo,
                 'name': name,
                 'mobile': mobile,
                 'carNo': carNo,
                 'recentLineStart':recentLineStart,
                 'recentLineEnd':recentLineEnd
             }
             response = HttpClient().get(self.__driverSelectApiUrl,self.__head_dict,payload)
             return response
         except Exception as e:
             Log().error('查询已关联的外请车发生异常:{0}'.format(e))
             return None

if __name__ == '__main__':
    config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
    response = DriverSelectApi().driver_select_api(name='刘新宇')
    print(response.json()['content']['dataList']['mobile'])
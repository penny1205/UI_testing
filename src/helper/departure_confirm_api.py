#__author__ = 'pan'
# -*- coding:utf-8 -*-

from util.http.httpclient import HttpClient
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil
from util.log.log import Log
from src.helper.get_token_api import GetTokenApi


class DepartureConfirmApi(object):
    '''
    发车确认
    /payment/tmsConfirmWayBill
    '''
    __slots__ = ('__departureConfirmWayBillApiUrl', '__head_dict','logger')

    def __init__(self):
        config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
        self.__departureConfirmWayBillApiUrl = 'https://{0}:{1}{2}/payment/tmsConfirmWayBill'.format(
            config['app_api_host'],config['app_api_port'],config['app_api_path'])
        token = GetTokenApi().get_token_api().json()['content']['token']
        self.__head_dict = {
            'token': token,
            'YD_OAUTH': token
        }
        self.logger = Log()


    def departure_confirm_api(self,billId=''):
        '''发车确认'''
        self.logger.info('#####  {0}  #####'.format(__name__))
        try:
            payload ={ 'billId':billId}
            response = HttpClient().post_json(self.__departureConfirmWayBillApiUrl,payload,self.__head_dict)
            return response
        except Exception as e:
            self.logger.error('发车确认发生异常:{0}'.format(e))
            return None

if __name__ == "__main__":
    test = DepartureConfirmApi().departure_confirm_api('719656')
    print(test.json())
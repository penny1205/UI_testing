#__author__ = 'pan'
# -*- coding:utf-8 -*-

import os
from util.http.httpclient import HttpClient
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil
from util.log.log import Log

class DriverConfirmApi(object):
    '''
    司机确认发车确认接口
    /app/payment/confirmWayBill
    '''
    __slots__ = ('__driverConfirmApiUrl', '__head_dict', 'partnerNo','logger')

    def __init__(self):
        config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
        self.__driverConfirmApiUrl = 'https://{0}:{1}{2}/payment/confirmWayBill'.format(
            config['app_api_host'], config['app_api_port'], config['app_api_path'])
        self.partnerNo = config['partnerNo']
        self.__head_dict = {
            'YD_VERSION': '3.0',
            'YD_CLIENT': 'driver',
            'YD_OAUTH': config['driver_YD_OAUTH']
        }
        self.logger = Log()

    def driver_confirm_api(self, billId='', totalAmt='', preAmt='', oilAmt='', destAmt='',
                                 lastAmt='', receiverId=''):
        """ 司机确认发车 """
        self.logger.info('#####  {0}  #####'.format(__name__))
        try:
            receipt_0 = FileUtil.getProjectObsPath() + os.path.sep + 'image' + os.path.sep + 'logo.png'
            receipt_name_0 = os.path.basename(receipt_0)
            with open(receipt_0, 'rb') as receipt_0:
                photoAirWay = (receipt_name_0, receipt_0.read())
            payload = {'id': (None, str(billId)),
                       'partnerNo': (None, str(self.partnerNo)),
                       'totalAmt': (None, str(totalAmt)),
                       'preAmt': (None, str(preAmt)),
                       'oilAmt': (None, str(oilAmt)),
                       'destAmt': (None, str(destAmt)),
                       'lastAmt': (None, str(lastAmt)),
                       'receiverId': (None, str(receiverId)),
                       'photoAirWay': photoAirWay
                       }
            response = HttpClient().post_multipart(url=self.__driverConfirmApiUrl, files=payload,
                                                   header_dict=self.__head_dict)
            return response
        except Exception as e:
            self.logger.error('司机确认发车发生异常:{0}'.format(e))
            return None

if __name__ == "__main__":
    test = DriverConfirmApi().driver_confirm_api('719656', totalAmt='10', preAmt='1', oilAmt='1', destAmt='1',
                                 lastAmt='1')
    print(test.json())

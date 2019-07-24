#! /usr/bin/python3
# -*- coding:utf-8 -*-
# author: vin

from util.http.httpclient import HttpClient
from util.config.yaml.readyaml import ReadYaml
from util.log.log import Log
from util.file.fileutil import FileUtil
from util.common.function import format_photo


class DriverUploadReceiptApi(object):
    # 司机上传回单
    def __init__(self):
        config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
        self._driverUploadReceiptApiUrl = 'https://{0}:{1}{2}/shipper/uploadReceipt'.format(
            config['app_api_host'], config['app_api_port'], config['app_api_path'])
        self._head_dict = {
            'YD_VERSION': str(config['chezhu_version']),
            'YD_CLIENT': str(config['chezhu_client']),
            'YD_OAUTH': str(config['driver_YD_OAUTH']),
        }
        self.logger = Log()

    def driver_upload_receipt_api(self, waybillId='', abnormal='', damaged='', losted='', memo='', type='C', receipt0='',
                                  receipt1='', receipt2='', receipt3='', receipt4=''):
        '''司机上传回单'''

        self.logger.info('#####  {0}  #####'.format(__name__))
        try:
            receipt0 = format_photo(receipt0)  # 需传图片绝对路径，对图片进行表单提交格式化处理
            receipt1 = format_photo(receipt1)
            receipt2 = format_photo(receipt2)
            receipt3 = format_photo(receipt3)
            receipt4 = format_photo(receipt4)
            files = {
                "id": (None, str(waybillId)),  # 运单id
                "abnormal": (None, abnormal),  # 是否有异常 Y：是、N：是
                "damaged": (None, damaged),  # 是否有破损 Y：是、N：是
                "losted": (None, losted),  # 是否丢失 Y：是、N：是
                "memo": (None, memo),  # 备注
                "type": (None, type),  # S：货主、C：司机
                "receipt_0": receipt0,  # 回单图片文件
                "receipt_1": receipt1,
                "receipt_2": receipt2,
                "receipt_3": receipt3,
                "receipt_4": receipt4
            }
            response = HttpClient().post_multipart(self._driverUploadReceiptApiUrl, header_dict=self._head_dict,files=files)
            return response
        except Exception as error:
            self.logger.info('####  发生错误：{0}  ####\t\t####  返回None  ####'.format(error))
            return None


if __name__ == '__main__':
    test = DriverUploadReceiptApi().driver_upload_receipt_api(waybillId='720518',receipt0=FileUtil.getProjectObsPath() + '/image/receipt.jpg')
    print(test)
    print(test.json())

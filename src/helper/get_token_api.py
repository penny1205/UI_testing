#__author__ = 'pan'
# -*- coding:utf-8 -*-

from util.http.httpclient import HttpClient
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil
from util.log.log import Log
from src.helper.login_api import LoginApi

class GetTokenApi(object):
    '''
    获取tms接口请求的token
   /app/shipper/tokenLogin
    '''
    # __slots__ = ('__getTokenApiUrl')

    def __init__(self):
        self.config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
        self.__getTokenApiUrl ='https://hfuapi.keking.cn:8015/app/shipper/tokenLogin'
        self.__head_dict = {
            'YD_VERSION': '3.7',
            'YD_CLIENT': 'shipper',
        }


    def get_token_api(self):
         '''货主APP登录接口'''
         try:
             appToken = LoginApi().login_api(self.config['name'], self.config['password'], self.config['productId'], self.config['source']
                                  ).json()['content']['appToken']
             payload ={'userCenterToken': appToken}
             response = HttpClient().post_json(self.__getTokenApiUrl,header_dict=self.__head_dict,body_dict=payload)
             return response
         except Exception as e:
             Log().error('获取tms接口请求的token发生异常:{0}'.format(e))
             return None

if __name__ == '__main__':
    response = GetTokenApi().get_token_api()
    print(response.json()['content']['token'])
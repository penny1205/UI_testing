#__author__ = 'pan'
# -*- coding:utf-8 -*-

from util.http.httpclient import HttpClient
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil
from util.log.log import Log

class LoginApi(object):
    '''
    货主APP登录接口
    /api/login/token/password
    '''
    __slots__ = ('__LoginApiUrl', '__head_dict')

    def __init__(self):
        config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
        self.__LoginApiUrl = "https://{0}:{1}{2}/api/login/token/password".format(
            config['account_app_api_host'],config['account_app_api_port'],config['account_app_api_path'])
        self.__head_dict = {
            'productId': config['productId'],
            'Content-Type': 'application/json',
        }

    def login_api(self,name='',password='',productId='',source=''):
         '''货主APP登录接口'''
         try:
             payload ={
                 'loginId': name,
                 'password': password,
                 'productId': productId,
                 'source': source,
             }
             response = HttpClient().post_json(self.__LoginApiUrl,payload,self.__head_dict)
             return response
         except Exception as e:
             Log().error('货主APP登录接口发生异常:{0}'.format(e))
             return None

if __name__ == '__main__':
    config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
    response = LoginApi().login_api(config['name'],config['password'],config['productId'],config['source'])
    print(response.json()['content']['appToken'])
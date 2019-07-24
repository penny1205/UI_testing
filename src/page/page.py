# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from util.log.log import Log
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil
from src.helper.login_api import LoginApi

class Page():
    '''物流云系统'''
    def __init__(self, selenium_driver):
        self.driver = selenium_driver
        self.config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
        self.base_url = self.config['base_url']
        self.logger = Log()

    def login(self):
        '''登录'''
        url = self.base_url +  LoginApi().login_api(self.config['name'],self.config['password'],self.config['productId'],
                                                    self.config['source']).json()['content']['appToken']
        self.driver.open(url)
        self.driver.driver.execute_script("return document.readyState == 'complete'")
        # self.driver.driver.implicitly_wait(5)

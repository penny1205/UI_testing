#__author__ = 'pan'
#coding=utf-8

import configparser

class ReadInit:
    """
    专门读取配置文件的，.ini文件格式
    """
    def __init__(self, filename):
        config_path = filename
        self.cf = configparser.ConfigParser()
        self.cf.read(config_path,encoding='UTF-8')

    def getValue(self, env, name):
        """
        [projectConfig]
        project_path=project_path=H:\work\gongdan
        :param env:[projectConfig]
        :param name:project_path
        :return:project_path=H:\work\gongdan
        """
        return self.cf.get(env,name)
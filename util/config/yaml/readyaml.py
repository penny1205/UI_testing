# -*- coding:utf-8 -*-

import yaml

class ReadYaml:
    """专门读取配置文件的，.yaml文件格式"""
    def __init__(self,filename):
        self.stream = open(filename,encoding= 'utf-8')

    def getValue(self):
        dict = yaml.load(self.stream)
        self.stream.close()
        return dict
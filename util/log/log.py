# __author__ = 'penny'
# -*- coding:utf-8 -*-

import logging
import os
import time
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil

class Log:
    '''打印日志'''

    def __init__(self):
        self.config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()

    def _print_console(self,level,message,log_path):
        try:
            self.logname = os.path.join(log_path, '{0}.log'.format(time.strftime("%Y-%m-%d")))
            # 创建一个logger
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            # 创建一个handler ,用于写入日志文件
            fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            # 创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            # 定义handler的输出格式
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            # 给logger添加handler
            logger.addHandler(fh)
            logger.addHandler(ch)
            # 记录一条记录
            if level == 'info':
                logger.info(message)
            elif level == 'debug':
                logger.debug(message)
            elif level == 'warning':
                logger.warning(message)
            elif level == 'error':
                logger.error(message)
            logger.removeHandler(ch)
            logger.removeHandler(fh)
            # 关闭打开的文件
            fh.close()
        except Exception:
            return None

    def info(self,message):
        log_path = self.config['log_path_info']
        self._print_console('info',message,log_path)

    def debug(self,message):
        log_path = self.config['log_path_info']
        self._print_console('debug',message,log_path)

    def warning(self,message):
        log_path = self.config['log_path_error']
        self._print_console('warning',message,log_path)

    def error(self,message):
        log_path = self.config['log_path_error']
        self._print_console('error',message,log_path)

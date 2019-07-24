# __author__ = ‘pan‘
# -*-coding:utf-8-*-

import unittest
from util.selenium.pyselenium import PySelenium
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil
from util.log.log import Log

class MyTest(unittest.TestCase):
    def setUp(self):
        self.logger = Log()
        self.logger.info('############################### START ###############################')
        config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
        self.driver = PySelenium(config['browser'],config['driver'])
        # self.driver.wait(30)
        self.driver.max_window()
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([],self.verificationErrors)
        self.logger.info('################################ END ################################')

if __name__ == '__main__':
    unittest.main()
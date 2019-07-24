# -*-coding:utf-8-*-
import unittest
from util.report.template import report_keking


class ReportUtil:
    def generate_report(self, unittest_suit, report_title, report_desc, report_path):
        try:
            if (isinstance(unittest_suit, unittest.TestSuite)):
                pass
            else:
                return False
            report_file = open(report_path, 'wb')
            runner = report_keking.HTMLTestRunner(stream=report_file, title=report_title, description=report_desc)
            runner.run(unittest_suit)
            return True
        except Exception:
            return False


if __name__ == '__main__':
    from util.unittest.unittestutil import UnitTestUtil
    suite = UnitTestUtil().discover_pattern('E:/PythonWorkSpace/tms_api_testing/biz', '*.py')
    print(ReportUtil().generate_report(suite, '测试报告', '随便测试一下Report', 'G:/report/report.html'))

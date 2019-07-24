import unittest
import re


class UnitTestUtil:
    def discover_pattern_undefine(self, filepath, filename_pattern, casename_pattern):
        suite = unittest.TestSuite()
        discover_cases = unittest.TestLoader().discover(filepath, pattern=filename_pattern, top_level_dir=None)
        for test_suite in discover_cases:
            for test_case in test_suite:
                index = 0
                casenum = len(test_case._tests)
                while index < casenum:
                    import re
                    if (re.match(casename_pattern, test_case._tests[index]._testMethodName) == None):
                        del (test_case._tests[index])
                        casenum = casenum - 1
                    else:
                        index = index + 1
                suite.addTest(test_case)
        return suite

    def discover_pattern(self, filepath, filename_pattern):
        suite = unittest.TestSuite()
        discover_cases = unittest.TestLoader().discover(filepath, pattern=filename_pattern, top_level_dir=None)
        for test_suite in discover_cases:
            for testcase in test_suite:
                suite.addTest(testcase)
        return suite

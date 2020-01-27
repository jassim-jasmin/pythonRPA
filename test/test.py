import unittest
from DataFetching.validation import LocatorValidation
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
import sys
import json

class ValidationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # initial run
        pathFile = open('path.json', 'r')
        path = json.loads(pathFile.read())
        pathFile.close()

        path = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'linux', path)
        print('begin')
        self.locatorValidation = LocatorValidation(path)

    def test_pattern_check(self):
        self.assertTrue(self.locatorValidation.patternCheck('^and test$', 'and test'))
        self.assertFalse(self.locatorValidation.patternCheck('^and test$', 'blah and test'))
        self.assertFalse(self.locatorValidation.patternCheck('^and test$', 'blah and test blll'))
        self.assertTrue(self.locatorValidation.patternCheck('^And test$', 'and test'))

    def tearDown(self):
        # final run
        print('end')
        del self.locatorValidation



def suite():

    suite = unittest.TestSuite()
    suite.addTest(ValidationTestCase('test_pattern_check'))
    # suite.addTest(ValidationTestCase('test_widget_resize'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
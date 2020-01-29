import unittest
from DataFetching.validation import LocatorValidation
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
from DataFetching.Locator import Locator
import sys
import json

from DataFetching.test_DataHandling import *

class ValidationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # initial run
        pathFile = open('path.json', 'r')
        path = json.loads(pathFile.read())
        pathFile.close()

        path = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'linux', path)
        print('begin')
        self.locatorValidation = LocatorValidation(path)
        self.locator = Locator(path)

    def test_pattern_check(self):
        self.assertTrue(self.locatorValidation.patternCheck('^and Test$', 'and Test'))
        self.assertFalse(self.locatorValidation.patternCheck('^and Test$', 'blah and Test'))
        self.assertFalse(self.locatorValidation.patternCheck('^and Test$', 'blah and Test blll'))
        self.assertTrue(self.locatorValidation.patternCheck('^And Test$', 'and Test'))

    def test_add_locatortag(self):
        self.assertTrue(self.locator.addLocatorTag('test_layer','test_locator','True', 'datafeth_test_'))

    def tearDown(self):
        # final run
        print('end')
        del self.locatorValidation



def suite():

    suite = unittest.TestSuite()
    suite.addTest(ValidationTestCase('test_pattern_check'))
    suite.addTest(ValidationTestCase('test_widget_resize'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
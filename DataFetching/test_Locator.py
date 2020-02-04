from unittest import TestCase
from DataFetching.Locator import Locator
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
import sys

class TestLocator(TestCase):
    def setUp(self) -> None:
        generalExceptionHandling = GeneralExceptionHandling()
        path = generalExceptionHandling.readFileAndReturnJson('path.json')
        if sys.platform == 'linux':
            path = path['linux']
        else:
            path = path['windows']

        self.locator = Locator(path)
    def test_add_locator_tag(self):
        print('test_add_locator_tag')
        # self.fail()

    def test_locator_data_search_and_replace(self):
        print('test_locator_data_search_and_replace')
        layerDataMain = {'locator': ['titleName'], 'locatorData': {'testdata': {'titleName': 'TICOR TITLE DO'}, 'testdata2':{'titleName':' TITLE COMPANY'}}}
        processed = self.locator.locatorDataSearchAndReplace(layerDataMain, 'title_lookup')
        self.assertNotEqual(False, processed)
        self.assertDictEqual({'locator': ['titleName'], 'locatorData': {'testdata': {'titleName': 'TICOR TITLE'}, 'testdata2': {'titleName': 'TITLE COMPANY'}}}, processed)

from unittest import TestCase
import unittest
from DataFetching.DataHandling import DataHandling
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
import json


class TestDataHandling(TestCase):
    def setUp(self) -> None:
        self.dataHandling = DataHandling(self.getPath(), 'datafetch_test_')
        self.assertTrue(True)

    def tearDown(self):
        # final run
        print('end')
        del self.dataHandling

    def test_get_connection(self):
        print('test_get_connection')
        self.assertTrue(self.dataHandling.getConnection())

    def getPath(self):
        pathFile = open('path.json', 'r')
        path = json.loads(pathFile.read())
        pathFile.close()

        path = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'linux', path)

        return path

    def test_create_layer(self):
        self.assertTrue(self.dataHandling.deleteLayer('test'))
        self.assertTrue(self.dataHandling.createLayer('test'))
        self.assertTrue(self.dataHandling.deleteLayer('test'))

    def test_table_exists(self):
        self.assertTrue(self.dataHandling.deleteLayer('test'))
        self.assertFalse(self.dataHandling.checkLayerExists('test'))
        self.assertTrue(self.dataHandling.createLayer('test'))
        self.assertTrue(self.dataHandling.checkLayerExists('test'))
        self.assertTrue(self.dataHandling.deleteLayer('test'))

    # def test_get_table_from_db(self):
    #     print('test_get_table_from_db')
    # self.dataHandling.getTableFromDB('test')

    def test_insert_layer(self):
        print('test_insert_layer')
        self.dataHandling.deleteLayer('test')
        self.dataHandling.insertLayer('test', 'locatorId', 'locatorData')

        count = self.dataHandling.getLayerDataCount('test')
        print('count;;;', count)
        if count:
            if count != 1:
                self.assertTrue(False, 'count miss match, should contain only one record, delete layer might not working well')
            else:
                pass
            # inserting different entry with validation
            self.assertTrue(self.dataHandling.insertLayer('test', 'locatorId', 'locatorData2'), 'should not insert duplicate locator tag')

            count = self.dataHandling.getLayerDataCount('test')
            print('duplicate count', count)
            if count != 2:
                self.assertTrue(False, 'Locator Re insertion failed, count shold be 1')

            # inserting duplicate entry with validation
            self.assertFalse(self.dataHandling.insertLayer('test', 'locatorId', 'locatorData'),
                            'should not insert duplicate locator tag')
            print('duplicate count', count)
            if count == 3:
                self.assertTrue(False, 'Locator Re insertion duplicate success, count shold be 2')

        self.assertTrue(count, 'Locator data insertion failed')

        self.assertTrue(self.dataHandling.deleteLayer('test'))

    def test_check_similar_record(self):
        print('test_check_similar_record')
        self.dataHandling.insertLayer('test', 'locatorId', 'locatorData')
        self.assertTrue(self.dataHandling.checkSimilarRecord('test', 'locatorId', 'locatorData'), 'duplicate locator insertion')
        self.dataHandling.insertRecord('test', 'locatorId', 'locatorData')
        self.assertTrue(self.dataHandling.checkSimilarRecord('test', 'locatorId', 'locatorData'), 'duplicate locator insertion more than record validation failed')
        self.dataHandling.deleteLayer('test')


# def suite():
#
#     suite = unittest.TestSuite()
#     suite.addTest(TestDataHandling('test_get_connection'))
#     return suite
#
# if __name__ == '__main__':
#     runner = unittest.TextTestRunner()
#     runner.run(suite())

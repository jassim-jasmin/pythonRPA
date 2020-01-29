from unittest import TestCase
import unittest
from DataFetching.DataHandling import DataHandling
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
import json


class TestDataHandling(TestCase):
    def setUp(self) -> None:
        self.dataHandling = DataHandling(self.getDbOption(), 'datafetch_test_')
        self.assertTrue(True)

    def tearDown(self):
        # final run
        # print('end')
        del self.dataHandling

    def test_get_connection(self):
        print('test_get_connection')
        self.assertTrue(self.dataHandling.getConnection())

    def getDbOption(self):
        pathFile = open('db.json', 'r')
        path = json.loads(pathFile.read())
        pathFile.close()
        path = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling, 'test', path)

        # path = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'linux', path)

        return path

    def test_create_layer(self):
        print('test_create_layer')
        self.assertTrue(self.dataHandling.deleteLayer('test'))
        self.assertTrue(self.dataHandling.createLayer('test'))
        self.assertTrue(self.dataHandling.deleteLayer('test'))

    def test_table_exists(self):
        print('test_table_exists')
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
        if count:
            if count != 1:
                self.fail('count miss match, should contain only one record, delete layer might not working well')
            else:
                pass
            # inserting different entry with validation
            self.assertTrue(self.dataHandling.insertLayer('test', 'locatorId', 'locatorData2'),
                            'should not insert duplicate locator tag')

            count = self.dataHandling.getLayerDataCount('test')
            if count != 2:
                self.fail('Locator Re insertion failed, count shold be 1')

            # inserting duplicate entry with validation
            self.assertFalse(self.dataHandling.insertLayer('test', 'locatorId', 'locatorData'),
                             'should not insert duplicate locator tag')
            if count == 3:
                self.fail('Locator Re insertion duplicate success, count shold be 2')

        self.assertTrue(count, 'Locator data insertion failed')

        self.assertTrue(self.dataHandling.deleteLayer('test'))

    def test_check_similar_record(self):
        print('test_check_similar_record')
        self.dataHandling.insertLayer('test', 'locatorId', 'locatorData')
        self.assertTrue(self.dataHandling.checkSimilarRecord('test', 'locatorId', 'locatorData'),
                        'duplicate locator insertion')
        self.dataHandling.insertRecord('test', 'locatorId', 'locatorData')
        self.assertTrue(self.dataHandling.checkSimilarRecord('test', 'locatorId', 'locatorData'),
                        'duplicate locator insertion more than record validation failed')
        self.dataHandling.deleteLayer('test')

    def test_generate_locator_from_table_field(self):
        print('test_generate_locator_from_table_field')
        dataFrame = self.dataHandling.generateLocatorFromTableField('test_layer', 'test_locator_id', 'mj_db', 'datafeth_locator_title_lookup', 'locatorData')
        if dataFrame.empty:
            self.fail('layer generation from database table field failed')

        dataFrame = self.dataHandling.generateLocatorFromTableField('test_layer', 'test_locator_id', 'mj_db1', 'datafeth_locator_title_lookup', 'locatorData')
        if not dataFrame.empty:
            self.fail('error schema validation failed')

        dataFrame = self.dataHandling.generateLocatorFromTableField('test_layer', 'test_locator_id', 'mj_db',
                                                                    'datafeth_locator_title_lookup1', 'locatorData')
        if not dataFrame.empty:
            self.fail('error table validation failed')

        dataFrame = self.dataHandling.generateLocatorFromTableField('test_layer', 'test_locator_id', 'mj_db',
                                                                    'datafeth_locator_title_lookup', 'locatorData1')
        if not dataFrame.empty:
            self.fail('error field validation failed')


    def test_get_data_from_dbas_df(self):
        print('test_get_data_from_dbas_df')

        dataFrame = self.dataHandling.getDataFromDBAsDF('mj_db', 'datafeth_locator_title_lookup', 'locatorData')
        if dataFrame.empty:
            self.fail('Returned empty data frame')

        dataFrame = self.dataHandling.getDataFromDBAsDF('mj_db', 'datafeth_locator_title_lookup', 'locatorData1')
        if not dataFrame.empty:
            self.fail('Invalid field')

        dataFrame = self.dataHandling.getDataFromDBAsDF('mj_db', 'datafeth_locator_title_lookup1', 'locatorData')
        if not dataFrame.empty:
            self.fail('Invalid table')

        dataFrame = self.dataHandling.getDataFromDBAsDF('mj_db1', 'datafeth_locator_title_lookup1', 'locatorData')
        if not dataFrame.empty:
            self.fail('Invalid schema')


# def suite():
#     suite = unittest.TestSuite()
#     suite.addTest(TestDataHandling('test_get_connection'))
#     suite.addTest(TestDataHandling('test_create_layer'))
#     suite.addTest(TestDataHandling('test_table_exists'))
#     suite.addTest(TestDataHandling('test_insert_layer'))
#     suite.addTest(TestDataHandling('test_check_similar_record'))
#     suite.addTest(TestDataHandling('test_generate_locator_from_table_field'))
#     # suite.addTest(TestDataHandling('test_get_data_from_dbas_df'))
#     return suite
#
#
# if __name__ == '__main__':
#     runner = unittest.TextTestRunner()
#     runner.run(suite())


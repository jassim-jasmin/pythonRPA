import json
import sys
from unittest import TestCase
from DataFetching.LocatorFromDB import SqlConnect

class TestSqlConnect(TestCase):
    def getPath(self):
        fp = open('path.json', 'r')
        path = json.loads(fp.read())[sys.platform]
        fp.close()
        return path

    def setUp(self) -> None:
        self.sqlConnect = SqlConnect(self.getPath())

    def test_get_connection(self):
        print('test_get_connection')
        self.assertTrue(self.sqlConnect.getConnection())

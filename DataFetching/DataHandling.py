import json
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

class DataHandling:
    def __init__(self, path, group):
        self.path = path
        self.dbOption = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling, 'DB', self.path)
        self.LocatorDirectory = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                          'DataFetching,filesPath', self.path)
        # self.getConnection()
        self.layerConnectorName = group
        self.locatorId = 'locator_id'
        self.locatorData = 'locatorData'

    def __del__(self):
        try:
            self.mydb.close()
        except:
            pass

    def getConnection(self):
        try:
            try:
                self.mydb.close()
            except:
                pass
            fp = open(self.dbOption, 'r')
            dbOptons = json.loads(fp.read())
            fp.close()
            # print(dbOptons['mysql']['default'])
            self.mydb = mysql.connector.connect(host=dbOptons['mysql']['default']['HOST'], user=dbOptons['mysql']['default']['USER'], password=dbOptons['mysql']['default']['PASSWORD'], database=dbOptons['mysql']['default']['DB'])
            # print(self.mydb)
            return True
        except Exception as e:
            print('error in mysql', e)
            return False

    def getTableFromDB(self, layerName):
        self.getConnection()
        tableName = self.layerConnectorName+layerName
        if self.checkTableExists(tableName):
            print('table exist')
        else:
            return False
        return True

    def createLayer(self, layerName):
        try:
            tableName = self.layerConnectorName + layerName
            self.getConnection()
            sql = f"create table {tableName} (locator_id varchar(200), locatorData varchar(500));"
            print(sql)
            cursor = self.mydb.cursor()
            cursor.execute(sql)
            cursor.close()
            return True
        except Exception as e:
            print('error in creatLayer in DataHandling', e)
            return False

    def deleteLayer(self, layerName):
        try:
            tableName = self.layerConnectorName + layerName
            sql = f"drop table if exists {tableName};"
            print(sql)
            self.getConnection()
            cursor = self.mydb.cursor()
            cursor.execute(sql)
            cursor.close()
            return True
        except Exception as e:
            print('error in deleteLayer in DataHandling', e)
            return False

    def checkLayerExists(self, layerName):
        self.getConnection()
        tableName = self.layerConnectorName + layerName
        return self.checkTableExists(tableName)

    def checkTableExists(dbcon, tablename):
        dbcur = dbcon.mydb.cursor()
        dbcur.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(tablename.replace('\'', '\'\'')))
        status = dbcur.fetchone()
        if status:
            if status[0] == 1:
                dbcur.close()
                return True

        dbcur.close()
        return False

    def getLayerDataCount(self, layerName):
        if self.checkLayerExists(layerName):
            tableName = self.layerConnectorName + layerName
            self.getConnection()
            sql = f"select count({self.locatorId}) from {tableName};"
            cursor = self.mydb.cursor()
            cursor.execute(sql)
            count = cursor.fetchone()

            return count[0]
        else:
            return False


    def checkSimilarRecord(self, layerName, locatorId, locatorData):
        tableName = self.layerConnectorName + layerName
        sql = f"select count({self.locatorId}) from {tableName} where {self.locatorId} = '{locatorId}' and {self.locatorData} = '{locatorData}'"
        print(sql)
        self.getConnection()
        cursor = self.mydb.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()

        print('count::', count)
        if count:
            if count[0] != 0:
                return True
            else:
                return False
        else:
            return False

    def insertRecord(self, layerName, locatorId, locatorData):
        tableName = self.layerConnectorName + layerName
        self.getConnection()

        sql = f"insert into {tableName} ({self.locatorId},{self.locatorData}) values ('{locatorId}','{locatorData}')"
        print(sql)
        cursor = self.mydb.cursor()
        cursor.execute(sql)
        cursor.close()
        self.mydb.commit()
        self.mydb.close()
        return True

    def insertLayer(self, layerName, locatorId, locatorData):
        try:
            if self.checkLayerExists(layerName):
                if not self.checkSimilarRecord(layerName, locatorId, locatorData):
                    self.insertRecord(layerName, locatorId, locatorData)
                    return True
                else:
                    return False
            else:
                print('No layer exist')
                if self.createLayer(layerName):
                    self.insertRecord(layerName, locatorId, locatorData)
                    return True
                else:
                    return False
        except Exception as e:
            print('error in insertLayer in DataHandling', e)
            return False




import json
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

class DataHandling:
    def __init__(self, path, group):
        self.path = path
        # self.dbOption = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling, 'DB', self.path)
        self.dbOptions = path
        # self.LocatorDirectory = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
        #                                                                   'DataFetching,filesPath', self.path)
        # self.getConnection()
        self.layerConnectorName = group
        self.locatorId = 'locator_id'
        self.locatorData = 'locatorData'
        self.layerConnectorName = 'datafeth_locator_'

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
            self.mydb = mysql.connector.connect(host=self.dbOptions['mysql']['default']['HOST'], user=self.dbOptions['mysql']['default']['USER'], password=self.dbOptions['mysql']['default']['PASSWORD'], database=self.dbOptions['mysql']['default']['DB'])
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
        # print(sql)
        self.getConnection()
        cursor = self.mydb.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()

        if count:
            if count[0] != 0:
                return True
            else:
                return False
        else:
            return False

    def insertRecord(self, layerName, locatorId, locatorData):
        try:
            tableName = self.layerConnectorName + layerName
            self.getConnection()

            sql = f"insert into {tableName} ({self.locatorId},{self.locatorData}) values ('{locatorId}','{locatorData}')"
            # print(sql)
            cursor = self.mydb.cursor()
            cursor.execute(sql)
            cursor.close()
            self.mydb.commit()
            self.mydb.close()
            return True
        except Exception as e:
            print('error in insertRecord in DataHandling', e)
            return False

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

    def generateLocatorFromTableField(self, layerName, locatorId, schemaName, tableName, fieldNameFromTable):
        try:
            dataFrameFromDB = self.getDataFromDBAsDF(schemaName, tableName, fieldNameFromTable)
            dataFrameFromDB[self.locatorId]=locatorId

            if not dataFrameFromDB.empty:
                sql = f"create table {self.layerConnectorName+layerName} ({self.locatorId} varchar(200), {self.locatorData} varchar(500));"
                print(sql)

            dataFrameFromDB.rename(columns={fieldNameFromTable: self.locatorData}, inplace=True)

            print(dataFrameFromDB)
            return dataFrameFromDB
        except Exception as e:
            print('error in generateLocatorFromTableField in DataHandling', e)
            return pd.DataFrame()

    def getDataFromDBAsDF(self, dataBaseForFetching, tableName, filedName):
            try:
                dbOptions = self.dbOptions['mysql']['default']
                engine = create_engine(
                    f'mysql+pymysql://{dbOptions["USER"]}:{dbOptions["PASSWORD"]}@{dbOptions["HOST"]}/{dataBaseForFetching}')

                sql = f"select distinct {filedName} from {tableName}"
                where = f" where {filedName} is not null"

                df = pd.read_sql(sql+where , con=engine)

                return df
            except Exception  as e:
                # print('error in getLocatorFromDb in LocatorFromDB', e)
                 return pd.DataFrame()
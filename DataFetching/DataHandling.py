import json
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

class DataHandling:
    def __init__(self, path, group):
        self.path = path
        self.dbOptions = path
        self.layerConnectorName = group
        self.locatorId = 'locator_id'
        self.locatorData = 'locatorData'
        self.layerConnectorName = 'datafeth_locator_'
        print(path)

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

            return True
        except Exception as e:
            print('error in mysql', e)
            return False

    def getTableFromDB(self, layerName) -> bool:
        """
        Layer name corresponding table from db is checked
        :param layerName: Name of layer
        :tableName: Converted corresponding mysql table name
        :return: True if exist else False
        :todo: Unfinished
        """
        self.getConnection()
        tableName = self.layerConnectorName+layerName
        if self.checkTableExists(tableName):
            return True
        else:
            return False


    def createLayer(self, layerName) -> bool:
        """
        Creating table with structure for layer name
        :param layerName: Name of layer
        :tableName: Converted corresponding mysql table Name
        :return:
        """
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
        """
        Layer name exist in db then delete
        :param layerName: Name of layer
        :tableName: Converted corresponding mysql table name
        :return: If no database error occure means Return True else False
        """
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

    def checkLayerExists(self, layerName) -> bool:
        """
        Confirming a layer corresponding table exists
        :param layerName: Layer name
        :tableName: Converting corresponding name for db table name
        :return: True if table exist else False
        """
        self.getConnection()
        tableName = self.layerConnectorName + layerName
        return self.checkTableExists(tableName)

    def checkTableExists(dbcon, tablename) -> bool:
        """
        Directly checking tablename in DB
        :param tablename:
        :return: True if exist else False
        """
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
        """
        Calculating overal row count corresponging to locator id
        :param layerName: Name of layer
        :return: Number if table exist else False
        """
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


    def checkSimilarRecord(self, layerName, locatorId, locatorData) -> bool:
        """
        If duplicate records there then return False
        :param layerName: Name of layer
        :param locatorId: locatorid field data in mysql table
        :param locatorData: Data in mysql
        :return: True if exist else False
        """
        tableName = self.layerConnectorName + layerName
        sql = f"select count({self.locatorId}) from {tableName} where {self.locatorId} = '{locatorId}' and {self.locatorData} = '{locatorData}'"
        # print(sql)
        self.getConnection()
        cursor = self.mydb.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()

        if count:
            if count[0] != 0:
                return False
            else:
                return False
        else:
            return False

    def insertRecord(self, layerName, locatorId, locatorData) -> bool:
        """
        Directly inserting a value to the mysql table
        :param layerName: Name of layer
        :param locatorId: Data
        :param locatorData: Data
        :tableName: Corresponding mysql table name
        :return: True if success else False
        """
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

    def insertLayer(self, layerName, locatorId, locatorData) -> bool:
        """
        Inserting a layer/data, if layer exists then insert only else create layer then insert
        If similar record then return False
        :param layerName: Name of layer
        :param locatorId: Data
        :param locatorData: Data
        :return: True if inserted else False
        """
        try:
            if self.checkLayerExists(layerName):
                if not self.checkSimilarRecord(layerName, locatorId, locatorData):
                    self.insertRecord(layerName, locatorId, locatorData)
                    return True
                else:
                    return False
            else:
                if self.createLayer(layerName):
                    self.insertRecord(layerName, locatorId, locatorData)
                    return True
                else:
                    return False
        except Exception as e:
            print('error in insertLayer in DataHandling', e)
            return False

    def generateLocatorFromTableField(self, layerName, locatorId, schemaName, tableName, fieldNameFromTable):
        """
        Direct layer map from a specific table data field
        :param layerName: Name of layer
        :param locatorId: Data
        :param schemaName: Schema name
        :param tableName: Name of table
        :param fieldNameFromTable: Field name
        :dataFrameFromDB: Pandas dataframe
        :return:
        """
        try:
            dataFrameFromDB = self.getDataFromDBAsDF(schemaName, tableName, fieldNameFromTable)

            if not dataFrameFromDB.empty:
                dataFrameFromDB[self.locatorId] = locatorId
                sql = f"create table {self.layerConnectorName+layerName} ({self.locatorId} varchar(200), {self.locatorData} varchar(500));"
                print(sql)

            dataFrameFromDB.rename(columns={fieldNameFromTable: self.locatorData}, inplace=True)

            # print(dataFrameFromDB)
            return dataFrameFromDB
        except Exception as e:
            print('error in generateLocatorFromTableField in DataHandling', e)
            return pd.DataFrame()

    def getDataFromDBAsDF(self, dataBaseForFetching, tableName, filedName) -> pd.DataFrame:
        """
        Get data frame from Database table as dataframe format
        :param dataBaseForFetching: Schema name
        :param tableName: Name of table
        :param filedName: Name of mysql field name
        :dbOptions: json data with database credentials
        :engine: sqlalchmy mysql connection
        :df: DataFrame object
        :return: DataFrame
        """
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
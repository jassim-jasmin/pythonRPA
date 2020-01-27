import json
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

class SqlConnect:
    def __init__(self, path):
        self.path = path
        self.dbOption = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling, 'DB', self.path)
        self.LocatorDirectory = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                          'DataFetching,filesPath', self.path)
        self.getConnection()
        self.layerConnectorName = 'datafeth_locator_'
        self.layerConnect = self.getLocatorFromDb('layer_connect')

        if self.layerConnect.empty:
            print('not data in layer_connect')
            exit()


    def getConnection(self):
        try:
            fp = open(self.dbOption, 'r')
            dbOptons = json.loads(fp.read())
            fp.close()
            # print(dbOptons['mysql']['default'])
            self.mydb = mysql.connector.connect(host=dbOptons['mysql']['default']['HOST'], user=dbOptons['mysql']['default']['USER'], password=dbOptons['mysql']['default']['PASSWORD'], database=dbOptons['mysql']['default']['DB'])
            # print(self.mydb)
        except Exception as e:
            print('error in mysql', e)
            return False

    def __del__(self):
        try:
            self.mydb.close()
        except:
            pass

    def getDbOptions(self):
        try:
            fp = open(self.dbOption, 'r')
            dbOptons = json.loads(fp.read())
            fp.close()
            return dbOptons
        except Exception as e:
            print('errror in getDbOptions', e)
            exit()

    def loadJsonToDb(self, layerName):
        try:
            try:

                layerJson = self.LocatorDirectory + layerName + '.json'

                fp = open(layerJson, 'r')
                locatorData = json.loads(fp.read())
                fp.close()

                df = pd.DataFrame()

                for locatorId, locator in locatorData.items():
                    if len(df.columns)>0:
                        temDataFrame = pd.DataFrame({'locatorData':locator, 'locator_id':locatorId})
                        df = df.append(temDataFrame)
                    else:
                        df['locatorData'] = locator
                        df.loc[df['locatorData'] == locator, 'locator_id'] = locatorId

            except Exception as e:
                print('error in json file', e)
            else:
                if self.dataFrameToDb(df, layerName):
                    return True
                else:
                    return False

        except Exception as e:
            print('error in getDatafromCSV in LocatorFromDB', e)
            return False

    def dataFrameToDb(self, dataFrame, layerName):
        try:
            dbOptions = self.getDbOptions()['mysql']['default']
            engine = create_engine(
                f'mysql+pymysql://{dbOptions["USER"]}:{dbOptions["PASSWORD"]}@{dbOptions["HOST"]}/{dbOptions["DB"]}',
                isolation_level='READ UNCOMMITTED')

            dataFrame.reset_index(drop=True, inplace=True)
            table_name_for_df = self.layerConnectorName + layerName
            dataFrame.to_sql(con=engine, name=table_name_for_df, if_exists='replace', index=False)
            return True
        except Exception as e:
            print('error in dataFrameToDb in LocatorFromDB', e)
            return False

    def loadValidtionLocatorToDb(self, layer_name):
        try:
            validationFile = self.LocatorDirectory+layer_name+'_validation.json'
            generalExceptionHandling = GeneralExceptionHandling()
            validation = generalExceptionHandling.readFileAndReturnJson(validationFile)

            # print(validation.keys())
            df = pd.DataFrame()
            for eachKey in validation.keys():
                # print(validation[eachKey])
                locatorData = validation[eachKey]
                for locatorId, locator in locatorData.items():
                    if len(df.columns) > 0:
                        temDataFrame = pd.DataFrame({'locatorData': locator, 'locator_id': locatorId})
                        df = df.append(temDataFrame)
                    else:
                        df['locatorData'] = locator
                        df.loc[df['locatorData'] == locator, 'locator_id'] = locatorId
                df.loc[df['locatorData'] == locator, 'flag'] = eachKey
            # print(df)

            if self.dataFrameToDb(df, layer_name+'_validation'):
                return True
            else:
                return False
        except Exception as e:
            print('error in loadValidationLocatorToDb in LocatorFromDB', e)
            return False

    def dBLocatorValidationToJson(self, layerName):
        try:
            dataFrame = self.getLocatorFromDb(layerName+'_validation') #mj
            if dataFrame.empty:
                return False
            flagArray = pd.unique(dataFrame['flag'])
            layerDictionary = dict()


            for eachFlag in flagArray:
                locatorDictionary = dict()
                eachFlagLayer = dataFrame[dataFrame['flag'] == eachFlag]
                locatorIdArray = pd.unique(eachFlagLayer['locator_id'])

                for eachId in locatorIdArray:
                    eachLocator = eachFlagLayer[eachFlagLayer['locator_id'] == eachId]['locatorData']
                    locatorDictionary[eachId] = eachLocator.to_list()
                layerDictionary[eachFlag] = locatorDictionary.copy()
            # print(layerDictionary)

            return layerDictionary
        except Exception as e:
            print('errro in dBLocatorValidationToJson in LocatorFromDB', e, self.layerConnectorName + layerName+'_validation')
            # print(dataFrame)
            return False

    def getLocatorFromDb(self, layer_name) ->dict:
        """
        Database converts to json
        :param layer_name: Name of layer
        :return: Json data
        """
        try:
            # print('layer name:::', layer_name)
            dbOptions = self.getDbOptions()['mysql']['default']
            engine = create_engine(
                f'mysql+pymysql://{dbOptions["USER"]}:{dbOptions["PASSWORD"]}@{dbOptions["HOST"]}/{dbOptions["DB"]}')

            # print(f'mysql+pymysql://{dbOptions["USER"]}:{dbOptions["PASSWORD"]}@{dbOptions["HOST"]}/{dbOptions["DB"]}')
            # print('select * from ' + self.layerConnectorName + layer_name)


            df = pd.read_sql('select * from ' +self.layerConnectorName+layer_name, con= engine)
            return df
        except Exception  as e:
            # print('error in getLocatorFromDb in LocatorFromDB', e)
            return pd.DataFrame()


    def buildLocatorJsonFileFromDb(self, layer_name) -> dict:
        """
        Collect data from db and convert to json format
        :param layer_name: name of layer
        :return: json data
        """
        try:
            # print('buildlocator:::', layer_name)
            df = self.getLocatorFromDb(layer_name)
            if not df.empty:
                """ Get distinct elements from dataframe """
                locator_id_array = pd.unique(df['locator_id'])
                layerDictionary = dict()

                """ Each locator id locator data array is inserted as rows """
                for eachLocatorId in locator_id_array:
                    eachLocator = df[df['locator_id'] == eachLocatorId]['locatorData']
                    """ Rows to array """
                    layerDictionary[eachLocatorId] = eachLocator.to_list()

                """ Commented for future use, It will write a json file """
                # GeneralExceptionHandling.writeJsonDataToFile(GeneralExceptionHandling, layerDictionary, self.LocatorDirectory+layer_name+ '.json')
                return layerDictionary
            else:
                print('Layer ', layer_name, 'not in db', df)
                return False
        except Exception as e:
            print('error in buildLocatorJsonFile in LocatorFromDB', e)
            print('Layer Name:', layer_name, df)
            return False

    def getLayerConnect(self, leftLayerName, leftValue, rigthLayerName, rightValue):
        try:
            # For debugg
            # print(leftLayerName+':'+leftValue+' = '+rigthLayerName+':'+rightValue)

            test = self.layerConnect.loc[(self.layerConnect['left_layer_name'] == leftLayerName) & (self.layerConnect['right_layer'] == rigthLayerName) & (self.layerConnect['left_connect'] == leftValue) & (self.layerConnect['right_connect'] == rightValue)]

            if test.empty:
                return False
            else:
                return True
        except Exception as e:
            print('error in getLayerConnect in LocatorFromDB', e)
            print(leftLayerName)
            print(self.layerConnect)
            exit()


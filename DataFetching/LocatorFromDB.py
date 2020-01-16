import json
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

class sqlConnect:
    def __init__(self):
        self.getConnection()

    def getConnection(self):
        try:
            fp = open('../db.json', 'r')
            dbOptons = json.loads(fp.read())
            fp.close()
            # print(dbOptons['mysql']['default'])
            self.mydb = mysql.connector.connect(host=dbOptons['mysql']['default']['HOST'], user=dbOptons['mysql']['default']['USER'], password=dbOptons['mysql']['default']['PASSWORD'], database=dbOptons['mysql']['default']['DB'])
            print(self.mydb)
        except Exception as e:
            print('error in mysql', e)
            return False

    def __del__(self):
        try:
            self.mydb.close()
            print('destroyed')
        except:
            pass

    # def createTableForClass(self, className):
    #     try:
    #         tableStructure = f'CREATE TABLE IF NOT EXISTS datafeth_locator_{className} (index locator_id varchar(200), locator_data text)'
    #         cursor = self.mydb.cursor()
    #         cursor.execute(tableStructure)
    #         print(tableStructure)
    #     except Exception as e:
    #         print('error in createTableForClass in LocatorFromDB', e)
    #         return False

    def getDbOptions(self):
        try:
            fp = open('../db.json', 'r')
            dbOptons = json.loads(fp.read())
            fp.close()
            return dbOptons
        except Exception as e:
            print('errror in getDbOptions', e)
            exit()

    def loadJsonToDb(self, layerName):
        try:
            try:
                layerJson = '/root/Documents/Test/' + layerName + '.json'
                dbOptions = self.getDbOptions()['mysql']['default']
                engine = create_engine(f'mysql+pymysql://{dbOptions["USER"]}:{dbOptions["PASSWORD"]}@{dbOptions["HOST"]}/{ dbOptions["DB"] }', isolation_level='READ UNCOMMITTED')

                fp = open(layerJson, 'r')
                locatorData = json.loads(fp.read())
                fp.close()

                df = pd.DataFrame()

                for locatorId, locator in locatorData.items():
                    df['locator_data'] = locator
                    df.loc[df['locator_data'] == locator, 'locator_id'] = locatorId

            except Exception as e:
                print('error in json file', e)
            else:
                df.reset_index(drop=True, inplace=True)
                table_name_for_df = 'datafeth_locator_' + layerName
                df.to_sql(con=engine, name=table_name_for_df, if_exists='replace')

        except Exception as e:
            print('error in getDatafromCSV in LocatorFromDB', e)
            return False

    def getLocatorFromDb(self, layer_name):
        dbOptions = self.getDbOptions()['mysql']['default']
        engine = create_engine(
            f'mysql+pymysql://{dbOptions["USER"]}:{dbOptions["PASSWORD"]}@{dbOptions["HOST"]}/{dbOptions["DB"]}')


        df = pd.read_sql('select * from datafeth_locator_'+layer_name, con= engine)
        return df

    def buildLocatorJsonFile(self, layer_name):
        id = 'locator_id'
        df = self.getLocatorFromDb(layer_name)
        locator_id_array = pd.unique(df[id])
        layerDictionary = dict()

        for eachLocatorId in locator_id_array:
            eachLocator = df[df[id] == eachLocatorId]['locator_data']
            layerDictionary[eachLocatorId] = eachLocator.to_list()
            print(type(eachLocator.to_list()))

        print(layerDictionary)

        fp = open('/root/Documents/Test/test2.json', 'w')
        fp.write(json.dumps(layerDictionary))
        fp.flush()
        fp.close()

sqlObj = sqlConnect()

sqlObj.loadJsonToDb('layer4')
sqlObj.buildLocatorJsonFile('layer4')
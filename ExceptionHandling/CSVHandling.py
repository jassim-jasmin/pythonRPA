import csv
import pandas as pd

class CsvHandling:
    def readCsvAsDict(self, pathWithFileName):
        try:
            fp = open(pathWithFileName, mode='r')
            if fp.readable():
                csv_reader = csv.DictReader(fp.read())
                return csv_reader
            else:
                return False

        except Exception as e:
            print('error in readCsvAsDict in CSVHandling', e)
            return False
        finally:
            try:
                fp.close()
            except Exception as e:
                pass

    def readCsvColumn(self, pathWithFileName, columnName):
        try:
            df = pd.read_csv(pathWithFileName, engine='python')
            print(df.columns)
            if columnName in df:
                return df[columnName]
            else:
                return False
        except Exception as e:
            print('error in readCsvColumn in CSVHandling', e)
            return False

    def saveAsCsv(self, csvNameWithPath, layerDictionary) -> bool:
        """

        :param csvNameWithPath:
        :param tag:
        :param layerDictionary:
        :return:
        """
        try:
            import csv

            if layerDictionary:
                with open(csvNameWithPath, 'w') as csvfile:
                    # print('opening csv', layerDictionary)
                    fieldNames = ['file_name']
                    if 'locator' in layerDictionary:
                        fieldNames.extend(layerDictionary['locator'])

                    if 'locatorData' in layerDictionary:
                        layerData = layerDictionary['locatorData']
                        csvfile.newlines
                        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
                        writer.writeheader()
                        print('csv save file:', csvNameWithPath)
                        for fileName, locatorData in layerData.items():
                            csvEacRowLocator = dict()
                            csvEacRowLocator['file_name'] = fileName

                            for data in locatorData:
                                array = []
                                dictionary = dict()

                                if type(locatorData) is  type(array):
                                    csvEacRowLocator[data] = data
                                elif type(locatorData) is type(dictionary):
                                    if data in locatorData:
                                        csvEacRowLocator[data] = locatorData[data]
                                    else:
                                        print('Error json error key' + data + ' not in ')
                                        print(locatorData)
                                        return False
                                else:
                                    print('not a dictionary', locatorData)
                                    return False

                            writer.writerow(csvEacRowLocator)
                        return True
                    else:
                        print('error creating csv invalid layer data')
                        return False
            else:
                print('error in csv dictionary in saveAsCsv in CSVHandling', layerDictionary)
                return False
        except Exception as e:
            print("error in saveAsCsv in CSVHandling", e)

    def saveDataAsCSV(self, fileName, dataDictionary, tag) -> bool:
        """
        Convert data for General Exception saveAsCsv format
        :param fileName: Name
        :param dataDictionary: csv content
        :param tag: Heading for csv if any
        :return: True if success else :return: False
        """
        try:
            csvName = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            csvName = csvName+fileName+'.csv'
            fp = open(csvName, 'w')
            fp.flush()
            fp.close()

            if self.saveAsCsv(csvName, dataDictionary):
                return True
            else:
                return False
        except Exception as e:
            print('error in saveDataAsCSV in CSVHandling', e)
            return False
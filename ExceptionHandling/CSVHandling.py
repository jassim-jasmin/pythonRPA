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

    def csvNotInCSV(self, mainCSV, subCSV, mainCSVConnColumn, subCSVConnColumn):
        try:
            notInCSV = mainCSV[~mainCSV[mainCSVConnColumn].isin(subCSV[subCSVConnColumn])]

            return notInCSV
        except Exception as e:
            print('error in csvNotInCSV in CSVHandling', e)
            return False

    def replaceSingleRow(self, dataFrame, columnName, string, replaceString):
        try:
            return dataFrame[columnName].str.replace(string, replaceString, case=False)
        except Exception as e:
            print('error in  replaceSingleRow in CSVHandling', e)
            return False

    def getDataFrameFromCSV(self, csvPathWithFileName):
        try:
            return pd.read_csv(csvPathWithFileName)
        except Exception as e:
            print('error in getDataFrameFromCSV in CSVHandling', e)
            return False

    def renameADataFrameColumn(self, dataFrame, columnName, rename):
        try:
            dataFrame.rename(columns={columnName: rename}, inplace=True)
            return dataFrame
        except Exception as e:
            print('error in renameADataFrameColumn in CSVHandling', e)
            return False

    def makeDataFrameFromArray(self, array, columnName):
        try:
            return pd.DataFrame(array, columns=[columnName])
        except  Exception as e:
            print('error in makeDataFrameFromArray in CSVHandling', e)
            return False

    def mergeTwoDataFrame(self, leftData, rightData, leftDataColumn, rightDataColumn):
        try:
            return pd.merge(leftData, rightData, left_on=leftDataColumn, right_on=rightDataColumn)
        except Exception as e:
            print('error in mergeTwoDataFrame in CSVHandling', e)
            return False

    def dataFrameToCSV(self, dataFrame, csvpathWithFileName):
        try:
            dataFrame.to_csv(csvpathWithFileName, index=False)
            return True
        except Exception as e:
            print('error in dataFrameToCSV in CSVHandling', e)
            return False

    def csvToDataFrame(self, filePahtWithName):
        try:
            data = pd.read_csv(filePahtWithName)
            return data
        except Exception as e:
            print('error in csvToDataFrame in CSVHandling', e)
            return False
from ExceptionHandling.CSVHandling import CsvHandling

class Analyse(CsvHandling):
    def __init__(self, path):
        self.path = path
        CsvHandling.__init__(self)

    def getAllFilesName(self):
        """
        todo need to remove
        :return:
        """
        try:
            filesPath = self.getJsonDataRecurssive('imagProcessing,ocrTextPath', self.path)
            allFiles = self.getDirectoryElementBykey(filesPath, 'txt')

            return allFiles
        except Exception as e:
            print('error in getAllFilesName in analyse', e)
            return False

    def getUnprocessedFiles(self, csvName) -> bool:
        """
        Create a csv with output as remaining.csv having files no data processed
        :return: True sueccess csv creation else False
        :todo: Need to process locator wise
        """
        try:
            csvPathWithFile = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            csvPathWithFileName = csvPathWithFile+csvName+'.csv'
            allFileColumnName = 'all_file_name'
            processedColumnName = 'processed_file_name'
            processedData = self.getDataFrameFromCSV(csvPathWithFileName)
            processedData = self.renameADataFrameColumn(processedData, 'file_name', processedColumnName)
            processedData[processedColumnName] = processedData[processedColumnName]+'.txt'

            allFilesWithName = self.getAllFilesName()

            if allFilesWithName:
                allFiles = self.makeDataFrameFromArray(allFilesWithName, allFileColumnName)

                pendingFiles = self.csvNotInCSV(allFiles, processedData, allFileColumnName, processedColumnName)
                # print(pendingFiles)

                pendingFiles = pendingFiles.copy()

                pendingFiles[allFileColumnName] = self.replaceSingleRow(pendingFiles, allFileColumnName, '.txt', '')

                mainCompare = self.getJsonDataRecurssive('DataFetching,comparisonFile', self.path)
                mainCompareData = self.csvToDataFrame(mainCompare)
                test = self.mergeTwoDataFrame(pendingFiles, mainCompareData, allFileColumnName, 'Image_Name')
                self.dataFrameToCSV(test, csvPathWithFile + 'test.csv')
                return True
            else:
                return False
        except Exception as e:
            print('errror in getUnprocesedFiles in analyse',e )
            return False


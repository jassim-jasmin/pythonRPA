from ExceptionHandling.CSVHandling import CsvHandling
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
from ExceptionHandling.DirecotryHandling import DrectoryHandling

class Analyse(CsvHandling):
    def __init__(self, path):
        self.path = path
        # self.path =  self.readFileAndReturnJson('../path.json')['linux']
        # DrectoryHandling.__init__(self)
        # GeneralExceptionHandling.__init__(self)
        CsvHandling.__init__(self)

    def getAllFilesName(self):
        try:
            filesPath = self.getJsonDataRecurssive('imagProcessing,ocrTextPath', self.path)
            allFiles = self.getDirectoryElementBykey(filesPath, 'txt')

            return allFiles
        except Exception as e:
            print('error in getAllFilesName in analyse', e)
            return False

    def getUnprocessedFiles(self) -> bool:
        """
        Create a csv with output as remaining.csv having files no data processed
        :return: True sueccess csv creation else False
        :todo: Need to process locator wise
        """
        try:
            import pandas as pd

            csvPathWithFile = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            csvPathWithFileName = csvPathWithFile+'allData.csv'
            allFileColumnName = 'all_file_name'
            processedColumnName = 'processed_file_name'
            processedData = pd.read_csv(csvPathWithFileName)
            processedData.rename(columns= { 'file_name': processedColumnName}, inplace=True)
            processedData[processedColumnName] = processedData[processedColumnName]+'.txt'
            # print(processedData)

            allFilesWithName = self.getAllFilesName()

            if allFilesWithName:
                allFiles = pd.DataFrame(allFilesWithName, columns=[allFileColumnName])
                # print(allFiles)

                # print(processedData[csvColumnName])
                # print(allFiles[csvColumnName])
                # print(allFiles[~allFiles[csvColumnName].isin(processedData[csvColumnName])])

                pendingFiles = allFiles[~allFiles[allFileColumnName].isin(processedData[processedColumnName])]

                pendingFiles = pendingFiles.copy()

                pendingFiles[allFileColumnName] = pendingFiles[allFileColumnName].str.replace(".txt", "", case=False)

                # print(pendingFiles[allFileColumnName])
                mainCompare = pd.read_csv('/root/Documents/Test/comparisonFile.csv')
                test = pd.merge(pendingFiles, mainCompare, left_on=allFileColumnName, right_on='Image_Name')
                print(test)
                test.to_csv(csvPathWithFile + 'test.csv', index=False)
                #
                # mergedFiles = allFiles.merge(pendingFiles)
                # print(mergedFiles)
                # pendingFiles.to_csv(csvPathWithFile+'remaining.csv', index=False)
            else:
                return False
        except Exception as e:
            print('errror in getUnprocesedFiles in analyse',e )
            return False



# obj = Analyse(False)
# obj.getUnprocessedFiles()
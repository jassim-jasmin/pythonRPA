from sklearn import  tree
# from DataFetching.StringHandling import StringHandling
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
from DataFetching.validation import LocatorValidation
from DataFetching.Locator import Locator

class DataFetchingMain:
    print('Data fetching')
    def __init__(self, path):
        self.path = path

    def trainingSet1(self):
        X = [[181, 80, 44], [177, 70, 43], [160, 60, 38],
             [154, 54, 37], [166, 65, 40], [190, 90, 47], [175, 64, 39],
             [177, 70, 40], [159, 55, 37], [171, 75, 42],
             [181, 85, 43], [168, 75, 41], [168, 77, 41]]

        Y = ['male', 'male', 'female', 'female', 'male', 'male', 'female', 'female', 'female', 'male', 'male', 'female',
             'female']
        return X,Y
    def testData1(self):
        return [[190, 70, 43], [154, 75, 38], [181, 65, 40]]

    def trainingSet2(self):
        X = [['jassim','jasmin'],['test1','test2']]
        Y = ['me','idontkonw']

        return X,Y

    def testData2(self):
        return [['jassim','jasmin']]

    def locatorDemo(self):
        try:
            print('locatorDemo')

        except Exception as e:
            print('error in locator demo', e)
    def desisionTreeTest(self):

        X,Y = self.trainingSet1()
        test_data = self.testData1()

        test_labels = ['male', 'female', 'male']


        # dtc_clf = tree.DecisionTreeClassifier()
        # dtc_clf = dtc_clf.fit(X, Y)
        # dtc_prediction = dtc_clf.predict(test_data)
        # print(dtc_prediction)

        # stringHandling = StringHandling(self.path)

        # stringHandling.test()
        # self.test()

    def generateOCR(self):
        try:
            self.locatorAdding()
            from imageProcessing.imageProcessing import ImageProcessing
            imageProcessing = ImageProcessing(self.path)

            imageNameKey = 'tif'
            filePath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'imagProcessing', self.path)
            filePath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'imagePath', filePath)

            if imageProcessing.ocrAllImage(imageNameKey, filePath):
                locator = Locator(self.path)

                # locatorDataDictionary = locator.processLocatorAndGetDataFromFile(locatorFilePathWithFileName='',sourceData='')
                return True
            else:
                print('Ocr could not complete')
                return False
        except Exception as e:
            print('error in ocrgeneration in DataFetching', e)
            return False

    def processLocator(self):
        try:
            locator = Locator(self.path)

            filePath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling, 'imagProcessing,ocrTextPath', self.path)
            locatorFilePath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling, 'DataFetching,filesPath', self.path)
            locatorFileName = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling, 'DataFetching,locatorDictionary', self.path)

            if filePath:
                locatorFilePathWithFileName = locator.processLocatorAndGetDataFromFileAll(locatorFilePath+locatorFileName, filePath)
                return locatorFilePathWithFileName
            else:
                print('error filePath in processLocator in DataFetching')
                return False
        except Exception as e:
            print('error in processLocator in DataFetching', e)
            return False

    def pdfHandling(self, locatorFilePathWithFileName):
        try:
            from PdfHandling.PdfHandling import PdfHanling
            pdfHandling = PdfHanling()
            pdfPath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                             'imagProcessing,pdfPath',
                                                                             self.path)
            imagePath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                             'imagProcessing,imagePath',
                                                                             self.path)

            for fileName, locatorDataDictionary in locatorFilePathWithFileName.items():
                print('filename: ', fileName)
                for locatorFinalId, locatorDataArray in locatorDataDictionary.items():
                    pdfHandling.pdfGenerator(imagePath, fileName, '.tif', pdfPath)
                    pdfHandling.highlihtPDF(pdfPath, fileName, locatorDataArray)

            return True
        except Exception as e:
            print('error in pdfHandling in DataFetching', e)
            return False

    def imageDataProcessing(self):
        try:
            # if not self.generateOCR():
            #     exit()
            self.locatorAdding()
            self.finalLocatorAdding()
            locatorDataDirectory = self.processLocator()
            if self.addLocatorValidation():
                print('validation added')

            # print(locatorDataDirectory)
            if locatorDataDirectory:
                validation = self.validatiingLocator(locatorDataDirectory)
                locator = Locator(self.path)
                locatorDataWithValidation = locator.getValidatedLocatorData(locatorDataDirectory, validation)

                finalCsv = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                           'DataFetching,processedDataPath',
                                                                           self.path)

                connectedLocator = self.connectingLocator(locatorDataWithValidation)
                finalData = self.processLocatorFromDict(connectedLocator)

                if finalCsv:
                    csvHead =['legal','parcel', 'parcel_number', 'lot', 'block']
                    if locator.saveAsCsv(finalCsv, 'Final Data fetched\n', finalData, csvHead):
                        print('saving')

            print('completed')

            # self.pdfHandling(locatorFilePathWithFileName)

            return True
        except Exception as e:
            print('error in imageDataProcessing in DataFetching', e)
            return False



    def locatorAdding(self):
        dataFetchingLocatorDictionary = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                  'DataFetching,locatorDictionary',
                                                                  self.path)
        locatorDirectory = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                  'DataFetching,filesPath',
                                                                  self.path)

        locator = Locator(self.path)

        testLocator = ['lot', 'block', 'plat']
        locatorId = 'legal'
        locator.addLocatorToDictionary(testLocator, locatorId, dataFetchingLocatorDictionary, locatorDirectory)

        testLocator = ['lot', 'block', 'plat', 'county']
        locatorId = 'legal'
        locator.addLocatorToDictionary(testLocator, locatorId, dataFetchingLocatorDictionary, locatorDirectory)

        testLocator = ['lot', 'plat', 'thereof']
        locatorId = 'legal'
        locator.addLocatorToDictionary(testLocator, locatorId, dataFetchingLocatorDictionary, locatorDirectory)

        testLocator = ['271-02171-0101', 'parcel']
        locatorId = 'parcel'
        locator.addLocatorToDictionary(testLocator, locatorId, dataFetchingLocatorDictionary, locatorDirectory)

    def addLocatorValidation(self):
        try:
            filesPath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                              'DataFetching,filesPath',
                                                                              self.path)
            validationLocator = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                              'DataFetching,validationLocator',
                                                                              self.path)
            # partial fetch
            locatorValidationDirectoryPath = filesPath + validationLocator + '.json'
            locatorValidation = LocatorValidation(self.path)
            locatorData = [('parcel','\d\d\d-\d\d\d\d\d-\d\d\d\d', 'True'),('legal', '^ *\d', 'False'),('parcel', '\d\d\d-\d\d\d\d\d-\d\d\d\d \d\d\d-\d\d\d\d\d-\d\d\d\d', 'False')]

            for eachLocaotrData in locatorData:
                locatorId, pattern, flag = eachLocaotrData
                if not locatorValidation.addValidation(locatorValidationDirectoryPath, locatorId, pattern, flag):
                    print('error in adding locator validation')
                    return False

            return True
        except Exception as e:
            print('error in addLocatorValidation in DataFetching', e)
            return False

    def validatiingLocator(self, locatorFilePathWithFileNameDictionary):
        try:
            if locatorFilePathWithFileNameDictionary:
                dataFetchingFilesPath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                                   'DataFetching,filesPath',
                                                                                   self.path)
                dataFetchingValidationLocatorPath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                                   'DataFetching,validationLocator',
                                                                                   self.path)

                locatorValidationDirectoryPath = dataFetchingFilesPath + dataFetchingValidationLocatorPath + '.json'
                locatorJsonFileNameWithPath = locatorValidationDirectoryPath
                # print(locatorFilePathWithFileName)
                locatorValidation = LocatorValidation(self.path)

                return locatorValidation.getValidatedLocaotr(locatorFilePathWithFileNameDictionary, locatorJsonFileNameWithPath)
            return False

        except Exception as e:
            print('error in validatinglocator in DataFetching', e)
            return False

    def finalLocatorAdding(self):

        dataFetchingLocatorDictionary = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                                           'DataFetching,locatorFinalDictionary',
                                                                                           self.path)
        locatorDirectory = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                                       'DataFetching,filesPath',
                                                                                       self.path)


        locator = Locator(self.path)
        testLocator = ['271-02171-0101']
        locatorId = 'parcel_number'
        locator.addLocatorToDictionary(testLocator, locatorId, dataFetchingLocatorDictionary, locatorDirectory)

        testLocator = ['LOTS 1, 2, 3, 4', 'LOTS 1']
        locatorId = 'lot'
        locator.addLocatorToDictionary(testLocator, locatorId, dataFetchingLocatorDictionary, locatorDirectory)
        testLocator = ['Block B,']
        locatorId = 'block'
        locator.addLocatorToDictionary(testLocator, locatorId, dataFetchingLocatorDictionary, locatorDirectory)

    def processLocatorFromDict(self, locatorData):
        try:
            locator = Locator(self.path)
            locatorFilePath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                              'DataFetching,filesPath',
                                                                              self.path)
            locatorFileName = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                              'DataFetching,locatorFinalDictionary',
                                                                              self.path)
            if locatorData:
                locatorDataDictionary = locator.processLocatorAndGetDataFromDictionary(locatorFilePath+locatorFileName,
                                                                                  locatorData)
                return locatorDataDictionary
            else:
                print('error filePath in processLocatorFromDict in DataFetching')
                return False
        except Exception as e:
            print('error in processLocatorFromDict in DataFetching', e)
            return False

    def connectingLocator(self, dictionary):
        try:
            processedDict = dict()
            connectorKeys = dict()

            #first locator key      = final locator key
            connectorKeys['parcel_number'] = 'parcel'
            connectorKeys['lot'] = 'legal'
            connectorKeys['block'] = 'legal'

            processedDict['connectorKeys'] = connectorKeys
            processedDict['locatorData'] = dictionary
            return processedDict
        except Exception as e:
            print('error in connectingLocator in DataFetching', e)
            return False
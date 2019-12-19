from sklearn import  tree
# from DataFetching.StringHandling import StringHandling
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
from DataFetching.validation import LocatorValidation

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
            from DataFetching.Locator import Locator

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
                from DataFetching.Locator import Locator
                locator = Locator(self.path)

                # locatorDataDictionary = locator.processLocatorAndGetDataFromFile(locatorFilePathWithFileName='',sourceData='')
                return True
            else:
                return False
        except Exception as e:
            print('error in ocrgeneration in DataFetching', e)
            return False

    def processLocator(self):
        try:
            from DataFetching.Locator import Locator
            locator = Locator(self.path)

            filePath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'imagProcessing', self.path)
            filePath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'ocrTextPath', filePath)

            locatorFilePath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'DataFetching', self.path)
            locatorFilePath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'filesPath', locatorFilePath)

            locatorFileName = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'DataFetching', self.path)
            locatorFileName = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'locatorDictionary',
                                                                   locatorFileName)
            if filePath:
                locatorFilePathWithFileName = locator.processLocatorAndGetDataFromFileAll(locatorFilePath+locatorFileName, filePath)
                return locatorFilePathWithFileName
            else:
                return False
        except Exception as e:
            print('error in processLocator in DataFetching', e)
            return False

    def pdfHandling(self, locatorFilePathWithFileName):
        try:
            from PdfHandling.PdfHandling import PdfHanling
            pdfHandling = PdfHanling()

            pdfPath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'imagProcessing', self.path)
            pdfPath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'pdfPath', pdfPath)
            imagePath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'imagProcessing', self.path)
            imagePath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'imagePath',
                                                             imagePath)

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
            # self.generateOCR()
            locatorFilePathWithFileName = self.processLocator()
            self.addLocatorValidation()
            validation = self.validatiingLocator(locatorFilePathWithFileName)
            print(validation)
            # self.pdfHandling(locatorFilePathWithFileName)

            return True
        except Exception as e:
            print('error in imageDataProcessing in DataFetching', e)
            return False



    def locatorAdding(self):
        from DataFetching.Locator import Locator
        locator = Locator(self.path)

        testLocator = ['warranty deed']
        locatorId = 'head'
        locator.addLocatorToDictionary(testLocator, locatorId)

        testLocator = ['according to the recorded', 'Parcel Identification Number']
        locatorId = 'parcel'

        locator.addLocatorToDictionary(testLocator, locatorId)

        testLocator = ['this deed']
        locatorId  = 'test'
        locator.addLocatorToDictionary(testLocator, locatorId)

    def testt(self):
        try:
            from DataFetching.Locator import Locator
            locator = Locator(self.path)
            locatorId = 'head'
            testLocator = ['QUIT','CLAIM', 'DEED', 'Document Number']
            locator.addLocatorToDictionary(testLocator, locatorId)
            testLocator = ['010-00532-0000', 'Parcel', 'Identification Number']
            testLocator = ['GRANTOR:']


            locator.addLocatorToDictionary(testLocator, locatorId)

            testLocator = ['010-00532-0000', 'Parcel', 'Identification Number']
            locatorId = 'parcel'
            locator.addLocatorToDictionary(testLocator, locatorId)

            from imageProcessing.imageProcessing import ImageProcessing

            if ImageProcessing.ocrImage(ImageProcessing, self.path['Data']['imageFile'], 'tif',
                                        self.path['Data']['imageFile'], self.path['Data']['path']):
                fp = open(self.path['Data']['path']+self.path['Data']['imageFile']+'.txt', encoding="utf8")
                sourceData = fp.read()
                fp.close()
                locatorFilePathWithFileName = self.path['DataFetching']['filesPath'] + self.path['DataFetching'][
                    'locatorDictionary']

                if sourceData:
                    locatorDataDictionary = locator.processLocatorAndGetDataFromFile(locatorFilePathWithFileName, sourceData)
                # locatorDataDictionary = self.processLocatorAndGetDataFromFile(locatorFilePathWithFileName, sourceData)

                from PdfHandling.PdfHandling import PdfHanling

                for locatorFinalId, locatorDataArray in locatorDataDictionary.items():
                    print(locatorId)
                    PdfHanling.pdfGenerator(PdfHanling,self.path['Data']['path'], self.path['Data']['imageFile'],'.tif')
                    PdfHanling.highlihtPDF(PdfHanling, self.path['Data']['path'], self.path['Data']['imageFile'], locatorDataArray)
                print('ocr complete')
            else:
                print('error')
        except Exception as e:
            print('error in test ', e)

    def addLocatorValidation(self):
        try:
            locatorValidation = LocatorValidation(self.path)
            locatorValidation.addValidation('parcel','\d\d\d-\d\d\d\d\d-\d\d\d\d', 'True')
            locatorValidation.addValidation('parcel', '\d\d\d-\d\d\d\d\d-\d\d\d\d', 'True')
            return True
        except Exception as e:
            print('error in addLocatorValidation in DataFetching', e)
            return False

    def validatiingLocator(self, locatorFilePathWithFileName):
        try:
            print('validation')
            # print(locatorFilePathWithFileName)
            locatorValidation = LocatorValidation(self.path)
            validationProgress = True

            validationDictionary = dict()
            for fileName, locatorDirectory in locatorFilePathWithFileName.items():
                print(fileName)
                validity = dict()
                for locatorId, locatorData in locatorDirectory.items():
                    validity[locatorId] = locatorValidation.getValidity(locatorId, locatorData)
                validationDictionary[fileName] = validity
            return validationDictionary

        except Exception as e:
            print('error in validatinglocator in DataFetching', e)
            return False
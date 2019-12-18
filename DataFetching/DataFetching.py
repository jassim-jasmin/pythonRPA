from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
from DataFetching.validation import LocatorValidation
from DataFetching.Locator import Locator

class DataFetchingMain:
    print('Data fetching')
    def __init__(self, path):
        self.path = path

    def generateOCR(self, imagesPath, ocrTextPath):
        try:
            # self.locatorAdding()
            from imageProcessing.imageProcessing import ImageProcessing
            imageProcessing = ImageProcessing(self.path)

            imageNameKey = 'tif'

            return imageProcessing.ocrAllImage(imageNameKey, imagesPath, ocrTextPath)
        except Exception as e:
            print('error in ocrgeneration in DataFetching', e)
            return False

    def processLayerFromSourceFile(self, layerName, ocrTextDirectryPath):
        try:
            locator = Locator(self.path)
            locatorFilePath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling, 'DataFetching,filesPath', self.path)

            if ocrTextDirectryPath:
                layerData = locator.processLocatorAndGetDataFromFileAll(locatorFilePath+layerName, ocrTextDirectryPath)
                validation = LocatorValidation(self.path)

                layer1Validation = validation.validateLayer(layerData, 'layer1')
                # print('valid', layer1Validation)

                validatedLayer = dict()
                validatedLocator = dict()
                for fileName, locatorData in layerData.items():
                    if fileName in layer1Validation:
                        validationLayerLocator = layer1Validation[fileName]
                        for eachLocator in validationLayerLocator:
                            if eachLocator in locatorData:
                                validatedLocator[eachLocator] =  locatorData[eachLocator]
                            # else:
                            #     print('invlid locaotr id in data fetch', eachLocator)
                        validatedLayer[fileName] = validatedLocator
                    # else:
                    #     validatedLayer = locatorData[fileName]

                return validatedLayer
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

    def finalValidatingLocator(self, locatorFilePathWithFileNameDictionary):
        try:
            if locatorFilePathWithFileNameDictionary:
                dataFetchingFilesPath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                                   'DataFetching,filesPath',
                                                                                   self.path)
                dataFetchingValidationLocatorPath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                                   'DataFetching,finalValidation',
                                                                                   self.path)

                locatorValidationDirectoryPath = dataFetchingFilesPath + dataFetchingValidationLocatorPath + '.json'
                locatorJsonFileNameWithPath = locatorValidationDirectoryPath
                # print(locatorFilePathWithFileName)
                locatorValidation = LocatorValidation(self.path)

                return locatorValidation.getValidatedLocaotr(locatorFilePathWithFileNameDictionary, locatorJsonFileNameWithPath)
            return False

        except Exception as e:
            print('error in finalValidatingLocator in DataFetching', e)
            return False



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
                # print(locatorDataDictionary)
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

    def imageDataProcessing(self):
        try:
            imagesPath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                      'imagProcessing,imagePath',
                                                                      self.path)
            ocrTextDirectoryPath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                                  'imagProcessing,ocrTextPath',
                                                                                  self.path)
            if not self.generateOCR(imagesPath, ocrTextDirectoryPath):
                exit()

            if not self.addLoatorLayer('layer1', self.getLayer1()):
                return False

            if not self.addLoatorLayer('layer2', self.getLayer2()):
                return False

            validation = LocatorValidation(self.path)

            validation.addValidationLayer('layer1', self.getValidation1())
            validation.addValidationLayer('layer2', self.getValidation2())

            # locatorDataDirectory = self.processLayerFromSourceFile('layer1', ocrTextDirectoryPath)
            layerData = self.processLayerFromSourceFile('layer1', ocrTextDirectoryPath)

            print('validation out', layerData)

            # if locatorDataDirectory:
            #     validation = self.validatiingLocator(locatorDataDirectory)
            #     locator = Locator(self.path)
            #     locatorDataWithValidation = locator.getValidatedLocatorData(locatorDataDirectory, validation)
            #
            #     finalCsv = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
            #                                                                'DataFetching,processedDataPath',
            #                                                                self.path)
            #     import json
            #     fp = open('DataFetching/files/finalValidation.json', 'r')
            #     data = json.loads(fp.read())
            #     fp.close()
            #     # finalValdation = self.finalValidatingLocator(data)
            #
            #     connectedLocator = self.connectingLocator(locatorDataWithValidation)
            #     finalData = self.processLocatorFromDict(connectedLocator)
            #
            #     finalValidation = locator.getValidatedLocatorData(finalData, )
            #
            #     if finalCsv:
            #         fp = open(finalCsv, 'w')
            #         fp.flush()
            #         fp.close()
            #         csvHead =['legal','parcel', 'parcel_number', 'lot', 'block']
            #         if locator.saveAsCsv(finalCsv, 'Final Data fetched\n', finalData, csvHead):
            #             print('saving')

            print('completed')

            # self.pdfHandling(locatorFilePathWithFileName)

            return True
        except Exception as e:
            print('error in imageDataProcessing in DataFetching', e)
            return False

    def getLayer1(self):
        data = []
        data.append(['legal', ['lot', 'block', 'plat']])
        data.append(['legal', ['lot', 'block', 'plat', 'county']])
        data.append(['legal', ['lot', 'plat', 'thereof']])
        data.append(['parcel', ['271-02171-0101', 'parcel']])

        return data

    def getLayer2(self):
        data = []

        data.append(['parcel_number', ['271-02171-0101']])
        data.append(['lot', ['LOT EIGHT', 'LOT 1']])
        data.append(['block', ['BLOCK ELEVEN']])

        return data

    def getValidation1(self):
        data = []
        data.append(('parcel', '\d\d\d-\d\d\d\d\d-\d\d\d\d', 'True'))
        data.append(('legal', '^ *\d', 'False'))
        data.append(('parcel', '\d\d\d-\d\d\d\d\d-\d\d\d\d \d\d\d-\d\d\d\d\d-\d\d\d\d', 'False'))

        return data

    def getValidation2(self):
        data = []
        data.append(('lot', 'lot \w', 'False'))

        return data

    def addLoatorLayer(self, layerName, data):
        try:
            locatorDirectory = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                      'DataFetching,filesPath',
                                                                      self.path)
            fp = open(locatorDirectory+layerName+'.json', 'w')
            fp.flush()
            fp.close()

            locator = Locator(self.path)

            for locatorId, locatorData in data:
                if not locator.addLocatorToDictionary(locatorData, locatorId, layerName, locatorDirectory):
                    return False

            return True
        except Exception as e:
            print('error in addLocatorLayer in DataFetching', e)
            return False


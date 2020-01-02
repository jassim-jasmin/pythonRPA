from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
from DataFetching.Locator import Locator

class DataFetchingMain(Locator, GeneralExceptionHandling):
    def __init__(self, path):
        """
        Class designed for fetching data
        :param path: General argument json file
        """
        self.path = path
        Locator.__init__(self, path)
        GeneralExceptionHandling.__init__(self)

    def generateOCR(self, imagesPath, ocrTextPath) -> bool:
        """
        For performing ocr
        :param imagesPath: Path of the image to convert
        :param ocrTextPath: Path for saving text
        :return: True if success else :return: False
        """
        try:
            from imageProcessing.imageProcessing import ImageProcessing
            imageProcessing = ImageProcessing(self.path)

            imageNameKey = 'tif'

            return imageProcessing.ocrAllImage(imageNameKey, imagesPath, ocrTextPath)
        except Exception as e:
            print('error in ocrgeneration in DataFetching', e)
            return False

    def pdfHandling(self, locatorFilePathWithFileName) -> bool:
        """
        For performing highlighting serachable pdf
        :param locatorFilePathWithFileName: json contains file name and locator
        :return: True if success else :return: False
        ":Todo: json file might contain locator connector and locator array confirm and sort it out
        """
        try:
            from PdfHandling.PdfHandling import PdfHanling
            pdfHandling = PdfHanling()
            pdfPath = self.getJsonDataRecurssive('imagProcessing,pdfPath', self.path)
            imagePath = self.getJsonDataRecurssive('imagProcessing,imagePath', self.path)

            for fileName, locatorDataDictionary in locatorFilePathWithFileName.items():
                print('filename: ', fileName)
                for locatorFinalId, locatorDataArray in locatorDataDictionary.items():
                    pdfHandling.pdfGenerator(imagePath, fileName, '.tif', pdfPath)
                    pdfHandling.highlihtPDF(pdfPath, fileName, locatorDataArray)

            return True
        except Exception as e:
            print('error in pdfHandling in DataFetching', e)
            return False

    def addLoatorLayer(self, layerName, data) -> bool:
        """
        Dictionary generation with locator
        :param layerName: name of layer
        :param data: json data for a layer
        :return: True if sucess else :return: False
        """
        try:
            locatorDirectory = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            print(locatorDirectory+layerName+'.json')
            fp = open(locatorDirectory+layerName+'.json', 'w')
            fp.flush()
            fp.close()

            if data:
                for locatorId, locatorData in data:
                    if not self.addLocatorToDictionary(locatorData, locatorId, layerName, locatorDirectory):
                        return False

                return True
            else:
                print('json data input for layer ' + layerName + ' is empty')
                return False
        except Exception as e:
            print('error in addLocatorLayer in DataFetching', e)
            return False

    def imageDataProcessing(self) -> bool:
        """
        Collect images and  perform ocr for each images
        Locator initialization and performing
        Data fetching
        Processed out
        :return: True if success else :return: False
        """
        try:
            imagesPath = self.getJsonDataRecurssive('imagProcessing,imagePath', self.path)
            ocrTextDirectoryPath = self.getJsonDataRecurssive('imagProcessing,ocrTextPath', self.path)

            # if not self.generateOCR(imagesPath, ocrTextDirectoryPath):
            #     exit()

            # if not self.addLoatorLayer('layer1', self.getLayer1()):
            #     return False
            #
            # if not self.addLoatorLayer('layer2', self.getLayer2()):
            #     return False

            if not self.addLoatorLayer('layer3', self.getLayer3()):
                return False

            # self.addValidationLayer('layer1', self.getValidation1())
            # self.addValidationLayer('layer2', self.getValidation2())
            # self.addValidationLayer('layer3', [])
            # self.addValidationLayer('layer4', [])

            # layerData = self.processLocatorAndGetDataFromFileAll('layer1', ocrTextDirectoryPath)
            # print('layer1 completed')
            #
            layer3Data = self.processLocatorAndGetDataFromFileAll('layer3', ocrTextDirectoryPath)

            # print('layer1 out', layerData)
            # if not self.saveDataAsCSV('layer1Out', layerData, 'layer1Out'):
            #     print('error saving csv layer1')
            #     return False
            #
            # if not self.saveDataAsCSV('layer3Out', layer3Data, 'layer3'):
            #     print('error saving csv layer1')
            #     return False

            # locatorDataDictionary = self.processLayerFromLayer('layer2', layerData, self.connectingLocator())

            titleCompay = self.processLayerFromLayer('layer4', layer3Data, self.connectingLocator())

            # print('layer2 out', locatorDataDictionary)
            # if locatorDataDictionary:
            #     if not self.saveDataAsCSV('layer2Out', locatorDataDictionary, 'layer2Out'):
            #         print('error saving csv layer2')
            #         return False
            # else:
            #     print('processing layer1 with layer2 failed')
            #     return False

            if titleCompay:
                if not self.saveDataAsCSV('layer4Out', titleCompay, 'Title Company'):
                    print('error saving csv layer2')
                    return False
            else:
                print('no data in layer4')
                return False


            print('completed')

            # self.pdfHandling(locatorFilePathWithFileName)

            return True
        except Exception as e:
            print('error in imageDataProcessing in DataFetching', e)
            return False

    def connectingLocator(self) -> dict:
        """
        Connector for each locator in different layers
        :return: connector dictionary
        """
        try:
            connectorKeys = dict()

            #first locator key      = final locator key
            connectorKeys['parcel_number'] = 'parcel'
            connectorKeys['parcel_number_new'] = 'parcel_1'
            connectorKeys['formated_parcel_number'] = 'parcel_1'
            connectorKeys['titleName'] = 'title_search'
            # connectorKeys['parcel_data_2'] = 'parcel_2'

            # connectorKeys['parcel_number_1'] = 'parcel'
            # connectorKeys['lot'] = 'legal'
            # connectorKeys['block'] = 'legal'
            # connectorKeys['lot_1'] = 'legal'

            return connectorKeys
        except Exception as e:
            print('error in connectingLocator in DataFetching', e)
            return False

    def getLayer1(self) -> list:
        """
        Custom locator asigning
        :return: locator array
        :Todo: Direct regular expression need to add (To improve fetching)
        """
        data = []
        # data.append(['legal', ['lot', 'block', 'plat']])
        # data.append(['legal', ['lot', 'block', 'plat', 'county']])
        # data.append(['legal', ['lot', 'plat', 'thereof']])
        # data.append(['parcel', ['271-02171-0101', 'parcel']])
        # data.append(['parcel', ['APN #;', 'R0235662']])
        # data.append(['parcel', ['A.P.N.', 'R1605212']])
        # data.append(['parcel', ['APN ', '17-02421']])
        data.append(['parcel_1', ['Parcel 1D Number:','R0235659 / 4009138524369']])
        data.append(['parcel_1', ['APN #:', '4-010-129-090-012']])
        data.append(['parcel_1', ['PARCEL NUMBER:','4016159029035']])

        # data.append(['parcel_1', ['Parcel Number: 114-150-49-06']])
        data.append(['parcel_1', ['APN: 594-020-17-00']])
        data.append(['parcel_1', ['APN: 108-505-34']])
        data.append(['parcel_1', ['A.P.N.: 6205200200']])
        data.append(['parcel_1', ['A.P. # 278-424-31-00']])
        data.append(['parcel_1', ['APN/Parcel ID(s):', '465-192-06-00']])
        data.append(['parcel_1', ['APN No. 186-270-35']])
        data.append(['parcel_1', ['A.P.N.: 501-174-60-08']])
        data.append(['parcel_1', ['Assessor’s Parcel No. 624-440-33-00']])
        data.append(['parcel_1', ['Parcel N', '595-221-08-41']])
        data.append(['parcel_1', ['Tax Parcel/Bill No. 380-243-11-00']])
        data.append(['parcel_1', ['APN: 1876400500']])
        data.append(['parcel_1', ['Parcel/Account Number: 582-420-16-00']])
        data.append(['parcel_1', ['APN 254 - 222 -20-60']])
        data.append(['parcel_1', ['Tax ID No: 001516 (Map No.) 496-040-20-00 (Parcel No.)']])
        data.append(['parcel_1', ['A. P N. 447-390-11']])
        data.append(['parcel_1', ['A. P. N.: 216-53 1-15-00']])
        data.append(['parcel_2', ['594-020-17-00']])

        return data

    def getValidation1(self) -> list:
        """
        Custom validation asigning
        :return: validation array
        :Todo: Pattern build need to add, only direct regular expressions are allowed
        """
        data = []
        # data.append(('parcel', '\d\d\d-\d\d\d\d\d-\d\d\d\d', 'True'))
        # data.append(('legal', '^ *\d', 'False'))
        # data.append(('parcel', '\d\d\d-\d\d\d\d\d-\d\d\d\d \d\d\d-\d\d\d\d\d-\d\d\d\d', 'False'))
        # data.append(('parcel', '\d\d\d\d\d\d\d\d', 'True'))
        # data.append(('parcel', '^A', 'True'))

        return data

    def getLayer2(self) -> list:
        """
        Custom locator asigning
        :return: locator array
        """
        data = []

        # data.append(['parcel_number', ['271-02171-0101']])
        # data.append(['lot', ['LOT 1']])
        # data.append(['lot_1', ['lot three', 'LOT FOUR', 'LOT SIXTEEN', 'lots four']])
        # data.append(['block', ['BLOCK ELEVEN']])
        # data.append(['parcel_number', ['R0242052']])
        # data.append(['parcel_number', ['RO242052']])
        # data.append(['parcel_number', ['02-34000']])
        # data.append(['parcel_number_new', ['108-505-34']])

        data.append(['parcel_number_new', ['186-270-35']])
        data.append(['parcel_number_new', ['254 - 222 -20-60']])
        data.append(['parcel_number_new', ['6205200200']])
        data.append(['formated_parcel_number', ['4-010-129-090-012']])
        data.append(['formated_parcel_number', ['114-150-49-06']])
        # data.append(['parcel_data_2', ['594-020-17-00']])
        # data.append(['parcel_number', ['10-33009']])

        return data

    def getValidation2(self) -> list:
        """
        Custom validation asigning
        :return: validation array
        """
        data = []
        # data.append(('lot', 'LOT [A-Z]$', 'False'))
        # data.append(('lot_1', '^[0-9]', 'False'))
        # data.append(('lot_1', 'LOT THREE \(3\)', 'False'))
        # data.append(('lot_1', 'STATE BAR', 'False'))
        # data.append(('lot', 'lot *[\\"]+', 'False'))
        # data.append(('lot', 'lot \w{2,}', 'False'))
        # data.append(('lot', '^[0-9]', 'False'))
        # data.append(('lot', 'one', 'true'))
        # data.append(('parcel_number','\d\d\d-\d\d\d\d\d-\d\d\d\d', 'True'))
        # data.append(('parcel_number', '\d\d\d\d\d\d', 'True'))

        return data

    def getLayer3(self):
        data = []
        data.append(['title_search', ['RECORDING REQUESTED BY:', 'ABOVE THIS LINE FOR RECORDER']])
        return data

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

            if self.saveAsCsv(csvName, tag+'\n', dataDictionary):
                return True
            else:
                return False
        except Exception as e:
            print('error in saveDataAsCSV in DataFetching', e)
            return False